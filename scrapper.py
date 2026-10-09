import requests
from requests import Response
from requests.exceptions import HTTPError
import json

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ko;q=0.7',
    'priority': 'u=1, i',
    'Authorization': '',
    'Origin': 'https://mangalib.me',
    'Referer': 'https://mangalib.me/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36',
    'Client-Time-Zone': 'Asia/Yekaterinburg',
    'Content-Type': 'application/json',
    'Sec-Ch-Ua': '"Google Chrome";v="155", "Chromium";v="155", "Not(A:Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Mode': 'cors',
    'Site-Id': '1'
}


def scrap_from_mangalib(user_id: int) -> list[dict]:
    manga_raw_list: list[dict] = []
    page: int = 1
    
    while True:
        url: str = f'https://api.cdnlibs.org/api/bookmarks?status=0&user_id={user_id}&sort_by=name&sort_type=desc&page={page}'

        response: Response = requests.get(url=url, headers=HEADERS)
        if response.status_code != 200:
            raise HTTPError('Error')
        response_json: dict = response.json()
        manga_page_list: list[dict] = response_json['data']
        meta: dict = response_json['meta']

        manga_raw_list += [manga for manga in manga_page_list]

        if meta['next_page_url']:
            page += 1
        else:
            break

    return manga_raw_list

def get_manga_list(user_id: int) -> list[dict]:
    manga_raw_list: list[dict] = scrap_from_mangalib(user_id)

    manga_list: list[dict] = []

    for manga_raw in manga_raw_list:
        manga = {
            'rus_name': manga_raw['media']['rus_name'],
            'eng_name': manga_raw['media']['eng_name'],
            'title_cover': manga_raw['media']['cover']['default'],
            'title_link': f"https://mangalib.me/ru/manga/{manga_raw['media']['slug']}",
            'status': manga_raw['status']
        }
        manga_list.append(manga)

    return manga_list
