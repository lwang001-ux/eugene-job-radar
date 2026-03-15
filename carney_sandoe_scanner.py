import requests
from bs4 import BeautifulSoup

URL = "https://www.carneysandoe.com/find-a-position/"

def scan():

    jobs = []

    try:

        r = requests.get(URL, timeout=10)

        if r.status_code == 200:

            soup = BeautifulSoup(r.text,"html.parser")

            links = soup.find_all("a")

            for link in links:

                text = link.get_text().lower()

                if any(word in text for word in ["design","steam","innovation","maker","art"]):

                    jobs.append({
                        "title":link.get_text().strip(),
                        "company":"Carney Sandoe",
                        "location":"Various Independent Schools",
                        "link":link.get("href")
                    })

    except:
        pass

    return jobs


if __name__ == "__main__":

    jobs = scan()

    print("Relevant Carney Sandoe roles found:",len(jobs))

    for j in jobs:

        print(j["title"], j["link"])
