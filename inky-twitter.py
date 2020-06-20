#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ####################
## IMPORT MODULES ##
####################
import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
import datetime # The datetime module supplies classes for manipulating dates and times.
import argparse # Enables you to pass arguments through terminal
import random # Enables picking randomin choices from lists
import re # Strips text easily
import keys # This module stores API credentials for use with the Twitter Developer API
import twitter # This module handles interactions with the Twitter Developer API
from PIL import Image, ImageFont, ImageDraw # This module handles creation of images and text, which are sent to the display
from StringIO import StringIO

#########################################
## SET VARIABLES FROM THE COMMAND LINE ##
#########################################

# Command line arguments to set display type and colour, and enter your name

parser = argparse.ArgumentParser()
parser.add_argument("--username", "-u", type=str, help="Your Twitter handle without the @ symbol", default="unsplash")
parser.add_argument("--test", "-t", type=bool, default=True, help="Set to 'true' to output to local PNG instead of to the display")
parser.add_argument("--colour", "-c", nargs="?", type=str, help="Set colour of the display", default="yellow")
args = parser.parse_args()

twitterUsername = args.username

twitterUsernameString = "@{}".format(twitterUsername)

test = args.test

inkyColour = args.colour


##########################
## SET GLOBAL VARIABLES ##
##########################

yellow = "#9B870C"
red = "#9B870C"
white = "#ffffff"
black = "#000000"

if test == True:
    displayHeight = 300
    displayWidth = 400
else:
    from inky import InkyWHAT # This module makes the e-ink display work and renders the image
    displayHeight = inky.HEIGHT
    displayWidth = inky.WIDTH

now = datetime.datetime.now()

tweetFontSize = 16
tweetSmallFontSize = 12
accountFontSize = 16
statsFontSize = 24



##################################
## SET UP THE INKY WHAT DISPLAY ##
##################################
# Set the display type and colour
# InkyPHAT is for the smaller display and InkyWHAT is for the larger display.
# Accepts arguments 'red', 'yellow' or 'black', based on the display you have. 
# (You can only use 'red' with the red display, and 'yellow' with the yellow; but 'black' works with either).

if test != True:
    inky = InkyWHAT(inkyColour)


##################################################
## IMPORT THE TWITTER DEVELOPER API CREDENTIALS ##
##################################################
# This sets your Twitter Developer API credentials.
# It imports the keys from 'keys.py', which is not included in the repository.
# The keys are in this format:
# 
# twitter = {
#     "consumer_key": "YOUR KEY HERE",
#     "consumer_secret": "YOUR KEY HERE",
#     "access_token_key": "YOUR KEY HERE",
#     "access_token_secret": "YOUR KEY HERE"
# }

api = twitter.Api(
    consumer_key = keys.twitter["consumer_key"],
    consumer_secret = keys.twitter["consumer_secret"],
    access_token_key = keys.twitter["access_token_key"],
    access_token_secret = keys.twitter["access_token_secret"],
    tweet_mode= 'extended' # Include this or tweets will be truncated
)








##########################
## IMPORT FONTS FOR USE ##
##########################
# ImageFont.truetype accepts two arguments, (1, 2):
# 1. "path/to/font" - where path/to/font is the path to the .ttf file
# 2. font size - as an integer

tweetFont = ImageFont.truetype("fonts/Regular.ttf", tweetFontSize)
tweetSmallFont = ImageFont.truetype("fonts/Regular.ttf", tweetSmallFontSize)
accountFont = ImageFont.truetype("fonts/Bold.ttf", accountFontSize)
statsFont = ImageFont.truetype("fonts/Bold.ttf", statsFontSize)

statsFontWidth, statsFontHeight = statsFont.getsize("ABCD ")





###########################
## HUMAN READABLE NUMERS ##
###########################
# This function truncates large numbers with the 'K', 'M', 'B' and 'T' format
# representing thousands, millions, billions and trillions

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])





####################
## GET THE TWEETS ##
####################
# For each account defined in 'accounts.py', this function gets the latest tweet and prepares it for rendering.

def getUser(handle):
    getUser = api.GetUser(screen_name=handle, include_entities=True)
    return getUser
#   return getUser.following, getUser.followers_count, getUser.friends_count, getUser.favourites_count, getUser.statuses_count

user = getUser(twitterUsername)
description = user.description
verified = user.verified
following = user.friends_count
followers_count = user.followers_count
statuses_count = user.statuses_count
favourites_count = user.favourites_count
listed_count = user.listed_count

print('Username: @{}').format(twitterUsername) # Print the username
print("Description: {}").format(description)
print("Verified: {}").format(verified)
print("Following: {}").format(following)
print("Followers: {}").format(followers_count)
print("Tweets: {}").format(statuses_count)
print("Favourites: {}").format(favourites_count)
print("Listed: {}").format(listed_count)

########################
## FINALISE THE IMAGE ##
########################
# Set a PIL image, numpy array or list to Inky's internal buffer. The image dimensions should match the dimensions of the pHAT or wHAT you're using.
# You should use PIL to create an image. PIL provides an ImageDraw module which allow you to draw text, lines and shapes over your image. 
# See: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

# inky.set_image(img)





###############################
## SET DISPLAY BORDER COLOUR ##
###############################
# .set_border(colour) sets the colour at the edge of the display
# colour should be one of 'inky.RED', 'inky.YELLOW', 'inky.WHITE' or 'inky.BLACK' with available colours depending on your display type.

# inky.set_border(white)





########################
## UPDATE THE DISPLAY ##
########################
# Once you've prepared and set your image, and chosen a border colour, you can update your e-ink display with .show()

# if test == True:
#     print('Updating local image')
#     img.save("./inky-nth-tweet/debug.png")
# else:
#     print('Updating Inky wHAT display')
#     inky.show()