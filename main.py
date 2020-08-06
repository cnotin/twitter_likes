#!/usr/bin/env python3
# coding: utf-8

import json
import logging
import sys
from datetime import datetime

import tweepy

from reporting import generate_reporting
from secrets import *

TARGET_USER = sys.argv[1]

api = None


def get_old_likes():
    with open(f"data/likes_{TARGET_USER}.json", "r", encoding="utf-8") as f:
        try:
            likes = json.loads(f.read())
        except Exception as e:
            print("Error: " + str(e))
            likes = {}
    return likes


def save_likes(likes):
    with open(f"data/likes_{TARGET_USER}.json", "w", encoding="utf-8") as f:
        json.dump(likes, f, indent=2)


def get_new_likes(since):
    """
    get all favorites from Twitter API, since the last one we already know
    """
    # first pass over the obtained statuses
    liked_statuses = []
    for status in tweepy.Cursor(api.favorites,
                                TARGET_USER,
                                count=200,
                                tweet_mode="extended",  # get content in new 280 chars limitation
                                since_id=since
                                ).items():
        liked_statuses.append(status)

        # is it a quote-RT?
        if status.is_quote_status and hasattr(status, "quoted_status"):  # sometimes the quoted tweet has disappeared
            # then add quoted status to the processing list
            liked_statuses.append(status.quoted_status)

    # now we have all new liked statuses, process them
    likes = []
    for status in liked_statuses:
        like = {}
        likes.append(like)

        # twitter appends unecessary stuff at the end of the text of the tweet, so we just select what is proper text
        text = status.full_text[status.display_text_range[0]:status.display_text_range[1]]
        text = text.replace("\n", "<br />\n")
        # convert minified URLs found in text with the original URL value and add hyperlink
        if "urls" in status.entities:
            for url in status.entities['urls']:
                link = f'<a href="{url["expanded_url"]}">{url["display_url"]}</a>'
                text = text.replace(url['url'], link)
        like["text"] = text

        # handle pictures, videos and GIFs
        if hasattr(status, 'extended_entities'):
            if "media" in status.extended_entities:
                like["medias"] = []
                for media in status.extended_entities['media']:
                    if media["type"] in ("photo", "animated_gif", "video"):  # for videos we get the thumbnail
                        like["medias"].append(media["media_url_https"])

        like["profile_image_url_https"] = status.user.profile_image_url_https
        like["screen_name"] = status.user.screen_name
        like["name"] = status.user.name
        like["id"] = status.id
        like["created_at"] = status.created_at.isoformat()

    return likes


def main():
    global api

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    print(str(datetime.now()) + " Start")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # we have a cache of the already known liked tweets, so we don't re-fetch them and we keep them if they're deleted
    # or unliked!
    try:
        old_likes = get_old_likes()
        since = old_likes[0]['id']  # id of the most recent liked tweet in the cache
    except:
        # surely means it's the first run, we don't have the cache built yet
        old_likes = []
        since = 1

    # get from API new likes since the last one we already have in cache
    new_likes = get_new_likes(since)

    # prepend new liked tweets to the cache content
    all_likes = new_likes + old_likes

    # save new cache content
    save_likes(all_likes)

    # generate HTML reporting page based on all liked tweets
    generate_reporting(TARGET_USER, all_likes)

    print(str(datetime.now()) + " Bye!")


if __name__ == '__main__':
    main()
