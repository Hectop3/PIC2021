import os
import argparse
import json
from scraper.description_downloader import scrape_video_data
from scraper.comments_downloader import comments_extractor

parser = argparse.ArgumentParser()
parser.add_argument('--video_id', required=True, help='YouTube video ID')
parser.add_argument('--out_dir', required=True, help='Directory to store video description')
args = vars(parser.parse_args())

if not os.path.exists(args['out_dir']):
    os.makedirs(args['out_dir'])

description_response = scrape_video_data(args['video_id'])
comment_response = comments_extractor(args['video_id'])

response = {
	'video_description': description_response,
	'comment_response': comment_response
}

with open(os.path.join(args['out_dir'],args['video_id'] + '.json'), 'w') as fw:
	fw.write(json.dumps(response))
