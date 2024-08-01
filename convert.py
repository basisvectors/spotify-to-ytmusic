import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Sec-GPC': '1',
    'Alt-Used': 'ytm2spotify.com',
    'Connection': 'keep-alive',
    'Referer': 'https://ytm2spotify.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def convert_to_yt(url, headers=HEADERS):
    params = {
        'url': url,
        'to_service': 'youtube_music',
    }

    response = requests.get(
        'https://ytm2spotify.com/convert', params=params, headers=headers)
    
    return response.json()

def uri_to_url(uri):
    _, type_, id_ = uri.split(':')
    return f'https://open.spotify.com/{type_}/{id_}'

def get_channel_id(channel_uri):
    return channel_uri.split("channel/")[-1]