import requests
from bs4 import BeautifulSoup
from src.AbstractSite import AbstractSite


class WeworkRemotely(AbstractSite):
    def extract(self):
        self.string2list()
        for term in self.terms:
            url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
            request = requests.get(url, headers={"User-Agent": "Kimchi"})
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, "html.parser")
                jobs = soup.find_all("li", class_="feature")
                for job in jobs:
                    company = job.find("span", class_="company")
                    position = job.find("span", class_="title")
                    location = job.find("span", class_="region")
                    if company:
                        company = company.string.strip()
                    if position:
                        position = position.string.strip()
                    if location:
                        location = location.string.strip()
                    if company and position and location:
                        job = {
                            'term': term,
                            'company': company,
                            'position': position,
                            'location': location
                        }
                        self.results.append(job)
            else:
                print("Can't get jobs.")
        return self.results


# w = WeworkRemotely("python,go")
# for i in w.extract():
#     print(i)
