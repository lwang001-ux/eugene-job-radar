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
EMAIL_TO = os.getenv("EMAIL_TO")


GOOGLE_JOBS_QUERIES = [
    "graphic designer southern california",
    "creative director southern california",
    "communications designer southern california",
    "makerspace educator southern california",
    "maker educator southern california",
    "makerspace coordinator southern california",
    "steam teacher southern california",
    "design teacher southern california",
    "art teacher southern california",
    "lower school art teacher southern california",
    "middle school art teacher southern california",
    "lower school design teacher southern california",
    "middle school design teacher southern california",
    "lower school makerspace coordinator southern california",
    "middle school makerspace coordinator southern california",
    "lower school makerspace educator southern california",
    "middle school makerspace educator southern california",
    "graphic designer los angeles",
    "creative director los angeles",
    "communications designer los angeles",
    "makerspace educator los angeles",
    "steam teacher los angeles",
    "design teacher los angeles",
    "art teacher los angeles",
    "graphic designer orange county",
    "creative director orange county",
    "communications designer orange county",
    "makerspace educator orange county",
    "steam teacher orange county",
    "design teacher orange county",
    "art teacher orange county",
    "graphic designer san diego",
    "creative director san diego",
    "communications designer san diego",
    "makerspace educator san diego",
    "steam teacher san diego",
    "design teacher san diego",
    "art teacher san diego",
]

WEB_SEARCH_QUERIES = [
    'site:linkedin.com/jobs/view "graphic designer" "southern california"',
    'site:linkedin.com/jobs/view "creative director" "southern california"',
    'site:linkedin.com/jobs/view "communications designer" "southern california"',
    'site:linkedin.com/jobs/view "makerspace educator" "southern california"',
    'site:linkedin.com/jobs/view "maker educator" "southern california"',
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
    'site:edjoin.org/Home/JobPosting "makerspace" california',
    '"lower school" "art teacher" "southern california"',
    '"middle school" "art teacher" "southern california"',
    '"lower school" "design teacher" "southern california"',
    '"middle school" "design teacher" "southern california"',
    '"makerspace coordinator" "lower school" "southern california"',
    '"makerspace coordinator" "middle school" "southern california"',
]


POSITIVE_WORDS = [
    "graphic designer",
    "creative director",
    "communications designer",
    "maker educator",
    "makerspace educator",
    "makerspace coordinator",
    "steam teacher",
    "design teacher",
    "art teacher",
    "lower school",
    "middle school",
    "maker",
    "makerspace",
    "design",
    "art",
    "steam",
    "education",
    "school",
]

NEGATIVE_WORDS = [
    "dance teacher",
    "music teacher",
    "drama teacher",
    "choir",
    "theater teacher",
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
    "insurance agent",
    "substitute teacher",
    "assistant coach",
    "coach",
]

ALLOWED_SOURCES = [
    "linkedin.com",
    "indeed.com",
    "edjoin.org",
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
    print("Searching Google Jobs...")
    results = []
    seen = set()

    for q in GOOGLE_JOBS_QUERIES:
        print("Searching:", q)

        url = "https://serpapi.com/search"
        params = {
            "engine": "google_jobs",
            "q": q,
            "hl": "en",
            "api_key": SERPAPI_API_KEY
        }

        try:
            r = requests.get(url, params=params, timeout=30)
            data = r.json()
        except Exception as e:
            print("Skipping because of error:", e)
            continue

        jobs = data.get("jobs_results", [])

        for job in jobs[:3]:
            title = job.get("title", "No title")
            company = job.get("company_name", "No company")
            location = job.get("location", "No location")
            link = get_google_jobs_link(job)

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
                "link": link
            })

    return results


def search_web_results():
    print("Searching LinkedIn / Indeed / EdJoin...")
    results = []
    seen = set()

    for q in WEB_SEARCH_QUERIES:
        print("Searching:", q)

        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": q,
            "hl": "en",
            "num": 8,
            "api_key": SERPAPI_API_KEY
        }

        try:
            r = requests.get(url, params=params, timeout=30)
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

            if not any(source in link_lower for source in ALLOWED_SOURCES) and "school" not in link_lower:
                continue

            source = "Web"
            if "linkedin.com" in link_lower:
                source = "LinkedIn"
            elif "indeed.com" in link_lower:
                source = "Indeed"
            elif "edjoin.org" in link_lower:
                source = "EdJoin"
            elif "school" in link_lower or "academy" in link_lower or ".edu" in link_lower:
                source = "School Site"

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
                "snippet": snippet
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
    <h2>New Southern California Job Matches</h2>
    <p>Focused on graphic design, creative leadership, makerspace, STEAM, design, and art roles.</p>
    """

    if not jobs:
        html += "<p>No matching jobs found today.</p>"
    else:
        for job in jobs:
            title = job.get("title", "")
            company = job.get("company", "")
            location = job.get("location", "")
            link = job.get("link", "")
            source = job.get("source", "")
            snippet = job.get("snippet", "")

            link_html = f'<a href="{link}">View job posting</a>' if link else "No direct link provided"
            company_html = f'<div style="margin-bottom: 4px;">{company}</div>' if company else ""
            location_html = f'<div style="margin-bottom: 6px; color: #666;">{location}</div>' if location else ""
            snippet_html = f'<div style="margin-top: 6px; color: #555;">{snippet}</div>' if snippet else ""

            html += f"""
            <div style="margin-bottom: 18px; padding: 14px; border: 1px solid #ddd; border-radius: 8px;">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 6px;">{title}</div>
                <div style="font-size: 12px; color: #888; margin-bottom: 6px;">Source: {source}</div>
                {company_html}
                {location_html}
                <div>{link_html}</div>
                {snippet_html}
            </div>
            """

    html += """
    </body>
    </html>
    """
    return html


def send_email(jobs):
    html_body = build_html_email(jobs)

    msg = MIMEText(html_body, "html")
    msg["Subject"] = "New SoCal Design / Makerspace / STEAM Job Matches"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO.split(","), msg.as_string())
    server.quit()


if __name__ == "__main__":
    print("Starting search...")

    google_jobs = search_google_jobs()
    web_results = search_web_results()

    all_results = dedupe_results(google_jobs + web_results)

    print("Total results found:", len(all_results))
    print("Sending email...")

    send_email(all_results[:60])

    print("Done!")
