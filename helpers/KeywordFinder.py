from bs4 import BeautifulSoup
import requests

class KeywordFinder:
    def __init__(self) -> None:
        self.headers = {
            'authority': 'www.fiverr.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            'referer': 'https://www.fiverr.com/search/gigs?query=wordpress%20site',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-full-version': '114.0.5735.248',
            'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.248", "Google Chrome";v="114.0.5735.248"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': 'Windows',
            'sec-ch-ua-platform-version': '10.0.0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'ect': '4g'
        }

        self.cookies = {
            'u_guid': '1690154923000-f8f75c54ee02763d6f162bba16cb667bed0cc8b1',
            '_pxhd': 'SXW9P2GeOn7nGk31DEbeU2oE5PE1hjO4uW8hd9nkLZ7aZVnErn9lh1I9/R/KQs9z9615t6Q73VypivCLXGVbxg==:sdvwxYUR9DVPFH5-oUQefz3TE8wDVGO7595/xjMZLoFElF8RbuF-JOBiHWQjOXY00dQg7p71JRjGggbKkODYaCUT8dxnGcxcLZc0eD8GyrU=',
            'logged_out_currency': 'PKR',
        }

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


    def soupify(x : requests.Response):
        return BeautifulSoup(x.content,'html.parser')
    

    def search_instead(self):
        response = self.session.get(self.mainurl, params=self.params)

        if response.status_code == 200:
            soup = self.soupify(response)
            return soup
        
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            return None


    def search(self, query) -> None:
        self.params['query'] = query
        response = self.session.get(self.mainurl, params=self.params)

        if response.status_code == 200:
            soup = self.soupify(response)
            search_instead = soup.find("span", {"class" : "redirect-query m-t-16"})

            if search_instead is not None:
                self.href = search_instead.findChild('a').get('href')
                soup = self.search_instead()

        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")

        if soup is not None:
            self.extract(soup)


    def extract(self, soup : BeautifulSoup):
        title = soup.find('span', {'class' : 'title'}).findChild('b').get_text(strip=True)
        volume = soup.find('div', {'class' : 'number-of-results tbody-5'}).get_text(strip=True).split(sep=" ")[0]

        self.data['Title'] = title
        self.data['Volume'] = volume


    def getData(self) -> dict:
        return self.data