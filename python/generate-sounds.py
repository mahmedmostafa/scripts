#!/bin/python

from sys import argv
from gtts import gTTS
import argparse

parser = argparse.ArgumentParser(prog="generate-sound.py",usage="%(prog)s [options]")

parser.add_argument("--word",help="word to generate",required=True)
parser.add_argument("--lang",help="language to use",required=True)
parser.add_argument("--times", help="How many times to generate the word", type=int)

args = parser.parse_args()
words= lambda: (args.word + ". ") * args.times if args.times else args.word + ". "

language = args.lang
times = args.times
word = words()

sound = gTTS(word,lang=language)
sound.save("%s.mp3" % word.split()[0].rstrip("."))

