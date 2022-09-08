# Use of Flickr API for Python to scrape images.

from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os,time,sys


key = "YOURFLICKRKEY"
secret = "YOURFLICKRSECRETKEY"

wait_time = 1
image_size = 'url_l'

#Get the first value of the command line argument. In the following cases[cat]Get
# python download.py cat 
category = sys.argv[1]
savedir = "./" + sys.argv[2]

#If path does not exist,it is created:
if not os.path.isdir(savedir):
    os.makedirs(savedir)
nb_images = int(sys.argv[3])
nb_pages = max((nb_images // 500), 1)

# format:Data to receive(Receive with json)
flickr = FlickrAPI(key, secret, format='parsed-json')

"""
text :Search keyword
per_page :Number of data you want to acquire
media :Type of data to search
sort :Sequence of data
safe_seach :Whether to display UI content
extras :The value of the option you want to get(url_q Image address information)
"""


def retrieve_img_per_page(n):
    result  = flickr.photos.search(
            text = category,
            per_page = min(500, nb_images),
            media = 'photos',
            sort = 'relevance',
            safe_seach = 1,
            extras = 'url_l, licence',
            page = n
        )
    return result['photos']
      

def download_photos(photos, image_size, n):
    for i, photo in enumerate(photos['photo']):
        try:
            url_size = photo[image_size]
            filepath = savedir + '/' + photo['id'] + '.jpg'
        except:
            continue
    #If there are duplicate files, skip them.
        if os.path.exists(filepath):
            continue
        print(f"{round((i + 1 + (n - 1) * 500)  / nb_images * 100, 1)} %", end='\r')
    #Download image data
        urlretrieve(url_size, filepath)
    #Wait 1 second to avoid overloading the server
        time.sleep(wait_time)
        
 
for n in range(1, nb_pages + 1):
    photos = retrieve_img_per_page(n)
    download_photos(photos, image_size, n)
