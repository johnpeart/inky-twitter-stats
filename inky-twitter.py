#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ####################
## IMPORT MODULES ##
####################
import os
import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
import datetime # The datetime module supplies classes for manipulating dates and times.
import argparse # Enables you to pass arguments through terminal
import random # Enables picking random choices from lists
import pickle # Allows you to save and load abitrary data to files
import keys # This module stores API credentials for use with the Twitter Developer API
import twitter # This module handles interactions with the Twitter Developer API
from PIL import Image, ImageFont, ImageDraw # This module handles creation of images and text, which are sent to the display
from StringIO import StringIO
from inky import InkyWHAT # This module makes the e-ink display work and renders the image

#########################################
## SET VARIABLES FROM THE COMMAND LINE ##
#########################################

# Command line arguments to set display type and colour, and enter your name

parser = argparse.ArgumentParser()
parser.add_argument("--username", "-u", type=str, help="Your Twitter handle without the @ symbol", default="johnpeart")
parser.add_argument("--test", "-t", type=bool, help="Set to 'true' to output to local PNG instead of to the display")
parser.add_argument("--colour", "-c", nargs="?", type=str, help="Set colour of the display", default="yellow")
args = parser.parse_args()

twitterUsername = args.username

twitterUsernameString = "@{}".format(twitterUsername)

test = args.test

inkyColour = args.colour



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
# 1. "path/to/font" - where path/to/font is the path to the .ttf or .otf file
# 2. font size - as an integer

usernameFont = ImageFont.truetype("./inky-twitter-stats/fonts/heavy.otf", 25)
descriptionFont = ImageFont.truetype("./inky-twitter-stats/fonts/regular.otf", 16)
headingFont = ImageFont.truetype("./inky-twitter-stats/fonts/heavy.otf", 16)
statFont = ImageFont.truetype("./inky-twitter-stats/fonts/light.otf", 36)
    
usernameFontWidth, usernameFontHeight = usernameFont.getsize("ABCD ")
descriptionFontWidth, descriptionFontHeight = descriptionFont.getsize("ABCD ")
headingFontWidth, headingFontHeight = headingFont.getsize("ABCD ")
statFontWidth, statFontHeight = statFont.getsize("ABCD ")





#################
## REFLOW TEXT ##
#################
# This function reflows text across multiple lines.
# It is adapted from the Pimoroni guidance for the Inky wHAT.

def reflowText(textToReflow, width, font):
    words = textToReflow.split(" ")
    reflowed = ''
    line_length = 0
    line_count = 1

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n" + word
            line_count += 1

    return reflowed, line_count




###########################
## HUMAN READABLE NUMERS ##
###########################
# This function truncates large numbers with the 'K', 'M', 'B' and 'T' format
# representing thousands, millions, billions and trillions

def human_format(num):
    if abs(num) >= 99999:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    else:
        return '{:0,}'.format(num)





####################
## GET THE TWEETS ##
####################
# For each account defined in 'accounts.py', this function gets the latest tweet and prepares it for rendering.

def getUser(handle):
    getUser = api.GetUser(screen_name=handle, include_entities=True)
    return getUser




########################
## COMPARE SAVED DATA ##
########################
# The data will output to an e-paper display, so to avoid needlessly updating the screen, we need to check against the things we saw last time.
# This function tries to open the data store to compare the content of the file against the data the Twitter function pulls down, or else dump the current data into a new file for next time

def checkDataMatching():
    try:
        file = pickle.load(open('./inky-twitter-stats/savedData.pickle', 'rb')) # Load the existing data, if it exists
        if file.screen_name != user.screen_name:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.description != user.description:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.verified != user.verified:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.following != user.following:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.followers_count != user.followers_count:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.statuses_count != user.statuses_count:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        elif file.favourites_count != user.favourites_count:
            print("NEW DATA. We need to refresh the screen.")
            refresh = True
        else:
            print("NO NEW DATA. We do not need to refresh the screen.")
            refresh = False
    except (OSError, IOError) as e:
        pickle.dump(user, open("./inky-twitter-stats/savedData.pickle", "wb")) # Create a new file
        print("NEW DATA. We need to refresh the screen.")
        refresh = True
    return refresh



##################################
## SET UP THE INKY WHAT DISPLAY ##
##################################
# Set the display type and colour
# InkyPHAT is for the smaller display and InkyWHAT is for the larger display.
# Accepts arguments 'red', 'yellow' or 'black', based on the display you have. 
# (You can only use 'red' with the red display, and 'yellow' with the yellow; but 'black' works with either).

def initialiseScreen(inkyColour):
    inky = InkyWHAT(inkyColour)
    return inky


########################
## UPDATE THE DISPLAY ##
########################
# Once you've prepared and set your image, and chosen a border colour, you can update your e-ink display with .show()

def updateDisplay(refresh, user):
    if refresh == True:
        
        if test == True:
            yellow = "#9B870C"
            red = "#9B870C"
            white = "#ffffff"
            black = "#000000"
            displayHeight = 300
            displayWidth = 400
        else:
            inky = initialiseScreen(inkyColour)
            yellow = inky.YELLOW
            red = inky.RED
            white = inky.WHITE
            black = inky.BLACK
            displayHeight = inky.HEIGHT
            displayWidth = inky.WIDTH

        if user.verified == True:
            screen_name = u'\u2713' + " @" + user.screen_name
        else:
            screen_name = "@" + user.screen_name
        description = user.description

        following = user.friends_count
        followers_count = user.followers_count
        statuses_count = user.statuses_count
        favourites_count = user.favourites_count

        file = pickle.load(open('./inky-twitter-stats/savedData.pickle', 'rb')) # Load the existing data, if it exists

        followers_change = followers_count - file.followers_count
        following_change = following - file.friends_count
        statuses_change = statuses_count - file.statuses_count
        favourites_change = favourites_count - file.favourites_count

        if followers_change > 0:
            followers_trend = u'\u2197' + " +" + human_format(followers_change)
        elif followers_change < 0:
            followers_trend = u'\u2198' + " " + human_format(followers_change)
        else:
            followers_trend = "No change"

        if following_change > 0:
            following_trend = u'\u2197' + " +" + human_format(following_change)
        elif following_change < 0:
            following_trend = u'\u2198' + " " + human_format(following_change)
        else:
            following_trend = "No change"

        if statuses_change > 0:
            statuses_trend = u'\u2197' + " +" + human_format(statuses_change)
        elif statuses_change < 0:
            statuses_trend = u'\u2198' + " " + human_format(statuses_change)
        else:
            statuses_trend = "No change"

        if favourites_change > 0:
            favourites_trend = u'\u2197' + " +" + human_format(favourites_change)
        elif favourites_change < 0:
            favourites_trend = u'\u2198' + " " + human_format(favourites_change)
        else:
            favourites_trend = "No change"

        pickle.dump(user, open("./inky-twitter-stats/savedData.pickle", "wb")) # Overwrite the data with the latest pull

        img = Image.new("P", (displayWidth, displayHeight))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (displayWidth, displayHeight)], fill = white, outline=None)
        draw.text((20, 20), screen_name, yellow, usernameFont)
        reflowed = reflowText(description, (displayWidth - 40), descriptionFont)
        reflowedDescription, lineCount = reflowed
        draw.text((20, 60), reflowedDescription, black, descriptionFont)
        draw.text((20, 140), "Followers", black, headingFont)
        draw.text((200, 140), "Following", black, headingFont)
        draw.text((20, 220), "Tweets", black, headingFont)
        draw.text((200, 220), "Favourites", black, headingFont)
        draw.text((20, 160), human_format(followers_count), black, statFont)
        draw.text((200, 160), human_format(following), black, statFont)
        draw.text((20, 240), human_format(statuses_count), black, statFont)
        draw.text((200, 240), human_format(favourites_count), black, statFont)
        draw.text((105, 140), followers_trend, yellow, headingFont)
        draw.text((285, 140), following_trend, yellow, headingFont)
        draw.text((85, 220), statuses_trend, yellow, headingFont)
        draw.text((290, 220), favourites_trend, yellow, headingFont)

        if test == True:
            print('Updating local image')
            img.save("./inky-twitter-stats/debug.png")
        else:
            print('Updating Inky wHAT display')
            inky.set_image(img) # Set a PIL image, numpy array or list to Inky's internal buffer.
            inky.set_border(white) # .set_border(colour) sets the colour at the edge of the display
            inky.show()
    else:
        print('Do nothing')





#########################
## PUT IT ALL TOGETHER ##
#########################

user = getUser(twitterUsername)
refresh = checkDataMatching()
updateDisplay(refresh, user)