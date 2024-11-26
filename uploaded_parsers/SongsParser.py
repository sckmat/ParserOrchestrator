import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.links = [
            "https://www.amalgama-lab.com/songs/l/linkin_park/1stp_klosr.html",
            "https://www.amalgama-lab.com/songs/l/linkin_park/a_place_for_my_head.html",
            "https://www.amalgama-lab.com/songs/l/linkin_park/breaking_the_habit.html",
            "https://www.amalgama-lab.com/songs/l/linkin_park/crawling.html",
        ]

    def parse_song(self, url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        containers = soup.select(".string_container")
        translated_lines = [container.select_one(".translate").get_text(strip=True) for container in containers if
                            container.select_one(".translate")]

        return translated_lines

    def run(self):
        results = {}
        for url in self.links:
            song_title = url.split('/')[-1].replace('.html', '').replace('_', ' ').capitalize()
            translation = self.parse_song(url)
            results[song_title] = translation
        return results
