# twitter_likes

This small Python 3 project allows to fetch from Twitter API all the tweets you (or even another account) liked, 
to save them (for backup) and display them as a nice HTML page.

I use it to save interesting content I see in my feed and to easily come back to it later or search content. For my own usage only.
Even if the original tweet was deleted or the author's profile was switched to private.

![result screenshot](screenshot.png)

## Known limitations
* The API has a "since" parameter that allows to fetch only the most recent tweets. That would be really helpful however we cannot use it since it would make us miss old tweets that are liked in the present if we liked more recent content in the meantime. Because this parameter works on the tweet date, not on date of the like action.
* The output page works fine on mobile but it isn't perfect. PRs are welcome :)
* The output page is not paginated, so everything is on one page. It's easier to search within, but it could be too much with too many likes since that's a lot of content and images are all loaded at opening.
* The GIF or videos embedded in original content are displayed as static images as it allows to save bandwidth when loading the page. Also the interesting content is more often in the text than in the image, and we can always open the original tweet.
* The media content is not downloaded and backed up so we can lose access to it, but I don't care as the text is usually what matters most.