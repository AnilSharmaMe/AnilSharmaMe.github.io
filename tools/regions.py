# -*- coding: utf-8 -*-
"""Region definitions for the Melbourne landing pages.

One entry per region. Each carries its OWN geography, hazard profile, commute
reality and angle -- the pages are not a template with the name swapped, because
near-identical location pages are what Google's doorway-abuse and scaled-content
policies are aimed at. If a region cannot be given something genuinely its own
to say, it does not get a page.

Nothing here states a crime statistic. Claims are limited to geography, council
areas, publicly documented events, and how Spotter's own features behave.
"""

REGIONS = [
    {
        "slug": "south-east-melbourne-safety.html",
        "name": "South East Melbourne",
        "short": "South East",
        "title": "Safety Alerts for South East Melbourne | Spotter",
        "description": "Live VicEmergency alerts for south east Melbourne — Dandenong, Narre Warren, Berwick, Pakenham, Cranbourne, Clayton, Springvale and Frankston. Free app.",
        "councils": "Greater Dandenong, Casey, Cardinia, Monash, Kingston and Frankston",
        "suburbs": ["Dandenong", "Noble Park", "Springvale", "Clayton", "Oakleigh",
                    "Narre Warren", "Berwick", "Pakenham", "Officer", "Cranbourne",
                    "Hampton Park", "Endeavour Hills", "Frankston", "Carrum Downs",
                    "Keysborough", "Mulgrave"],
        "geography": """South east Melbourne is the largest slice of the city by population — the
        corridor running from Clayton and Oakleigh out through Dandenong, Narre Warren and
        Berwick to Pakenham and Officer, plus the Cranbourne and Frankston arms. Casey and
        Cardinia together are among the fastest-growing municipalities in the country, and
        the edge of the built-up area moves outward every year.""",
        "hazard": """The hazard profile changes as you move out. The inner part of the corridor is
        dense residential and industrial — Dandenong South is one of the largest industrial
        precincts in the state, which is why hazardous material incidents and structure fires
        show up in the feed here more than in a purely residential area. Past Pakenham and
        Officer you reach the grassland and farmland interface, where grass fires through
        summer become the dominant incident type, and the Cardinia and Bunyip catchments
        bring flood and storm warnings.""",
        "commute": """The Pakenham and Cranbourne lines and the Monash Freeway carry a very large
        number of people in and out each day, and a lot of households here have school in one
        suburb and work 40 km away. Arrival notices for Home, School and Work exist for exactly
        that — you get told when the kids reach school and when someone gets home, without
        anyone having to remember to message.""",
        "angle": {
            "heading": "Why a growth corridor is the hardest place to judge",
            "body": """Estates in Officer, Clyde North and Cranbourne East were paddocks a few years
            ago. Official crime statistics for them are thin or non-existent, the suburb has no
            long-established network of neighbours yet, and any &ldquo;safety score&rdquo; you find online
            is averaging a brand-new estate together with areas built forty years earlier.
            <br><br>That is the case where a live feed is worth more than a historical score. Save
            the address as a place in Spotter and you see what actually comes through for it,
            rather than a number derived from data that predates the street.""",
        },
    },
    {
        "slug": "western-suburbs-melbourne-safety.html",
        "name": "Melbourne's Western Suburbs",
        "short": "West",
        "title": "Safety Alerts for Melbourne's Western Suburbs | Spotter",
        "description": "Live VicEmergency alerts for Melbourne's west — Footscray, Sunshine, Werribee, Tarneit, Point Cook, Caroline Springs, Melton and Wyndham Vale. Free app.",
        "councils": "Wyndham, Brimbank, Melton, Maribyrnong and Hobsons Bay",
        "suburbs": ["Footscray", "Sunshine", "Altona", "Williamstown", "Yarraville",
                    "Werribee", "Tarneit", "Point Cook", "Hoppers Crossing", "Truganina",
                    "Caroline Springs", "Melton", "Wyndham Vale", "Deer Park", "Laverton"],
        "geography": """The west runs from Footscray and Yarraville, a few kilometres from the CBD,
        out through Sunshine and Deer Park to Melton, and down the Princes Freeway through
        Werribee, Tarneit and Point Cook. Wyndham has been one of the fastest-growing councils
        in Australia for most of the last decade.""",
        "hazard": """Two things shape the feed here. The first is industry and freight — the Port of
        Melbourne, the West Gate corridor, and the industrial belt through Laverton North and
        Truganina mean hazardous material incidents and large structure fires appear more often
        than the residential population alone would suggest. The second is water: the
        Maribyrnong River flooded homes in Maribyrnong and Ascot Vale in October 2022, and the
        Werribee River catchment carries its own flood and storm warnings.""",
        "commute": """A lot of the west commutes across the West Gate or on the Werribee and Sunbury
        lines, and a single incident on either can strand tens of thousands of people. Spotter
        will not tell you the bridge is closed — that is not an emergency feed — but it will tell
        you if a live incident is near someone you care about while they are out in it.""",
        "angle": {
            "heading": "Flooding is the one people underestimate",
            "body": """Fire gets the attention in Victoria, but the west&rsquo;s most expensive recent
            emergency was water. Flood is slower than fire, which sounds reassuring and is not —
            slow means people keep driving into it.
            <br><br>Spotter carries VICSES flood and storm warnings from the same official feed as
            everything else, ordered by distance from you, and Risk Radar&rsquo;s repeat-incident areas
            pick up the stretches of road where reports keep landing.""",
        },
    },
    {
        "slug": "northern-suburbs-melbourne-safety.html",
        "name": "Melbourne's Northern Suburbs",
        "short": "North",
        "title": "Safety Alerts for Melbourne's Northern Suburbs | Spotter",
        "description": "Live VicEmergency alerts for Melbourne's north — Preston, Reservoir, Epping, Craigieburn, Mill Park, Broadmeadows, Sunbury and Whittlesea. Free app.",
        "councils": "Hume, Whittlesea, Darebin, Moreland (Merri-bek), Banyule and Nillumbik",
        "suburbs": ["Preston", "Reservoir", "Coburg", "Brunswick", "Thomastown",
                    "Epping", "Mill Park", "South Morang", "Mernda", "Craigieburn",
                    "Roxburgh Park", "Broadmeadows", "Sunbury", "Whittlesea", "Greenvale"],
        "geography": """The north runs from Brunswick and Coburg, inner and dense, out through
        Preston, Reservoir and Thomastown to Epping, Mill Park and Mernda, with the Hume arm
        taking in Broadmeadows, Craigieburn, Roxburgh Park and Sunbury. The outer edge reaches
        genuine countryside around Whittlesea, Wallan and the Kinglake ranges.""",
        "hazard": """The north has the sharpest urban-to-bushfire transition of any part of Melbourne.
        Suburbs like Mernda, Doreen, Whittlesea and Sunbury sit at or near the bushfire interface,
        and the Kinglake ranges beyond them carry the most serious fire history in the state.
        Closer in, around Broadmeadows and Campbellfield, industrial land again means structure
        fires and hazardous material incidents in the feed.""",
        "commute": """The Hume Freeway, the Craigieburn and Mernda lines and the Ring Road carry the
        north&rsquo;s traffic, and plenty of households run between an outer estate and an inner
        workplace daily. Risk Radar fires as you enter a repeat-incident area with the app closed,
        using the phone&rsquo;s own region monitoring, so it costs almost nothing in battery.""",
        "angle": {
            "heading": "Living at the bushfire interface",
            "body": """If you are in Mernda, Doreen, Whittlesea, Sunbury or the Kinglake side, your
            summer is different from someone in Brunswick. The official VicEmergency warning levels —
            Advice, Watch and Act, Emergency Warning — are the source of record, and you should have
            the VicEmergency app for them. Spotter does not replace it.
            <br><br>What Spotter adds on those days is your people. If someone in your circle is
            within 1 km of a live incident, that becomes the top card with a one-tap
            &ldquo;Are you OK?&rdquo; message, and the reply reaches you without them having to find
            and type anything.""",
        },
    },
    {
        "slug": "eastern-suburbs-melbourne-safety.html",
        "name": "Melbourne's Eastern Suburbs",
        "short": "East",
        "title": "Safety Alerts for Melbourne's Eastern Suburbs | Spotter",
        "description": "Live VicEmergency alerts for Melbourne's east — Box Hill, Doncaster, Ringwood, Glen Waverley, Croydon, Lilydale and the Dandenong Ranges. Free app.",
        "councils": "Whitehorse, Manningham, Maroondah, Knox, Monash and Yarra Ranges",
        "suburbs": ["Box Hill", "Doncaster", "Blackburn", "Nunawading", "Glen Waverley",
                    "Wantirna", "Ringwood", "Croydon", "Bayswater", "Boronia",
                    "Lilydale", "Mooroolbark", "Belgrave", "Olinda", "Healesville"],
        "geography": """The east runs from Box Hill and Doncaster through Ringwood and Croydon to
        Lilydale, then climbs into the Dandenong Ranges at Belgrave, Olinda and Sassafras and
        continues to Healesville and the Yarra Valley. The character changes completely over
        that distance — from one of Melbourne&rsquo;s densest activity centres to forested hills.""",
        "hazard": """The Dandenong Ranges are the defining risk. Heavily treed, steep, with narrow
        roads and a single way out of many streets, they produce two recurring emergency types:
        bushfire through summer, and storm damage with trees down and extended power outages
        through winter. The June 2021 storms cut power to parts of the ranges for well over a
        week. Further down, around Bayswater and Boronia, industrial land brings the usual
        structure fire and hazardous material incidents.""",
        "commute": """The Belgrave and Lilydale lines and the Eastern Freeway and EastLink carry the
        east, and many ranges households drive down the hill daily. The practical value of
        arrival notices is higher here than almost anywhere — mobile coverage in the hills is
        patchy, and &ldquo;got home fine&rdquo; is a message that often does not send.""",
        "angle": {
            "heading": "What a week without power actually needs",
            "body": """Ranges residents already know the drill: trees down, roads cut, power out for
            days. The gap in that situation is not information about the storm, it is knowing where
            everyone is and whether they got out.
            <br><br>Spotter keeps the full alert history rather than only what is live, so you can
            see what has been running near a saved place over several days. And an
            &ldquo;I&rsquo;m OK&rdquo; message to your circle sends no location at all — the server writes the
            text from its own copy of the alert — which matters when you are trying to send
            something small over a bad connection.""",
        },
    },
    {
        "slug": "inner-melbourne-safety.html",
        "name": "Inner Melbourne and the CBD",
        "short": "Inner city",
        "title": "Safety Alerts for Inner Melbourne and the CBD | Spotter",
        "description": "Live VicEmergency alerts for inner Melbourne — the CBD, Southbank, Docklands, Carlton, Fitzroy, Richmond, St Kilda and South Yarra. Free on iOS and Android.",
        "councils": "City of Melbourne, Yarra, Port Phillip and Stonnington",
        "suburbs": ["Melbourne CBD", "Southbank", "Docklands", "Carlton", "Fitzroy",
                    "Collingwood", "Richmond", "South Yarra", "Prahran", "St Kilda",
                    "Port Melbourne", "North Melbourne", "Parkville", "Brunswick East"],
        "geography": """Inner Melbourne is the CBD grid plus the ring of dense suburbs around it —
        Carlton, Fitzroy, Collingwood, Richmond, South Yarra, Prahran, St Kilda, Southbank,
        Docklands and Port Melbourne. It has the city&rsquo;s highest residential density, its highest
        proportion of apartment living, and a daytime population several times its resident one.""",
        "hazard": """High-rise living changes which incidents matter. Structure fires in apartment
        towers, lift rescues and hazardous material incidents in basement car parks are the
        recurring types here, and an incident 200 m away in a dense grid affects far more people
        than the same incident in an outer suburb. Distance is also measured differently: 500 m
        in the CBD is a different thing from 500 m in Pakenham.""",
        "commute": """Almost everyone in inner Melbourne moves on foot, by tram or by bike, often late
        at night, and a large share are students or recent arrivals without family nearby. The
        one-tap alert to your circle and the ability to share an approximate suburb-level position
        rather than an exact one were both built with that in mind.""",
        "angle": {
            "heading": "If you are new to the city",
            "body": """International students and new arrivals get the worst version of this problem:
            no local network, unfamiliar geography, and advice that is either scare stories or
            nothing at all. Spotter will not hand you a ranked list of dangerous streets, because
            that list would be mostly wrong.
            <br><br>What it does is show what is actually live near you right now, and let you
            connect a circle — including people overseas — who get told if you are near an
            incident. Every connection needs mutual approval, you can pause sharing at any time,
            and removing someone takes effect immediately without telling them.""",
        },
    },
    {
        "slug": "bayside-melbourne-safety.html",
        "name": "Bayside and South East Beachside Melbourne",
        "short": "Bayside",
        "title": "Safety Alerts for Bayside Melbourne | Spotter",
        "description": "Live VicEmergency alerts for bayside Melbourne — Brighton, Sandringham, Mentone, Mordialloc, Chelsea, Carrum and Frankston along Port Phillip Bay. Free app.",
        "councils": "Bayside, Kingston and Frankston",
        "suburbs": ["Brighton", "Hampton", "Sandringham", "Black Rock", "Beaumaris",
                    "Mentone", "Parkdale", "Mordialloc", "Aspendale", "Chelsea",
                    "Carrum", "Seaford", "Frankston", "Elwood"],
        "geography": """The bayside strip follows Port Phillip Bay from Elwood and Brighton south
        through Sandringham, Beaumaris and Mentone to Mordialloc, Chelsea, Carrum, Seaford and
        Frankston — roughly 40 km of coastline, most of it a narrow band of suburb between the
        Nepean Highway and the water.""",
        "hazard": """Being coastal changes the mix. Storm surge and coastal flooding affect the
        low-lying stretches around Elwood, Aspendale, Chelsea and Carrum — Elwood in particular
        has a long history of flash flooding. VICSES water rescues and beach incidents appear
        through summer, and the Patterson River and Mordialloc Creek catchments carry their own
        warnings.""",
        "commute": """The Frankston and Sandringham lines and the Nepean Highway run the length of the
        strip. In summer the daytime population of the beachside suburbs multiplies, which is
        exactly when families get separated — the Family Map and saved places are doing their most
        ordinary and most useful work on a crowded January afternoon.""",
        "angle": {
            "heading": "Summer, beaches and kids",
            "body": """The realistic bayside emergency is not dramatic: it is a child who wandered
            off at a packed beach, or a teenager who said they would be back by five.
            <br><br>Spotter&rsquo;s Family Map shows where your people are on one screen, and the family
            page says plainly what it knows and when it last knew it — &ldquo;Last seen 3 days ago&rdquo;
            appears quietly on that person&rsquo;s row rather than as an alarm, because a silent phone
            is usually just a flat battery. It never tells you someone is safe. It tells you what
            it knows.""",
        },
    },
]
