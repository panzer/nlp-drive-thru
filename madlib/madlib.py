#!/usr/bin/env python
# coding: utf8
# CS4120 NLP, Northeastern University 2020

import sys
import json
import random

menus = "../webscraping/menus.json"
ten_percent = range(0,10)
twenty_five_percent = range(0,4)
filler = ["Uh", "Um", "Uhhhh", "Yeah", "Hmm"]
quantities = ["One", "Two", "Three", "Four"]
like = "Like"
templates = ["Can I get", "Could I get", "Could I just get", "I'll have", "I'd like", "I'll get", "Can I have", "I'll just have", "I'll just get", "Could I please have", "Can I please get", "Can I please have", "Could I please just get", "Could I please just have", "I would like", "I will have", "I will get", "Could I please have", "Can I please get", "I would like to have", "I would like to get"]
modify_templates = ["Actually wait, could you make it", "Could you actually make it", "Could you change it to", "Can you actually change it to", "Wait, can it be", "Wait, can you make it", "Wait, could you make it", "Wait, could you change it to", "And can it be", "Sorry, could you change it to", "And can you change it to", "Sorry, could it be", "Sorry can it be"]
also = "Also"
conjunctions = ["and", "with"]
thanks = [", please", ", thanks", ", thank you", ", that's it", ", that'll be it", ", that's all", ". I think that's it", ". That should be it", ". That should be all", ". That's it, I think", ". That should be all, I think", ". Alright, that's it", ". Alright, that'll be it", ". Okay, that should be it"]

#
def fix_capitalization(s):
    xs = s.split(" ")
    result = ""
    result += xs[0] + " "

    for i in range(1, len(xs)):
        if xs[i-1] == "." or xs[i] == "I" or "." in xs[i-1]:
            result += xs[i] + " "
        elif xs[i] == "." or xs[i] == ",":
            result = result[:-1] + xs[i] + " "
        elif xs[i] != " ":
            result += xs[i].lower() + " "

    return result
    
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
        return "Five"
    if x <= 25:
        return "Four"
    if x <= 50:
        return "Three"
    if x <= 100:
        return "Two"
    if x <= 500:
        return "A"
    else:
        return "One"

def quantities_unweighted():
    return random.choice(quantities)

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
    item_size = m[item][item_name]["size"]
    
    return [item_name, item_size]

def sentence(j, ks):
    sentence = ""
    orders = sentence_order_weighted()
    modify_item = False
    modified_item = ""
    original_q = ""

    for i in range(0, orders):
        if twentyfiveP():
            sentence += random.choice(filler) + " "

        if i > 0 and tenP():
            sentence += also + " "

        if flip_coin():
            sentence += random.choice(templates) + " "

        if twentyfiveP():
            sentence += random.choice(filler) + " "

        if tenP():
            sentence += like + " "

        q = quantities_weighted()
        sentence += q + " "

        item = get_item(j, ks)
        if item[1] != "" and flip_coin():
            sentence += item[1] + " "

        if tenP() and not modify_item:
            modify_item = True
            modified_item = item[0]
            original_q = q.lower()

        sentence += item[0] + " "

        if i < (orders - 1):
            sentence += random.choice(conjunctions) + " "

    if modify_item:
        sentence = sentence[:-1] + ". "
        sentence += random.choice(modify_templates) + " "

        new_q = quantities_unweighted()
        while new_q == original_q:
            new_q = quantities_unweighted()
            
        sentence += new_q + " "
        sentence += modified_item + " "

    if twentyfiveP():
        sentence += random.choice(thanks) + " "

    sentence = sentence[:-1] + "."

    return sentence

def full_sample(j, ks):
    sentences = sentence_order_weighted()

    for i in range(0, sentences):
        print(fix_capitalization(sentence(j, ks)))

def main(x):
    j = open_json(menus)
    for i in range(0, x):
        full_sample(j, j.keys())

if __name__ == "__main__":
    main(int(sys.argv[1]))
