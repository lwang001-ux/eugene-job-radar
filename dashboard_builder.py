import json
import os

JOBS_FILE = "dashboard_jobs.json"

def build_dashboard(jobs):

    html = """
    <html>
    <head>
    <title>Southern California Creative + Maker Job Radar</title>
    <style>
    body{font-family:Arial;margin:40px;background:#f4f4f4}
    h1{color:#222}
    .job{background:white;padding:15px;margin-bottom:15px;border-radius:8px}
    a{color:#1a73e8;text-decoration:none}
    </style>
    </head>
    <body>
    """

    html += "<h1>Southern California Creative + Maker Job Radar</h1>"

    if not jobs:
        html += "<p>No jobs found yet.</p>"

    for j in jobs:
        html += f"""
        <div class='job'>
        <b>{j.get('title','')}</b><br>
        {j.get('company','')}<br>
        {j.get('location','')}<br>
        <a href="{j.get('link','')}">View Job</a>
        <br><br>
        ⭐ Save | Generate Cover Letter
        </div>
        """

    html += "</body></html>"

    with open("index.html","w") as f:
        f.write(html)

    print("Dashboard updated")

if __name__ == "__main__":

    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE,"r") as f:
            jobs = json.load(f)
    else:
        jobs = []

    build_dashboard(jobs)
