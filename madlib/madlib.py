#!/usr/bin/env python
# coding: utf8
# CS4120 NLP, Northeastern University 2020

import json
import random

menus = "../webscraping/menus.json"
ten_percent = range(0,10)
twenty_five_percent = range(0,4)
filler = ["Uh", "Um", "Uhhhh", "Yeah", "Hmm"] # informal filler words
like = "like"
templates = ["Can I get", "Could I get", "Could I just get", "I'll have", "I'd like", "I'll get", "Can I have", "I'll just have", "I'll just get", "Could I please have", "Can I please get", "Can I please have", "Could I please just get", "Could I please just have"]
also = "also"
conjunctions = ["and", "with"]
thanks = ["please", "thanks", "thank you", "that's it", "that'll be it", "that's all", "I think that's it", "that should be it", "that should be all", "that's it, I think", "that should be all, I think", "alright, that's it", "alright, that'll be it", "okay, that should be it"]

#
def sentence_order_weighted():
    x = random.choice(range(1,100))

    if x <= 5:
        return 4
    if x <= 20:
        return 3
    if x <= 40:
        return 2
    else:
        return 1

def quantities_weighted():
    x = random.choice(range(0,1000))

    if x <= 5:
        return "five"
    if x <= 25:
        return "four"
    if x <= 50:
        return "three"
    if x <= 100:
        return "two"
    if x <= 500:
        return "a"
    else:
        return "one"

# randint between 1 and 2
def flip_coin():
    x = random.randint(1,2)
    if x == 1:
        return True
    else:
        return False

def tenP():
    x = random.randint(1,10)
    if x == 1:
        return True
    else:
        return False

def twentyfiveP():
    x = random.randint(1,4)
    if x == 1:
        return True
    else:
        return False

# Open a json
def open_json(filename):
    with open(filename) as f:
        data = json.load(f)

    return data

def get_item(j, ks):
    r = random.choice(list(ks))

    m = j[r]
    while len(m) == 0:
        r = random.choice(list(ks))
        m = j[r]
        
    item = random.choice(range(0, len(m)))
    item_name = list(m[item].keys())[0]
    
    return item_name

def sentence(j, ks):
    sentence = ""
    orders = sentence_order_weighted()

    for i in range(0, orders):
        if twentyfiveP():
            sentence += random.choice(filler) + " "

        if i > 0 and tenP():
            sentence += also + " "

        if flip_coin():
            sentence += random.choice(templates) + " "

        if twentyfiveP():
            sentence += random.choice(filler) + " "

        sentence += quantities_weighted() + " "

        sentence += get_item(j, ks) + " "

        if i < (orders - 1):
            sentence += random.choice(conjunctions) + " "

    if random.choice(twenty_five_percent) == 1:
        sentence += random.choice(thanks) + " "

    return sentence

def full_sample(j, ks):
    sentences = sentence_order_weighted()

    for i in range(0, sentences):
        print(sentence(j, ks))

def main():
    j = open_json(menus)
    for i in range(0, 100):
        full_sample(j, j.keys())

if __name__ == "__main__":
    main()
