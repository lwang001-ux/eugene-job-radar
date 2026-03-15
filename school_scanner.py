import requests
from bs4 import BeautifulSoup

SCHOOLS = {

"Harvard-Westlake": "https://www.hw.com/about/employment",
"Crossroads School": "https://crossroadsschool.org/about/employment",
"Brentwood School": "https://www.brentwoodschool.org/about/employment",
"Oakwood School": "https://www.oakwoodschool.org/about/employment",
"Westridge School": "https://www.westridge.org/about/employment",
"Buckley School": "https://www.thebuckleyschool.org/about/employment",
"Archer School": "https://www.archer.org/about/employment",
"Laguna Blanca": "https://www.lagunablanca.org/about/employment",
"Sage Hill": "https://www.sageshill.org/about/employment",
"St Margaret's": "https://www.stmargarets.org/about/employment",
"La Jolla Country Day": "https://www.ljcds.org/about/employment",
"Sequoyah School": "https://sequoyahschool.org/about/employment",
"Wildwood School": "https://www.wildwood.org/about/employment",
"New Roads School": "https://www.newroads.org/about/employment",
"Polytechnic School": "https://www.polytechnic.org/about/employment",
"Viewpoint School": "https://www.viewpoint.org/about/employment",
"Chadwick School": "https://www.chadwickschool.org/about/employment",
"High Tech High": "https://www.hightechhigh.org/about/employment"

}

def scan():

    jobs = []

    for school, url in SCHOOLS.items():

        try:

            r = requests.get(url, timeout=10)

            if r.status_code == 200:

                jobs.append({
                    "title":"Check Employment Page",
                    "company":school,
                    "location":"Southern California",
                    "link":url
                })

        except:
            pass

    return jobs

if __name__ == "__main__":

    jobs = scan()

    print("Schools checked:", len(jobs))

    for j in jobs:
        print(j["company"], j["link"])
