from save_dashboard_jobs import save_jobs
from dashboard_builder import build_dashboard
import os
import requests
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = [x.strip() for x in os.getenv("EMAIL_TO").split(",")]

CREATIVE_QUERIES = [

"graphic designer los angeles",
"creative director los angeles",
"communications designer los angeles",
"graphic designer orange county",
"creative director orange county",
"graphic designer san diego"

]

MAKER_QUERIES = [

"makerspace educator los angeles",
"makerspace coordinator los angeles",
"innovation lab teacher los angeles",
"steam teacher elementary school california",
"steam teacher middle school california",
"maker educator museum california"

]

SCHOOL_QUERIES = [

"lower school design teacher california",
"middle school design teacher california",
"lower school art teacher california",
"middle school art teacher california",

"site:crossroadsschool.org jobs",
"site:hw.com employment",
"site:brentwoodschool.org jobs",
"site:polytechnic.org employment",
"site:oakwoodschool.org employment",
"site:westridge.org employment",
"site:thebuckleyschool.org employment",
"site:archer.org employment",
"site:lagunablanca.org employment",
"site:cateschool.net employment",
"site:flintridgeprep.org employment"

]

MUSEUM_QUERIES = [

"site:getty.edu jobs educator",
"site:lacma.org jobs educator",
"site:californiasciencecenter.org jobs educator",
"site:kidspacemuseum.org jobs educator",
"site:discoverycube.org jobs educator"

]

def search_google_jobs(query):

    params = {
        "engine": "google_jobs", "hl": "en", "gl": "us", "location": "California, United States",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    r = requests.get("https://serpapi.com/search", params=params)
    data = r.json()

    jobs = data.get("jobs_results", [])

    results = []

    for job in jobs[:3]:

        results.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "link": job.get("share_link")
        })

    return results


def run_queries(query_list):

    results = []

    for q in query_list:

        print("Searching:", q)

        try:

            results.extend(search_google_jobs(q))

        except Exception as e:

            print("Error:", e)

    return results


def format_section(title, jobs):

    html = f"<h2>{title}</h2>"

    if not jobs:

        html += "<p>No jobs today.</p>"

    for j in jobs:

        html += f"""
        <div style='margin-bottom:15px'>
        <b>{j['title']}</b><br>
        {j['company']}<br>
        {j['location']}<br>
        <a href='{j['link']}'>View Job</a>
        </div>
        """

    return html


def send_email(creative, maker, school, museum):

    html = "<html><body>"

    html += format_section("Creative Design Jobs", creative)
    html += format_section("Maker / STEAM Education", maker)
    html += format_section("Lower & Middle School Teaching", school)
    html += format_section("Museums & Maker Programs", museum)

    html += "</body></html>"

    msg = MIMEText(html, "html")
    body = "\nLive Job Dashboard:\nhttps://lwang001-ux.github.io/eugene-job-radar/\n\n" + body

    msg["Subject"] = "Southern California Creative + Maker Jobs"
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

    server.quit()


if __name__ == "__main__":

    print("Starting job search...")

    creative = run_queries(CREATIVE_QUERIES)

    maker = run_queries(MAKER_QUERIES)

    school = run_queries(SCHOOL_QUERIES)

    museum = run_queries(MUSEUM_QUERIES)

    all_jobs = creative + maker + school + museum
    save_jobs(all_jobs)
    build_dashboard(all_jobs)

    print("Sending email...")

    send_email(creative, maker, school, museum)

    print("Done!")


LINKEDIN_INDEED_QUERIES = [

"site:linkedin.com/jobs graphic designer los angeles",
"site:linkedin.com/jobs creative director los angeles",
"site:linkedin.com/jobs makerspace educator california",
"site:linkedin.com/jobs steam teacher california",
"site:linkedin.com/jobs design teacher middle school california",

"site:indeed.com graphic designer los angeles",
"site:indeed.com creative director los angeles",
"site:indeed.com makerspace educator california",
"site:indeed.com steam teacher california",
"site:indeed.com design teacher middle school california"

]

print("LinkedIn and Indeed searches added")


INDEPENDENT_SCHOOL_QUERIES = [

# LOS ANGELES INDEPENDENT SCHOOLS
"site:hw.com employment teacher",
"site:crossroadsschool.org employment teacher",
"site:brentwoodschool.org employment teacher",
"site:oakwoodschool.org employment teacher",
"site:westridge.org employment teacher",
"site:thebuckleyschool.org employment teacher",
"site:archer.org employment teacher",

# ORANGE COUNTY INDEPENDENT SCHOOLS
"site:lagunablanca.org employment teacher",
"site:stmargarets.org employment teacher",
"site:sageshill.org employment teacher",
"site:fairmontschools.com employment teacher",

# SAN DIEGO INDEPENDENT SCHOOLS
"site:cateschool.net employment teacher",
"site:flintridgeprep.org employment teacher",
"site:bishops.com employment teacher",
"site:ljcds.org employment teacher"

]

print("Independent school searches added")


def score_job(job):

    score = 0

    title = str(job.get("title","")).lower()
    company = str(job.get("company","")).lower()

    # BEST MATCHES
    if "makerspace" in title:
        score += 10

    if "innovation" in title:
        score += 9

    if "design teacher" in title:
        score += 9

    if "steam" in title:
        score += 8

    if "maker" in title:
        score += 8

    # LOWER / MIDDLE SCHOOL
    if "middle school" in title:
        score += 7

    if "elementary" in title:
        score += 7

    if "lower school" in title:
        score += 7

    # CREATIVE ROLES
    if "creative director" in title:
        score += 6

    if "graphic designer" in title:
        score += 5

    if "communications designer" in title:
        score += 5

    # EDUCATION ORGANIZATIONS
    if "school" in company:
        score += 3

    if "academy" in company:
        score += 3

    return score


def rank_jobs(jobs):

    for j in jobs:
        j["score"] = score_job(j)

    return sorted(jobs, key=lambda x: x["score"], reverse=True)

print("Smart job ranking enabled")


EXPANDED_QUERIES = [

# NATIONAL SCHOOL JOB BOARDS
"site:nais.org jobs teacher california",
"site:carneysandoe.com jobs teacher california",
"site:indeed.com independent school teacher california",
"site:linkedin.com jobs independent school teacher california",

# MAKER / STEAM PROGRAMS
"makerspace coordinator school california",
"innovation lab director school california",
"maker educator nonprofit california",
"steam program coordinator california",
"design lab educator california",

# MUSEUM EDUCATION JOBS
"museum educator california maker",
"children's museum educator california",
"science center educator california",
"museum steam educator california",

# MAJOR MUSEUMS
"site:getty.edu jobs educator",
"site:lacma.org jobs educator",
"site:californiasciencecenter.org jobs educator",
"site:kidspacemuseum.org jobs educator",
"site:discoverycube.org jobs educator",

# MAKER NONPROFITS
"maker educator nonprofit",
"maker lab educator california",
"fab lab educator california",
"innovation lab school california",

# DESIGN EDUCATION ROLES
"design educator nonprofit california",
"creative educator california",
"graphic design educator california",

# CHILDREN'S SCIENCE CENTERS
"children science museum educator california",
"stem education coordinator museum california",

# PRIVATE SCHOOL CONSORTIUMS
"site:nais.org california design teacher",
"site:nais.org california makerspace",
"site:nais.org california steam teacher",

# EDUCATION DESIGN ORGANIZATIONS
"design thinking educator california",
"innovation education coordinator california",
"project based learning teacher california"

]

print("Expanded job sources enabled")


def top_matches(jobs):

    scored = []

    for j in jobs:

        title = str(j.get("title","")).lower()

        score = 0

        if "makerspace" in title:
            score += 10

        if "innovation" in title:
            score += 9

        if "design teacher" in title:
            score += 9

        if "steam" in title:
            score += 8

        if "maker" in title:
            score += 8

        if "middle school" in title:
            score += 7

        if "elementary" in title:
            score += 7

        if "lower school" in title:
            score += 7

        scored.append((score,j))

    scored.sort(reverse=True)

    return [x[1] for x in scored[:5]]


def build_top_section(jobs):

    best = top_matches(jobs)

    html = "<h1>⭐ Top 5 Best Matches</h1>"

    for j in best:

        html += f"""
        <div style='margin-bottom:20px;padding:10px;border:2px solid #4CAF50'>
        <b>{j['title']}</b><br>
        {j['company']}<br>
        {j['location']}<br>
        <a href='{j['link']}'>View Job</a>
        </div>
        """

    return html

print("Top job match highlighting enabled")


SOUTHERN_CALIFORNIA_SCHOOL_QUERIES = [

# LOS ANGELES INDEPENDENT SCHOOLS
"site:hw.com employment",
"site:crossroadsschool.org employment",
"site:brentwoodschool.org employment",
"site:oakwoodschool.org employment",
"site:westridge.org employment",
"site:thebuckleyschool.org employment",
"site:archer.org employment",

# ORANGE COUNTY INDEPENDENT SCHOOLS
"site:lagunablanca.org employment",
"site:stmargarets.org employment",
"site:sageshill.org employment",
"site:fairmontschools.com employment",

# SAN DIEGO INDEPENDENT SCHOOLS
"site:cateschool.net employment",
"site:flintridgeprep.org employment",
"site:bishops.com employment",
"site:ljcds.org employment"

]

SOUTHERN_CALIFORNIA_MUSEUM_QUERIES = [

"site:getty.edu jobs educator",
"site:lacma.org jobs educator",
"site:californiasciencecenter.org jobs educator",
"site:kidspacemuseum.org jobs educator",
"site:discoverycube.org jobs educator",
"site:exploratorium.edu jobs educator",
"site:nhm.org jobs educator"

]

print("Southern California schools and museums added")


CITY_CLUSTER_QUERIES = [

# LOS ANGELES SCHOOL CLUSTERS
"makerspace educator santa monica school",
"steam teacher santa monica school",
"design teacher santa monica school",

"makerspace educator pasadena school",
"steam teacher pasadena school",
"design teacher pasadena school",

"makerspace educator beverly hills school",
"steam teacher beverly hills school",
"design teacher beverly hills school",

"makerspace educator manhattan beach school",
"steam teacher manhattan beach school",
"design teacher manhattan beach school",

# ORANGE COUNTY CLUSTERS
"makerspace educator irvine school",
"steam teacher irvine school",
"design teacher irvine school",

"makerspace educator newport beach school",
"steam teacher newport beach school",
"design teacher newport beach school",

# SAN DIEGO CLUSTERS
"makerspace educator la jolla school",
"steam teacher la jolla school",
"design teacher la jolla school",

"makerspace educator del mar school",
"steam teacher del mar school",
"design teacher del mar school"

]

print("City cluster school searches enabled")


def build_dashboard(jobs):

    html = "<html><head><title>Job Dashboard</title></head><body>"
    html += "<h1>Creative + Maker Jobs</h1>"

    for j in jobs:

        html += f"""
        <div style='margin-bottom:20px;padding:10px;border:1px solid #ccc'>
        <b>{j.get('title')}</b><br>
        {j.get('company')}<br>
        {j.get('location')}<br>
        <a href="{j.get('link')}">View Job</a>
        </div>
        """

    html += "</body></html>"

    with open("job_dashboard.html","w") as f:
        f.write(html)

    print("Dashboard updated")


def build_dashboard(jobs):

    html = """
    <html>
    <head>
    <title>Creative + Maker Job Radar</title>
    <style>
    body{font-family:Arial;margin:40px;background:#f5f5f5}
    h1{color:#222}
    h2{margin-top:40px}
    .job{background:white;padding:15px;margin-bottom:15px;border-radius:8px}
    .top{border-left:6px solid #4CAF50}
    a{color:#1a73e8;text-decoration:none}
    </style>
    </head>
    <body>
    """

    html += "<h1>Southern California Creative + Maker Job Radar</h1>"
    html += "<p>Updated automatically by your job search bot.</p>"

    ranked = rank_jobs(jobs)

    html += "<h2>Top Matches</h2>"

    for j in ranked[:5]:

        html += f"""
        <div class='job top'>
        <b>{j.get('title')}</b><br>
        {j.get('company')}<br>
        {j.get('location')}<br>
        <a href="{j.get('link')}">View Job</a>
        </div>
        """

    html += "<h2>All Jobs Found</h2>"

    for j in ranked:

        html += f"""
        <div class='job'>
        <b>{j.get('title')}</b><br>
        {j.get('company')}<br>
        {j.get('location')}<br>
        <a href="{j.get('link')}">View Job</a>
        </div>
        """

    html += "</body></html>"

    with open("job_dashboard.html","w") as f:
        f.write(html)

    print("Dashboard updated")


import requests

DIRECT_SCHOOL_SITES = [

"https://www.hw.com/about/employment",
"https://crossroadsschool.org/about/employment",
"https://www.brentwoodschool.org/about/employment",
"https://www.oakwoodschool.org/about/employment",
"https://www.westridge.org/about/employment",
"https://www.thebuckleyschool.org/about/employment",
"https://www.archer.org/about/employment",
"https://www.lagunablanca.org/about/employment",
"https://www.stmargarets.org/about/employment",
"https://www.sageshill.org/about/employment",
"https://www.ljcds.org/about/employment"

]

def check_school_sites():

    results = []

    for site in DIRECT_SCHOOL_SITES:

        try:

            r = requests.get(site, timeout=10)

            if r.status_code == 200:

                results.append({
                    "title": "Employment Page",
                    "company": site,
                    "location": "Southern California",
                    "link": site
                })

        except:

            pass

    return results

print("Direct school scanning enabled")


PROGRESSIVE_SCHOOL_QUERIES = [

# PROGRESSIVE / DESIGN-FOCUSED SCHOOLS
"site:sequoyahschool.org employment",
"site:wildwood.org employment",
"site:newroads.org employment",
"site:polytechnic.org employment",
"site:viewpoint.org employment",
"site:chadwickschool.org employment",
"site:hightechhigh.org employment",

# INNOVATION PROGRAMS
"innovation lab teacher california independent school",
"maker lab teacher independent school california",
"design thinking teacher independent school california"

]

print("Progressive school searches enabled")

