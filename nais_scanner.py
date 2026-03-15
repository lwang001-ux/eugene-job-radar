import requests
from bs4 import BeautifulSoup

URL = "https://careers.nais.org/jobs"

def scan():

    jobs = []

    try:
        r = requests.get(URL, timeout=10)

        soup = BeautifulSoup(r.text,"html.parser")

        links = soup.find_all("a")

        for link in links:

            text = link.get_text().lower()

            if any(word in text for word in ["design","steam","maker","innovation","art"]):

                jobs.append({
                    "title": link.get_text().strip(),
                    "company": "NAIS School",
                    "location": "Various",
                    "link": link.get("href")
                })

    except:
        pass

    return jobs

if __name__ == "__main__":

    jobs = scan()

    print("NAIS roles found:",len(jobs))

    for j in jobs:
        print(j["title"], j["link"])
