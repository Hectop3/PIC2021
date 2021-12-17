from urllib.request import urlopen


from bs4 import BeautifulSoup
import json
import re

VERSION = '0.1.0'

RESPONSE = {
    'id': str,
    'title': str,
    'upload_date': str,
    'duration': str,
    'description': str,
    'genre': str,
    'is_paid': bool,
    'is_unlisted': bool,
    'is_family_friendly': bool,
    'uploader': {
        'channel_id': str,
    },
    'statistics': {
        'views': int,
        'likes': int,
        'dislikes': int
    }
}


def is_true(string):
    return string.lower() not in ['false', '0']


def remove_comma(string):
    return ''.join(string.split(','))


def make_soup(url):




def scrape_video_data(id):


    youtube_video_url = 'https://www.youtube.com/watch?v=' + id


    soup = make_soup(youtube_video_url)
    soup_itemprop = soup.find(id='watch7-content')

    if len(soup_itemprop.contents) > 1:
        video = RESPONSE
        uploader = video['uploader']
        statistics = video['statistics']
        video['regionsAllowed'] = []

        video['id'] = id

        for tag in soup_itemprop.find_all(itemprop=True, recursive=False):
            key = tag['itemprop']
            if key == 'name':

                video['title'] = tag['content']
            elif key == 'duration':

                video['duration'] = tag['content']
            elif key == 'datePublished':

                video['upload_date'] = tag['content']
            elif key == 'genre':

                video['genre'] = tag['content']
            elif key == 'paid':

                video['is_paid'] = is_true(tag['content'])
            elif key == 'unlisted':

                video['is_unlisted'] = is_true(tag['content'])
            elif key == 'isFamilyFriendly':

                video['is_family_friendly'] = is_true(tag['content'])
            elif key == 'thumbnailUrl':

                video['thumbnail_url'] = tag['href']
            elif key == 'interactionCount':

                statistics['views'] = int(tag['content'])
            elif key == 'channelId':

                uploader['channel_id'] = tag['content']
            elif key == 'description':
                video['description'] = tag['content']
            elif key == 'playerType':
                video['playerType'] = tag['content']
            elif key == 'regionsAllowed':
                video['regionsAllowed'].extend(tag['content'].split(','))

        all_scripts = soup.find_all('script')
        for i in range(len(all_scripts)):
            try :
                if 'ytInitialData' in all_scripts[i].string:
                    match = re.findall("label(.*)",re.findall("LIKE(.*?)like",all_scripts[i].string)[0])[0]
                    hasil = (''.join(match.split(',')).split("\"")[-1]).strip()
                    try:
                        video['statistics']['likes'] = eval(hasil)
                    except:
                        video['statistics']['likes'] = 0
                
                    match = re.findall("label(.*)",re.findall("DISLIKE(.*?)dislike",all_scripts[i].string)[0])[0]
                    hasil = (''.join(match.split(',')).split("\"")[-1]).strip()
                    try:
                        video['statistics']['dislikes'] = eval(hasil)
                    except:
                        video['statistics']['dislikes'] = 0
                
            except :
                pass

        return RESPONSE

    return ({
        'error': 'Video with the ID {} does not exist'.format(id)
    })