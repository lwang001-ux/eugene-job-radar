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
EMAIL_TO = [x.strip() for x in os.getenv("EMAIL_TO", "").split(",") if x.strip()]

GOOGLE_JOBS_QUERIES = [
    "graphic designer southern california",
    "creative director southern california",
    "communications designer southern california",
    "makerspace educator southern california",
    "makerspace coordinator southern california",
    "maker educator southern california",
    "steam teacher southern california",
    "design teacher southern california",
    "art teacher southern california",
    "lower school design teacher southern california",
    "middle school design teacher southern california",
    "lower school art teacher southern california",
    "middle school art teacher southern california",
    "graphic designer los angeles",
    "creative director los angeles",
    "communications designer los angeles",
    "graphic designer orange county",
    "creative director orange county",
    "graphic designer san diego",
    "creative director san diego",
]

WEB_SEARCH_QUERIES = [
    'site:linkedin.com/jobs/view "graphic designer" "southern california"',
    'site:linkedin.com/jobs/view "creative director" "southern california"',
    'site:linkedin.com/jobs/view "communications designer" "southern california"',
    'site:linkedin.com/jobs/view "makerspace educator" "southern california"',
    'site:linkedin.com/jobs/view "makerspace coordinator" "southern california"',
    'site:linkedin.com/jobs/view "steam teacher" "southern california"',
    'site:linkedin.com/jobs/view "design teacher" "southern california"',
    'site:linkedin.com/jobs/view "art teacher" "southern california"',

    'site:indeed.com/viewjob "graphic designer" "southern california"',
    'site:indeed.com/viewjob "creative director" "southern california"',
    'site:indeed.com/viewjob "communications designer" "southern california"',
    'site:indeed.com/viewjob "makerspace educator" "southern california"',
    'site:indeed.com/viewjob "makerspace coordinator" "southern california"',
    'site:indeed.com/viewjob "steam teacher" "southern california"',
    'site:indeed.com/viewjob "design teacher" "southern california"',
    'site:indeed.com/viewjob "art teacher" "southern california"',

    'site:edjoin.org/Home/JobPosting "steam teacher" california',
    'site:edjoin.org/Home/JobPosting "design teacher" california',
    'site:edjoin.org/Home/JobPosting "art teacher" california',
    'site:edjoin.org/Home/JobPosting makerspace california',

    '"lower school" "design teacher" "southern california" site:org',
    '"middle school" "design teacher" "southern california" site:org',
    '"lower school" "art teacher" "southern california" site:org',
    '"middle school" "art teacher" "southern california" site:org',
    '"makerspace coordinator" school "southern california"',
    '"makerspace educator" school "southern california"',
    '"maker educator" museum "southern california"',
]

POSITIVE_WORDS = [
    "graphic designer",
    "creative director",
    "communications designer",
    "makerspace educator",
    "makerspace coordinator",
    "maker educator",
    "steam teacher",
    "design teacher",
    "art teacher",
    "lower school",
    "middle school",
    "makerspace",
]

NEGATIVE_WORDS = [
    "dance teacher",
    "music teacher",
    "drama teacher",
    "choir",
    "theater",
    "coach",
    "assistant coach",
    "substitute teacher",
    "software engineer",
    "nurse",
    "custodian",
    "janitor",
    "accountant",
    "warehouse",
    "medical assistant",
    "security guard",
    "real estate",
    "delivery driver",
    "cashier",
]

def looks_relevant(text):
    text = (text or "").lower()
    if any(bad in text for bad in NEGATIVE_WORDS):
        return False
    return any(good in text for good in POSITIVE_WORDS)

def get_google_jobs_link(job):
    if job.get("share_link"):
        return job["share_link"]
    links = job.get("related_links", [])
    if links and isinstance(links, list):
        first = links[0]
        if isinstance(first, dict):
            return first.get("link", "")
    return ""

def search_google_jobs():
    print("Weekly search: Google Jobs")
    results = []
    seen = set()

    for q in GOOGLE_JOBS_QUERIES:
        print("Searching:", q)
        params = {
            "engine": "google_jobs",
            "q": q,
            "hl": "en",
            "api_key": SERPAPI_API_KEY,
        }
        try:
            r = requests.get("https://serpapi.com/search", params=params, timeout=30)
            data = r.json()
        except Exception as e:
            print("Skipping because of error:", e)
            continue

        jobs = data.get("jobs_results", [])
        for job in jobs[:4]:
            title = job.get("title", "No title")
            company = job.get("company_name", "No company")
            location = job.get("location", "No location")
            link = get_google_jobs_link(job)
            posted = (job.get("detected_extensions") or {}).get("posted_at", "")

            combined = f"{title} {company} {location}"
            if not looks_relevant(combined):
                continue

            key = f"{title}|{company}|{location}|{link}"
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "source": "Google Jobs",
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "posted": posted,
                "snippet": "",
            })
    return results

def search_web_results():
    print("Weekly search: LinkedIn / Indeed / EdJoin / school sites")
    results = []
    seen = set()

    for q in WEB_SEARCH_QUERIES:
        print("Searching:", q)
        params = {
            "engine": "google",
            "q": q,
            "hl": "en",
            "num": 8,
            "api_key": SERPAPI_API_KEY,
        }
        try:
            r = requests.get("https://serpapi.com/search", params=params, timeout=30)
            data = r.json()
        except Exception as e:
            print("Skipping because of error:", e)
            continue

        items = data.get("organic_results", [])
        for item in items[:4]:
            title = item.get("title", "No title")
            link = item.get("link", "")
            snippet = item.get("snippet", "")

            combined = f"{title} {snippet}"
            if not looks_relevant(combined):
                continue

            link_lower = link.lower()
            if "linkedin.com" in link_lower:
                source = "LinkedIn"
            elif "indeed.com" in link_lower:
                source = "Indeed"
            elif "edjoin.org" in link_lower:
                source = "EdJoin"
            elif "museum" in link_lower:
                source = "Museum Site"
            elif "school" in link_lower or ".edu" in link_lower or "academy" in link_lower:
                source = "School Site"
            else:
                continue

            key = f"{title}|{link}"
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "source": source,
                "title": title,
                "company": "",
                "location": "",
                "link": link,
                "posted": "",
                "snippet": snippet,
            })
    return results

def dedupe_results(items):
    final = []
    seen = set()
    for item in items:
        key = f"{item.get('title', '')}|{item.get('link', '')}"
        if key in seen:
            continue
        seen.add(key)
        final.append(item)
    return final

def build_html_email(jobs):
    html = """
    <html>
    <body style="font-family: Arial, Helvetica, sans-serif; color: #222;">
    <h2>Weekly Broader Job Roundup</h2>
    <p>Graphic design, creative leadership, makerspace, STEAM, design, and art roles across Southern California.</p>
    """

    if not jobs:
        html += "<p>No matching jobs found this week.</p>"
    else:
        for job in jobs:
            title = job.get("title", "")
            company = job.get("company", "")
            location = job.get("location", "")
            link = job.get("link", "")
            source = job.get("source", "")
            posted = job.get("posted", "")
            snippet = job.get("snippet", "")

            company_html = f'<div style="margin-bottom:4px;">{company}</div>' if company else ""
            location_html = f'<div style="margin-bottom:4px;color:#666;">{location}</div>' if location else ""
            posted_html = f'<div style="margin-bottom:4px;color:#888;font-size:12px;">Posted: {posted}</div>' if posted else ""
            snippet_html = f'<div style="margin-top:6px;color:#555;">{snippet}</div>' if snippet else ""
            link_html = f'<a href="{link}">View job posting</a>' if link else "No direct link"

            html += f"""
            <div style="margin-bottom:18px;padding:14px;border:1px solid #ddd;border-radius:8px;">
                <div style="font-size:16px;font-weight:bold;margin-bottom:6px;">{title}</div>
                <div style="font-size:12px;color:#888;margin-bottom:6px;">Source: {source}</div>
                {company_html}
                {location_html}
                {posted_html}
                <div>{link_html}</div>
                {snippet_html}
            </div>
            """

    html += "</body></html>"
    return html

def send_email(jobs):
    html_body = build_html_email(jobs)

    msg = MIMEText(html_body, "html")
    msg["Subject"] = "Weekly SoCal Design / Makerspace / STEAM Roundup"
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

if __name__ == "__main__":
    print("Starting weekly search...")
    google_jobs = search_google_jobs()
    web_results = search_web_results()
    all_results = dedupe_results(google_jobs + web_results)

    print("Weekly results:", len(all_results))
    print("Sending weekly email...")
    send_email(all_results[:70])
    print("Done!")

