import requests
from bs4 import BeautifulSoup
from src.AbstractSite import AbstractSite


class RemoteOk(AbstractSite):
    def extract(self):
        self.string2list()
        for term in self.terms:
            url = f"https://remoteok.com/remote-{term}-jobs"
            request = requests.get(url, headers={"User-Agent": "Kimchi"})
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, "html.parser")
                jobs = soup.find_all("tr", class_="job")
                for job in jobs:
                    company = job.find("h3", itemprop="name")
                    position = job.find("h2", itemprop="title")
                    location = job.find("div", class_="location")
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


# w = RemoteOk("python,go")
# for i in w.extract():
#     print(i)
