import requests
from requests import Response
from requests.exceptions import HTTPError
import json

HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8,ko;q=0.7',
    'priority': 'u=1, i',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMjkxNTZjZDJiOTYyYThmNzkwNWE0MGEzODI3ZThhZDQ4NGMwMzdlNDYwMDU3YmMwMDZjNTQxODUyYzVkYzFhMmJkYmI3ZDFmNDYwYzMwNTYiLCJpYXQiOjE3OTA5NjMwNzkuNzU2NzMyLCJuYmYiOjE3OTA5NjMwNzkuNzU2NzM0LCJleHAiOjE3OTM2NDE0NzkuNzUyNDE3LCJzdWIiOiIxMzI5MDc2Iiwic2NvcGVzIjpbXX0.1NlWoKtTlGeVky0Im-LMeCKaAa5oJL1qxfB5Z1WzZQoDdKiLiK5RpMeKVgu6dsPQ_ih88vn8zoAZ7IyqEYB6MaVOk3Edv9ONZiuAfWB2VMj2aMedTKJyl07rp8xlC7YV45x9d9Vdxai-W4HCeB2x0tN1sv4-JaIGgBQGeezSvmf-xP8ZNy1p3osIHiV8KcZhtuPoDJVmzvaR6yT2FCJliThWevXMLngT3CzW9RCPgUbIt9RNABYSIwRnZ1oy2LGl-cJV5K8DvjRkswUfvUdljc2DcmGwnicGf89FmmngBAZ7hlZ4xe6s-xnhJRXyRhpjCdGMbDP-SF-M-2h5QTrW6FoFlQBbbQsk2546MMCn2bqcvjM-8tdBYqF74Hc7BgseThNOPcJUVxWM-8xTREJS0-BMmnm-afEGLfkY_pOwAUwRHAatP49jNlrtDE3Xuq3ky155X-ZE0xNw0eoDqy3aIvcEos0CTqcKeJ0D6LP_jR4CCrkKU8hNnhHHZpwJUTN10YEaWfdAmdXAs-rm4PZI0AcfW-f2ncHEM8FvOEoRQg5MLrV0remHgkX23JtQQQQvvBPP5rJrdWrMISRrqyWm_z1J0kdgGfj3zWdyt0VzDRRgOFmAnQLzZsgvPX0r1EEbvl_tTwTS9hsUNSfleTB-qBfAp4WDIXICDicB6-pxRhc',
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
