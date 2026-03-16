import json
import smtplib
import os
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

DASHBOARD_URL = "https://lwang001-ux.github.io/eugene-job-radar/"

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def load_jobs():
    try:
        with open("dashboard_jobs.json","r") as f:
            return json.load(f)
    except:
        return []

def send_email(jobs):

    if not jobs:
        print("No jobs to send")
        return

    html = f"""
    <p><b>Live Job Dashboard</b><br>
    <a href="{DASHBOARD_URL}">
    {DASHBOARD_URL}
    </a></p>
    """

    html += "<h3>Today's Job Listings</h3>"

    for j in jobs:
        title = j.get("title","")
        company = j.get("company","")
        location = j.get("location","")
        link = j.get("link","")

        html += f"""
        <p>
        <b>{title}</b><br>
        {company}<br>
        {location}<br>
        <a href="{link}">View Job</a>
        </p>
        """

    msg = MIMEText(html, "html")
    msg["Subject"] = "Job Bot"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)

    server.sendmail(EMAIL_FROM, EMAIL_TO.split(","), msg.as_string())

    print("Email sent")

if __name__ == "__main__":

    jobs = load_jobs()

    print("Sending email...")

    send_email(jobs)
