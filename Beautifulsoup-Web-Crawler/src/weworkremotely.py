import requests
from bs4 import BeautifulSoup


class WeworkRemotely:
    def __init__(self):
        self.url = "https://weworkremotely.com/remote-jobs/search?term=python"
        self.request = requests.get(self.url, headers={"User-Agent": "Kimchi"})
        self.results = []

    def extract(self):
        if self.request.status_code == 200:
            soup = BeautifulSoup(self.request.text, "html.parser")
            jobs = soup.find_all("li", class_="feature")
            for job in jobs:
                print(job)
            print(len(job))
        return 1


w = WeworkRemotely()
w.extract()
