from abc import *


class AbstractSite(metaclass=ABCMeta):

    search_str = "검색어"
    terms = '검색어 리스트'
    results = '결과 리스트'

    def __init__(self, search_str):
        self.search_str = search_str
        self.results = []
        self.terms = []

    def string2list(self):
        for s in self.search_str.strip().split(','):
            self.terms.append(s)

    @abstractmethod
    def extract(self):
        """
        Crawling
        :return: self.results
        """
        return self.results
