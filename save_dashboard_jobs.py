import json

def save_jobs(jobs):
    with open("dashboard_jobs.json","w") as f:
        json.dump(jobs,f)
