-- Exports the per-suburb incident facts that a suburb landing page needs.
--
-- A suburb page is only worth publishing if it can say something TRUE and
-- SPECIFIC about that suburb. Without real numbers the page is a template with
-- the name swapped, which is what Google's doorway-abuse and scaled-content
-- policies are aimed at. So: no data, no page.
--
-- Suburb name comes from the "Location: <suburb>" line that
-- vic-emergency.service.js writes into incident_alerts.notes.
--
-- Run against the production read replica:
--   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -At -f tools/export-suburb-stats.sql \
--     | python3 -I tools/stats-to-json.py > tools/suburb-stats.json

WITH located AS (
    SELECT
        initcap(trim(substring(notes FROM 'Location: ([^\n]+)'))) AS suburb,
        category,
        latitude,
        longitude,
        created_at
    FROM incident_alerts
    WHERE source = 'system'                      -- official VicEmergency rows only
      AND notes ~ 'Location: '
      AND created_at >= now() - interval '12 months'
),
ranked AS (
    SELECT
        suburb,
        count(*)                                        AS incidents_12mo,
        count(DISTINCT category)                        AS category_count,
        round(avg(latitude)::numeric, 4)                AS centre_lat,
        round(avg(longitude)::numeric, 4)               AS centre_lon,
        max(created_at)                                 AS most_recent,
        (SELECT string_agg(c, '|' ORDER BY n DESC)
         FROM (SELECT category AS c, count(*) AS n
               FROM located l2
               WHERE l2.suburb = located.suburb
               GROUP BY category
               ORDER BY n DESC
               LIMIT 3) top3)                           AS top_categories
    FROM located
    WHERE suburb IS NOT NULL
      AND length(suburb) BETWEEN 3 AND 40
    GROUP BY suburb
)
SELECT suburb, incidents_12mo, top_categories, centre_lat, centre_lon, most_recent
FROM ranked
-- The gate. Below this a page has nothing of its own to say, so it is not built.
WHERE incidents_12mo >= 12
ORDER BY incidents_12mo DESC;
