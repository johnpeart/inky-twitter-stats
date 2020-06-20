# Inky Twitter Stats

This app displays your latest stats from Twitter on an e-ink display attached to a Raspberry Pi.

I made this to start to learn how to work with Python and the Inky wHAT display.

## Pre-requisites

### Hardware

- Raspberry Pi (running Raspbian Buster)
- Pimoroni Inky wHAT e-ink display

### Software

- Python 3
- [Inky Python library](https://github.com/pimoroni/inky)
- [Pillow Python library](https://pillow.readthedocs.io/en/stable/index.html)
- [Twitter Python library](https://python-twitter.readthedocs.io/en/latest/)

### Other stuff

- Access to the [Twitter Developer API](https://developer.twitter.com)

## Set up

1. To do

##  Usage

Run the code using 

```python
python inky-twitter.py
```

You can pass the following arguments to `inky-twitter.py`

- `--test`, `-t` - outputs a local PNG file `debug.png` instead of updating the Inky wHAT (defaults to False)
- `--colour`, `-c` - sets the colour of the display (defaults to yellow)
- `--help`, `-h` - runs the help

### Examples

```python
# Output locally to a PNG
python inky-twitter.py -t True
```

## Screenshots

To do

## Things to do

1. This will run just once; you'd need to set up a way for this to run on its own, probably with something like a cron job.

## Credits

Fonts are open sourced and from [iA Writer](https://github.com/iaolo/iA-Fonts).