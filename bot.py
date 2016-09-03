import tweepy, os
import urllib, json

from secrets import *
from time import gmtime, strftime

## XKCD Data collecter

def fetchComic(url):
    print "Fetching " + url
    response = urllib.urlopen(url)
    response_data = response.read()
    response_code = response.getcode()

    if(response_code == 200):
        data = json.loads(response_data)
        imgURL = data['img']
        imgTitle= data['title']
        imgDescription = data['alt']
        return [imgTitle, imgURL, imgDescription]
    return [None, None]

def getLatestComic():
    url = "http://xkcd.com/info.0.json"
    return fetchComic(url)


def getOldComics():

    base_url = "http://xkcd.com/"
    counter = 1
    response_code = 200

    while(True):
        #Forming the url for the comic
        currentComicURL = base_url + str(counter) + "/info.0.json"
        [imgTitle, imgUrl, imgDescription] = fetchComic(currentComicURL)
        if(imgTitle == None or imgUrl == None):
            break
        print imgTitle, imgUrl 
        counter += 1


## Twitter Bot

bot_username = C_NAME
logfile_name = bot_username + ".log"

def tweet(text):
    "Tweets on my behalf"

    auth  = tweepy.OAuthHandler(C_KEY,C_SECRET)
    auth.set_access_token(A_TOKEN,A_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted : " + text)

def tweetMedia(filename, title):
    
    auth  = tweepy.OAuthHandler(C_KEY,C_SECRET)
    auth.set_access_token(A_TOKEN,A_TOKEN_SECRET)
    api = tweepy.API(auth)

    try :
        api.update_with_media(filename,status=title)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted : " + title)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        print message
        f.write("\n" + t + " " + message)

if __name__ == "__main__":
    [tweetTitle, imgLink, imgDescription] = getLatestComic()

    localFileName = tweetTitle + ".png"
    statusMessage = tweetTitle + " " + imgLink + " " + "#xkcd" 
    urllib.urlretrieve(imgLink, filename=localFileName)
    tweetMedia(localFileName,statusMessage)
