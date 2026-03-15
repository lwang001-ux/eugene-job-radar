import json, os

def build_dashboard(jobs):

    html = """
    <html>
    <head>
    <title>Creative + Maker Job Radar</title>
    <style>
    body{font-family:Arial;margin:40px;background:#f4f4f4}
    .job{background:white;padding:15px;margin-bottom:15px;border-radius:8px}
    h1{color:#222}
    a{color:#1a73e8;text-decoration:none}
    </style>
    </head>
    <body>
    """

    html += "<h1>Southern California Creative + Maker Job Radar</h1>"

    if not jobs:
        html += "<p>No jobs captured yet. They will appear after the next search run.</p>"

    for j in jobs:

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

    print("Dashboard written successfully")

if __name__ == "__main__":

    # simple test jobs so the dashboard always shows something
    sample = [
        {"title":"Sample Makerspace Educator","company":"Example School","location":"Los Angeles","link":"https://example.com"},
        {"title":"Sample Design Teacher","company":"Creative Academy","location":"Santa Monica","link":"https://example.com"}
    ]

    build_dashboard(sample)
