import requests

COMPANIES = {

"IDEO": "https://www.ideo.com/careers",
"Frog Design": "https://www.frog.co/careers",
"Gensler": "https://www.gensler.com/careers",
"Local Projects": "https://localprojects.com/careers",
"Pentagram": "https://www.pentagram.com/about/careers",
"Two Bit Circus": "https://twobitcircus.com/careers",
"Meow Wolf": "https://jobs.lever.co/meowwolf",
"Disney Imagineering": "https://jobs.disneycareers.com/",
"Nickelodeon": "https://careers.paramount.com/",
"Mattel": "https://corporate.mattel.com/careers",
"Snap Inc": "https://snap.com/jobs",
"Netflix Creative": "https://jobs.netflix.com/",
"Google Creative Lab": "https://careers.google.com/jobs/",
"Apple Design": "https://jobs.apple.com/en-us/search"
}

def scan():

    jobs = []

    for company, url in COMPANIES.items():

        try:

            r = requests.get(url, timeout=10)

            if r.status_code == 200:

                jobs.append({
                    "title":"Creative Roles – check careers page",
                    "company":company,
                    "location":"Various",
                    "link":url
                })

        except:
            pass

    return jobs


if __name__ == "__main__":

    jobs = scan()

    print("Creative companies checked:",len(jobs))

    for j in jobs:
        print(j["company"], j["link"])
