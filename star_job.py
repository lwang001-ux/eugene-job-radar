import json

STAR_FILE = "starred_jobs.json"

def star(job):

    try:
        with open(STAR_FILE,"r") as f:
            stars = json.load(f)
    except:
        stars = []

    stars.append(job)

    with open(STAR_FILE,"w") as f:
        json.dump(stars,f)

    print("Job starred")
