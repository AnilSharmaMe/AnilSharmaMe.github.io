#!/usr/bin/env python3
"""Generates the location landing pages from one shared template.

Each page is a real page with its own content: the goal is to rank for
local intent ("crime alert app Melbourne", "is Melton safe"), and thin
near-duplicate pages get treated as doorway pages, so every BODY below
says something specific to its place.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regions import REGIONS

IOS = "https://apps.apple.com/au/app/spotterapp/id6755062103"
PLAY = "https://play.google.com/store/apps/details?id=spotter.anilsharmame.github.com"
SITE = "https://spotterapp.com.au"

TEMPLATE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{site}/{slug}">
    <meta name="geo.region" content="AU-VIC">
    <meta name="geo.placename" content="{placename}">

    <meta property="og:type" content="article">
    <meta property="og:url" content="{site}/{slug}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{site}/app-icon.png">
    <meta name="twitter:card" content="summary">

    <script type="application/ld+json">
{schema}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="location.css">
</head>
<body>
    <nav>
        <a href="/" class="logo"><img src="app-icon.png" alt="Spotter logo" width="32" height="32" style="border-radius: 22%;">Spotter</a>
        <div class="nav-links">
            <a href="/#features">Features</a>
            <a href="/#security">Security</a>
            <a href="/#faq">FAQ</a>
            <a href="melbourne-safety-app.html">Melbourne</a>
            <a href="victoria-emergency-alerts.html">Victoria</a>
        </div>
        <a href="{ios}" class="btn" target="_blank" rel="noopener noreferrer">Get Spotter</a>
    </nav>

    <main>
        <p class="breadcrumb"><a href="/">Spotter</a> &rsaquo; {breadcrumb}</p>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
{body}
        <div class="cta">
            <h2 style="margin-top:0;">Get Spotter</h2>
            <p>Free on iOS and Android. Search &ldquo;SpotterApp&rdquo; in either store.</p>
            <div class="cta-buttons">
                <a href="{ios}" class="btn" target="_blank" rel="noopener noreferrer">Download for iPhone</a>
                <a href="{play}" class="btn btn-play" target="_blank" rel="noopener noreferrer">Download for Android</a>
            </div>
        </div>

        <div class="related">
            <h3 style="margin-top:0;">Related pages</h3>
            <ul>
{related}
            </ul>
        </div>
    </main>

    <footer>
        <p><a href="/">Home</a><a href="privacy-policy.html">Privacy Policy</a><a href="terms-of-service.html">Terms of Service</a><a href="mynetra.html">Mynetra Pty Ltd</a></p>
        <p style="margin-top:12px;">&copy; 2026 Mynetra Pty Ltd (ACN 678 559 736). Spotter is not an emergency service. In an emergency, call 000.</p>
    </footer>
</body>
</html>
"""

OFFICIAL_NOTE = """        <div class="callout">
            <p><strong>Spotter is not an emergency service.</strong> In an emergency, always call 000. Spotter does not replace
            VicEmergency, the CFA or Victoria Police &mdash; it reads the same official feeds and puts them next to your
            family&rsquo;s safety in one app, so you are not checking four sources at once.</p>
        </div>
"""

MELBOURNE_BODY = """        <h2>What you actually get in Melbourne</h2>
        <p>Spotter reads Victoria&rsquo;s official incident feed &mdash; the same
        <a href="https://www.emergency.vic.gov.au/respond/" target="_blank" rel="noopener noreferrer">VicEmergency</a> data that
        powers the state&rsquo;s warnings &mdash; and shows the incidents near you, sorted by how close they are rather than by
        when they were filed. Structure fires, hazardous material incidents, rescues, flooding and grass fires across
        Greater Melbourne appear on the home feed as they are published.</p>
        <p>Two things are deliberately different from a plain feed reader:</p>
        <ul>
            <li><strong>It ranks by distance to your people, not just to you.</strong> If someone in your circle is within
            1&nbsp;km of a live incident, that becomes the top card &mdash; &ldquo;Mum is 450&nbsp;m from this: Fire&rdquo; &mdash; with a
            one-tap &ldquo;Are you OK?&rdquo; message. Beyond 1&nbsp;km nothing is raised, because a fire three suburbs away is not news.</li>
            <li><strong>It never tells you an area is safe.</strong> When there is nothing live nearby the app says
            &ldquo;Nothing reported near you&rdquo;. That is a different claim from &ldquo;you are safe&rdquo;, and we are not willing to make
            the second one.</li>
        </ul>

        <h2>Risk Radar: a warning before you arrive</h2>
        <p>Most safety apps tell you what already happened. Risk Radar watches the 20 nearest repeat-incident areas around
        you using the phone&rsquo;s own region monitoring, so it works with the app closed and costs almost no battery. An area
        becomes a hotspot when there have been <strong>three or more reports inside roughly a one-kilometre cell in the last
        180 days</strong>, and the warning circle is 1.2&nbsp;km across.</p>
        <p>In practice that means you get a notification as you drive into an area with a genuine recent pattern &mdash; a
        station car park with repeated break-ins, a stretch of road with repeated collisions &mdash; rather than a generic
        &ldquo;this suburb scores 6 out of 10&rdquo; rating. There is no suburb score in Spotter, because a single number across
        a whole postcode tells you nothing useful about the street you are standing on.</p>

        <h2>Family safety across a city this size</h2>
        <p>Melbourne is roughly 10,000&nbsp;km&sup2;, and a lot of households are spread across it &mdash; school in one suburb,
        work in another, grandparents half an hour away. Spotter&rsquo;s Family Map handles the ordinary version of that:</p>
        <ul>
            <li>Saved places for <strong>Home, School and Work</strong>, with an arrival notice when someone gets there &mdash; the
            &ldquo;text me when you land&rdquo; message nobody remembers to send.</li>
            <li>Mutual approval on every connection. Nobody can add you without your consent, and you can switch to an
            approximate suburb-level position or pause sharing entirely at any time.</li>
            <li>Removing a connection takes effect immediately and is <strong>not announced</strong> to the person removed, so
            leaving a circle quietly does not tip anyone off.</li>
        </ul>

        <h2>Your part of Melbourne</h2>
        <p>Melbourne covers close to 10,000&nbsp;km&sup2; and the picture is genuinely different
        across it &mdash; industrial land in the south east and west, the bushfire interface in the
        outer north and the Dandenong Ranges, coastal flooding along the bay, high-rise structure
        fires in the inner city. These pages cover what recurs where:</p>
        <ul>
REGION_LINKS
        </ul>

        <h2>Stolen cars and missing persons</h2>
        <p>Spotter also checks Victoria&rsquo;s stolen property register, so you can look up a plate before buying a used car,
        and it can match a photo against public missing-persons and wanted lists. That matching runs
        <strong>entirely on your device</strong> &mdash; the photo is never uploaded &mdash; and only against closed, named lists. It
        is not a search-anyone tool, and it is not pointed at social media.</p>
"""

VICTORIA_BODY = """        <h2>Where Victoria&rsquo;s official alerts come from</h2>
        <p>Victoria publishes a live incident feed through
        <a href="https://www.emergency.vic.gov.au/respond/" target="_blank" rel="noopener noreferrer">VicEmergency</a>, covering
        Fire Rescue Victoria, the CFA, VICSES and Ambulance Victoria responses. Spotter reads that feed directly and turns
        each incident into a card on your home screen.</p>
        <p>The raw feed is noisier than most people expect. About 98% of entries carry an operational status &mdash;
        &ldquo;Responding&rdquo;, &ldquo;Going&rdquo;, &ldquo;Under control&rdquo; &mdash; and many carry a size field reading
        <code>SMALL</code> or <code>0 ha</code>. Spotter hides those, because a card that says &ldquo;0 ha&rdquo; reads as if nothing
        happened. What is left is the warning level, the incident type, how far it is from you, and how fresh it is.</p>

        <h2>Should you use this instead of the VicEmergency app?</h2>
        <p>No &mdash; and we say so inside the app. VicEmergency is the official channel, it carries the formal
        Advice / Watch and Act / Emergency Warning levels, and during a bushfire it is the source of record. Keep it
        installed.</p>
        <p>What Spotter adds is everything official feeds do not do:</p>
        <ul>
            <li><strong>Several sources in one place.</strong> VicEmergency incidents, the stolen vehicle register and public
            missing-persons lists, instead of three separate apps.</li>
            <li><strong>Your family&rsquo;s position against the incident.</strong> An official alert tells you a fire is at a
            street address. Spotter tells you that your daughter is 450&nbsp;m from it.</li>
            <li><strong>A warning before you drive in</strong>, via Risk Radar&rsquo;s repeat-incident areas.</li>
            <li><strong>An &ldquo;I&rsquo;m OK&rdquo; message</strong> on any live incident within 10&nbsp;km, which tells your circle you are
            fine without sending them your location. The server writes the message from its own copy of the alert, so no
            text from your phone reaches your family.</li>
        </ul>

        <h2>Coverage across the state, and beyond it</h2>
        <p>Victoria has Spotter&rsquo;s deepest coverage, because VicEmergency publishes the full range of incident types &mdash;
        structure fires, rescues, hazardous material incidents, flooding and grass fires. That applies across Greater
        Melbourne and regional Victoria: Geelong, Ballarat, Bendigo, the Latrobe Valley, Shepparton, Mildura and the towns
        between them.</p>
        <p>Spotter also imports two other states&rsquo; official feeds, checked every five minutes:</p>
        <ul>
            <li><strong>New South Wales</strong> &mdash; major incidents from the
            <a href="https://www.rfs.nsw.gov.au/fire-information/fires-near-me" target="_blank" rel="noopener noreferrer">NSW Rural Fire Service</a>.</li>
            <li><strong>Queensland</strong> &mdash; bushfire alerts from the Queensland Fire Department.</li>
        </ul>
        <p>Those two are fire-focused feeds, so outside Victoria you get major fire and bushfire warnings rather than the
        full incident mix. Each alert carries its source agency on the detail screen, as those feeds&rsquo; licences require.
        Community reports and all the family features work anywhere in Australia.</p>
        <p>We would rather set that out precisely than claim uniform national coverage.</p>

        <h2>Bushfire season</h2>
        <p>Through a Victorian summer the feed gets busy, and distance is what makes it usable. Spotter shows the nearest
        live incident within 10&nbsp;km on the home headline, and keeps the full history so you can see what has been running
        near a saved place over the past days rather than only what is on screen right now.</p>
        <p>Area Insights draws the same data as a heat map, which is the honest way to look at a pattern over time &mdash; it
        shows where reports have clustered, without pretending to predict where the next one will be.</p>
"""

MELTON_BODY = """        <h2>What the data can and cannot tell you</h2>
        <p>&ldquo;Is Melton safe?&rdquo; is usually answered online with a suburb score out of ten, pulled from old crime
        statistics across a whole postcode. Melton is about 36&nbsp;km north-west of the Melbourne CBD and covers a large,
        mixed area &mdash; a single number across it tells you very little about one street at one time of day.</p>
        <p>Spotter deliberately does not publish a suburb safety score. What it shows instead is specific and current:</p>
        <ul>
            <li><strong>Live incidents near you</strong>, from Victoria&rsquo;s official VicEmergency feed &mdash; structure fires,
            rescues, hazardous material incidents, flooding &mdash; ordered by distance.</li>
            <li><strong>Repeat-incident areas</strong>, where three or more reports have landed inside roughly a
            one-kilometre cell in the past 180 days. Those are the places worth knowing about, and they are far more
            local than a suburb.</li>
            <li><strong>An incident heat map</strong> in Area Insights, so you can see where reports have actually clustered
            around Melton, Melton South, Melton West, Kurunjang and Brookfield.</li>
        </ul>

        <div class="callout">
            <p><strong>If you are deciding whether to move here</strong>, the useful version of this question is street-level
            and time-of-day specific. Install Spotter, save the address you are considering as a place, and watch what
            comes through for a couple of weeks. That is real local data about the actual location, not a postcode average.</p>
        </div>

        <h2>Melton to the city</h2>
        <p>A lot of Melton households commute &mdash; the train line into Southern Cross, or the Western Freeway. Two features
        exist for exactly that gap between home and work:</p>
        <ul>
            <li><strong>Arrival notices</strong> for Home, School and Work. You get a notification when your kids reach
            school and when your partner gets home, without anyone having to remember to message.</li>
            <li><strong>Risk Radar on the drive.</strong> Warnings fire as you enter a repeat-incident area, with the app
            closed, using the phone&rsquo;s region monitoring &mdash; including station car parks with repeated reports.</li>
        </ul>

        <h2>Growth areas and new estates</h2>
        <p>Melton is one of Victoria&rsquo;s fastest-growing council areas, and new estates are where local knowledge is
        thinnest: there is no established street network of neighbours, and official statistics lag the build by years.
        That is the case where a live feed plus community reports is worth more than a historical score &mdash; the data about
        a three-year-old estate mostly does not exist yet.</p>
"""

PAGES = [
    {
        "slug": "melbourne-safety-app.html",
        "title": "Safety App for Melbourne | Live Crime & Emergency Alerts | Spotter",
        "description": "Free safety app for Melbourne: live VicEmergency incident alerts near you, Risk Radar warnings before you enter a repeat-incident area, and family arrival notices.",
        "placename": "Melbourne, Victoria, Australia",
        "breadcrumb": "Melbourne",
        "h1": 'Safety alerts for <span class="gradient-text-primary">Melbourne</span>',
        "lede": "Live incidents from Victoria&rsquo;s official emergency feed, a warning before you drive into a repeat-incident area, and your family&rsquo;s position against whatever is happening &mdash; in one free app.",
        "body": MELBOURNE_BODY + OFFICIAL_NOTE,
        "about": {"@type": "City", "name": "Melbourne", "containedInPlace": {"@type": "State", "name": "Victoria"}},
    },
    {
        "slug": "victoria-emergency-alerts.html",
        "title": "Victoria Emergency Alerts on Your Phone | Spotter",
        "description": "Get Victoria's VicEmergency incident alerts on your phone, ranked by distance to you and your family, plus NSW and Queensland fire feeds. Free on iOS and Android.",
        "placename": "Victoria, Australia",
        "breadcrumb": "Victoria",
        "h1": 'Victoria emergency alerts, <span class="gradient-text-primary">on your phone</span>',
        "lede": "Spotter reads Victoria&rsquo;s official incident feed and shows what is live near you and near your family &mdash; across Greater Melbourne and regional Victoria.",
        "body": VICTORIA_BODY + OFFICIAL_NOTE,
        "about": {"@type": "State", "name": "Victoria", "containedInPlace": {"@type": "Country", "name": "Australia"}},
    },
    {
        "slug": "melton-safety.html",
        "title": "Is Melton Safe? Live Local Alerts for Melton, VIC | Spotter",
        "description": "Live safety alerts for Melton, Victoria: official VicEmergency incidents near you, repeat-incident areas from the last 180 days, and a local incident heat map.",
        "placename": "Melton, Victoria, Australia",
        "breadcrumb": "Melton, VIC",
        "h1": 'Safety in <span class="gradient-text-primary">Melton, Victoria</span>',
        "lede": "No suburb score out of ten. Live official incidents near you, the repeat-incident areas around Melton, and a heat map of where reports have actually clustered.",
        "body": MELTON_BODY + OFFICIAL_NOTE,
        "about": {"@type": "Place", "name": "Melton", "address": {"@type": "PostalAddress", "addressLocality": "Melton", "addressRegion": "VIC", "postalCode": "3337", "addressCountry": "AU"}},
    },
]



def region_body(r):
    """Assembles a region page from that region's own blocks."""
    suburbs = ", ".join(r["suburbs"][:-1]) + " and " + r["suburbs"][-1]
    return """        <h2>What Spotter covers in %(name)s</h2>
        <p>%(geography)s</p>
        <p>Spotter reads Victoria&rsquo;s official incident feed &mdash; the same
        <a href="https://www.emergency.vic.gov.au/respond/" target="_blank" rel="noopener noreferrer">VicEmergency</a>
        data behind the state&rsquo;s warnings &mdash; and shows what is live near you across %(councils)s,
        including %(suburbs)s.</p>

        <h2>The incidents that actually recur here</h2>
        <p>%(hazard)s</p>
        <p>Spotter orders all of it by distance rather than by when it was filed, and hides the
        operational-status and &ldquo;0 ha&rdquo; noise that makes the raw feed hard to read. When nothing is
        live nearby it says &ldquo;Nothing reported near you&rdquo; &mdash; never that you are safe.</p>

        <h2>Getting around %(short)s</h2>
        <p>%(commute)s</p>

        <h2>%(angle_heading)s</h2>
        <p>%(angle_body)s</p>

        <h2>Risk Radar</h2>
        <p>An area becomes a hotspot when <strong>three or more reports land inside roughly a
        one-kilometre cell within 180 days</strong>, and the warning circle is 1.2&nbsp;km across. Spotter
        watches the 20 nearest of those using the phone&rsquo;s own region monitoring, so warnings arrive
        with the app closed. There is no suburb score anywhere in Spotter: a single number across a
        whole postcode tells you nothing useful about the street you are on.</p>
""" % {
        "name": r["name"], "short": r["short"], "geography": r["geography"],
        "councils": r["councils"], "suburbs": suburbs, "hazard": r["hazard"],
        "commute": r["commute"], "angle_heading": r["angle"]["heading"],
        "angle_body": r["angle"]["body"],
    }


for _r in REGIONS:
    PAGES.append({
        "slug": _r["slug"],
        "title": _r["title"],
        "description": _r["description"],
        "placename": "%s, Victoria, Australia" % _r["name"],
        "breadcrumb": _r["short"],
        "h1": 'Safety alerts for <span class="gradient-text-primary">%s</span>' % _r["name"],
        "lede": "Live incidents from Victoria&rsquo;s official emergency feed across %s, a warning before you enter a repeat-incident area, and your family&rsquo;s position against whatever is happening." % _r["councils"],
        "body": region_body(_r) + OFFICIAL_NOTE,
        "about": {
            "@type": "Place",
            "name": _r["name"],
            "containedInPlace": {"@type": "City", "name": "Melbourne",
                                 "containedInPlace": {"@type": "State", "name": "Victoria"}},
        },
    })


def schema_for(page):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["title"],
        "description": page["description"],
        "url": "%s/%s" % (SITE, page["slug"]),
        "inLanguage": "en-AU",
        "about": page["about"],
        "isPartOf": {"@type": "WebSite", "name": "Spotter", "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "Mynetra Pty Ltd",
            "url": SITE + "/mynetra.html",
        },
        "mainEntity": {
            "@type": "MobileApplication",
            "name": "Spotter",
            "alternateName": "SpotterApp",
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "iOS, Android",
            "url": SITE + "/",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AUD"},
        },
    }


def related_for(slug):
    """Hub pages first, then up to four siblings, rotated so every page is linked
    from somewhere. A block of identical links on every page is its own smell."""
    out = ['                <li><a href="/">Spotter &mdash; smart community safety</a></li>']
    for hub in ("melbourne-safety-app.html", "victoria-emergency-alerts.html"):
        if hub != slug:
            p = next(x for x in PAGES if x["slug"] == hub)
            out.append('                <li><a href="%s">%s</a></li>' % (p["slug"], p["title"].split(" | ")[0]))
    others = [p for p in PAGES if p["slug"] not in (slug, "melbourne-safety-app.html", "victoria-emergency-alerts.html")]
    start = [p["slug"] for p in PAGES].index(slug)
    for p in [others[(start + i) % len(others)] for i in range(min(4, len(others)))]:
        out.append('                <li><a href="%s">%s</a></li>' % (p["slug"], p["title"].split(" | ")[0]))
    return "\n".join(out)


STATIC_URLS = [
    ("", "weekly", "1.0"),
    ("mynetra.html", "yearly", "0.4"),
    ("privacy-policy.html", "yearly", "0.3"),
    ("terms-of-service.html", "yearly", "0.3"),
]


def write_sitemap(here, today):
    rows = []
    for slug, freq, pri in STATIC_URLS:
        rows.append((slug, freq, pri))
    for p in PAGES:
        rows.append((p["slug"], "monthly", "0.9" if "melbourne-safety-app" in p["slug"] or "victoria" in p["slug"] else "0.8"))
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, freq, pri in rows:
        out.append("  <url>")
        out.append("    <loc>%s/%s</loc>" % (SITE, slug))
        out.append("    <lastmod>%s</lastmod>" % today)
        out.append("    <changefreq>%s</changefreq>" % freq)
        out.append("    <priority>%s</priority>" % pri)
        out.append("  </url>")
    out.append("</urlset>")
    io.open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("wrote sitemap.xml (%d urls)" % len(rows))


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for page in PAGES:
        body = page["body"]
        if "REGION_LINKS" in body:
            body = body.replace("REGION_LINKS", "\n".join(
                '            <li><a href="%s"><strong>%s</strong></a> &mdash; %s</li>'
                % (r["slug"], r["name"], ", ".join(r["suburbs"][:5]) + " and more")
                for r in REGIONS))
            page = dict(page, body=body)
        html = TEMPLATE.format(
            site=SITE,
            ios=IOS,
            play=PLAY,
            schema=json.dumps(schema_for(page), indent=2),
            related=related_for(page["slug"]),
            **{k: page[k] for k in ("slug", "title", "description", "placename", "breadcrumb", "h1", "lede", "body")}
        )
        path = os.path.join(here, page["slug"])
        io.open(path, "w", encoding="utf-8").write(html)
        print("wrote %s (%d bytes)" % (page["slug"], len(html)))
    write_sitemap(here, "2026-10-30")


if __name__ == "__main__":
    main()
