import requests
from bs4 import BeautifulSoup as BS
import os

from service.logger import LOGGER


def update_shedule(university_name: str, URL: str, *args) -> None:
    resp = requests.get(URL)

    soup = BS(resp.text, features='html.parser')
    links_soup = soup.find_all(*args)

    file_counter_expected = len(links_soup)
    file_counter = 0
    
    links = []

    for link in links_soup:
        href = link.get('href')
        links.append(href)
        link_resp = requests.get(href, allow_redirects=True)

        filename = href.rsplit('/', 1)[-1]
        dir_path = f"tables\\{university_name}\\"

        full_path = str(os.path.realpath(__file__)).replace("parser.py", dir_path + filename)
        open(full_path, 'wb').write(link_resp.content)

        file_counter += 1

    if file_counter_expected != file_counter:
        LOGGER.critical(f"failed to update schedule, university_name='{university_name}', donwloaded : {file_counter} of {file_counter_expected}")
    else:
        LOGGER.info(f"the schedule has been updated, university_name='{university_name}', donwloaded : {file_counter} of {file_counter_expected}")




def get_shedule(study_data: list[str, int, str, str], week_type: int, day: int):
    """
    Study_data structure:\n
    {
        'university': None,
        'course': None,
        'faculty': None,
        'group': None,
    }
    """
    print("Парсим xlsx")
    pass

