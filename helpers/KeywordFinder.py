from bs4 import BeautifulSoup
import requests
from time import sleep

class KeywordFinder:
    def __init__(self) -> None:
        self.params = {
            'query': 'make wordpress',
        }

        self.mainurl = 'https://www.fiverr.com/search/gigs'
        self.href = None
        self.data = {
            "Title" : None,
            "Volume" : None
        }

        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)


    def soupify(self, x):
        return BeautifulSoup(x,'html.parser')


    def search_instead(self):
        try:
            sleep(1)
            response = self.session.get(self.mainurl + self.href, params=None)

            if response.status_code == 200:
                soup = self.soupify(response.content)
                return soup
            else:
                print(f"Failed to fetch data. Status Code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


    def search(self, query) -> None:
        self.params['query'] = query

        try:
            response = self.session.get(self.mainurl, params=self.params)

            if response.status_code == 200:
                soup = self.soupify(response.content)
                search_instead = soup.find("span", {"class": "redirect-query m-t-16"})

                if search_instead is not None:
                    self.href = search_instead.findChild('a').get('href')
                    soup = self.search_instead()
            else:
                print(f"Failed to fetch data. Status Code: {response.status_code}")
                soup = None

            if soup is not None:
                self.extract(soup)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while searching for the keyword: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def extract(self, soup : BeautifulSoup):
        title = soup.find('span', {'class' : 'title'}).findChild('b').get_text(strip=True)
        volume = soup.find('div', {'class' : 'number-of-results tbody-5'}).get_text(strip=True).split(sep=" ")[0]

        self.data['Title'] = title
        self.data['Volume'] = volume


    def getData(self) -> dict:
        return self.data