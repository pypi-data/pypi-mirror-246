"""Helper module to create a sample config.ini file."""
# flake8: noqa
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

CONFIG_TEMPLATE = """
# This is the config file for Tootbot! You must restart the bot for any changes to take
# effect.

# General settings
[BotSettings]
# Minimum delay between social media posts, in seconds (default is '600')
DelayBetweenPosts: 300
# Run only once (for example when using cron to run tootbot on schedule)
RunOnceOnly : false
# Minimum position of post on subreddit front page that the bot will look at
# (default is '10')
PostLimit : 10
# Allow NSFW Reddit posts to be posted by the bot
NSFWPostsAllowed : false
# NSFW media will be marked as sensitive
NSFWPostsMarked : true
# Allow Reddit posts marked as spoilers to be posted by the bot
SpoilersAllowed : true
# Allow Reddit self-posts to be posted by the bot
SelfPostsAllowed : true
# Allow Reddit stickied post to be posted by the bot
StickiedPostsAllowed : false
# List of hashtags to be used on EVERY post, separated by commas without # symbols
# (example: hashtag1, hashtag2)
# Hashtags in the Subreddits section of this config file will be added to the overall
# hashtags defined here.
# Leaving this blank will disable overall hashtags
Hashtags :
# Log level for messages printed to stdout
# Possible values are CRITICAL, ERROR, WARNING, INFO, DEBUG
# If not set the default is INFO
LogLevel : INFO

# Name of subreddits to take posts from (example: 'gaming')
# Multireddits can be used like this: 'gaming+funny+news'
# lines in the Subbreddits section are formatted as:
# subreddit: hashtags
# Subreddit can also be a multireddit as per above
# hashtags can be one or multiple hashtags separated by commas without the "#" symbol
# (e.g. hashtag1, hashtag2)
[Subreddits]
cats: cats
kittens+bodegacats: cats, kittens, bodegcats
dogs: dogs
puppies+goodboy: dogs, puppies, goodboy

# Name of redditors (reddit users) to follow and take posts from
# lines in the Redditors section are formatted as:
# username: hashtags
# hashtags can be one or multiple hashtags separated by commas without the "#" symbol
# (e.g. hashtag1, hashtag2)
[Redditors]
Sunkisty: variety

# Name of redditors (reddit users) to skip / ignore
# lines in the IgnoreUsersList section are formatted as:
# username:
# the trailing colon (":") is important!
[IgnoreUsersList]
toughgetsgoing:
Turbulent-Egg-9222:
Time_Comfortable8644:
YouHaveANiceName:
Humble_Dumbbell:


# Settings related to promotional messages
[PromoSettings]
# How often should the promotional message be added
# Setting is for a promotional message to be added every x messages
# I.e. 0 = no promotional messages added ever
#      1 = promotional message added to every new post
#      2 = promotional message added to every 2nd new post
#      n = promotional message added to every nth new post
PromoEvery: 0
# Actual Promotional message to be added
PromoMessage: Posted with tootbot (https://codeberg.org/MarvinsMastodonTools/tootbot)

#Settings around Health Checks
[HealthChecks]
# This is the part of the URL before the unique id UID of the check. Could be
# something like
# https://hc-ping.com or https://hc.example.com:8000/ping/
# To disable Healthchecks leave the BaseUrl empty
BaseUrl:
# This is the unique identifier for the health check you set-up in your
# HealthChecks account.
# It will be in the format: 123e4567-e89b-12d3-a456-426614174000
UUID :

# Settings related to media attachments
[MediaSettings]
# Folder name for media downloads (default is 'media')
MediaFolder: media
# Set the bot to only post Reddit posts that directly link to media
# Links from Giphy, Imgur, i.redd.it, and i.reddituploads.com are
# currently supported
MediaPostsOnly: false

# Mastodon settings
[Mastodon]
# Name of instance to log into (example: mastodon.social). This is mandatory
InstanceDomain :
# Sets all media attachments as sensitive media, this should be left on 'true'
# in most cases (note: images from NSFW Reddit posts will always be marked as sensitive)
# More info:
# https://gist.github.com/joyeusenoelle/74f6e6c0f349651349a0df9ae4582969#what-does-cw-mean
SensitiveMedia : true
# Visibility setting to use for posts. If left empy defaults to "public"
# Possible values are "public", "unlisted", "private"
PostVisibility : unlisted
# With throttling enabled, tootbot will slow down posting toots more and more while
# the Mastodon API is returning errors
ThrottlingEnabled : true
# Maximum delay in seconds between attempts to post a toot when throttling.
ThrottlingMaxDelay : 86400
# Should tootbot add a caption to the toot? This defaults to true and will use the title
# of the reddit post as source for the caption
UseCaption : true
# Include hash tags in toots posted? This setting defaults to true and will use the
# hash tags defined in this config file.
UseTags : true
# Include a link back to the reddit post being tooted. This defaults to true
UseBacklink : true
# Make back link go directly to url reddit post links to. For this to take effect,
# UseBacklink needs to be set to true as well.
MediaLink : false
# Add "posted by #u<reddit username>" to the end of the post but before any hash tags.
UseRedditorTag: false
"""


def create() -> None:
    """Creates a sample config.ini configuration file."""
    with open(file="config.ini", mode="w+", encoding="UTF-8") as config_file:
        config_file.writelines(CONFIG_TEMPLATE)
