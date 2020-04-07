#!/usr/bin/env python
# coding: utf8
# CS4120 NLP, Northeastern University 2020

import sys
import json
import random
import string

SAMPLES = "samples.txt"
ANSWERS = "answers.txt"
ENTITIES = "entities.txt"
menus = "../webscraping/menus.json"
ten_percent = range(0,10)
twenty_five_percent = range(0,4)
filler = ["Uh", "Um", "Uhhhh", "Yeah", "Hmm"]
quantities = ["One", "Two", "Three", "Four"]
q_to_int = {"A":1, "One":1, "Two":2, "Three":3, "Four":4, "Five": 5}
like = "Like"
templates = ["Can I get", "Could I get", "Could I just get", "I'll have", "I'd like", "I'll get", "Can I have", "I'll just have", "I'll just get", "Could I please have", "Can I please get", "Can I please have", "Could I please just get", "Could I please just have", "I would like", "I will have", "I will get", "Could I please have", "Can I please get", "I would like to have", "I would like to get"]
modify_templates = ["Actually wait, could you make it", "Could you actually make it", "Could you change it to", "Can you actually change it to", "Wait, can it be", "Wait, can you make it", "Wait, could you make it", "Wait, could you change it to", "And can it be", "Sorry, could you change it to", "And can you change it to", "Sorry, could it be", "Sorry can it be"]
also = "Also"
conjunctions = ["and", "with"]
thanks = [", please", ", thanks", ", thank you", ", that's it", ", that'll be it", ", that's all", ". I think that's it", ". That should be it", ". That should be all", ". That's it, I think", ". That should be all, I think", ". Alright, that's it", ". Alright, that'll be it", ". Okay, that should be it"]

def entity_structure(sentence, items):
    result = "["

    # To prevent capitalization issues
    s = sentence.lower()
    for item in items:
        result += "("
        index = s.index(item.lower())
        result += str(index) + ", " + str(index + len(item)) + ", "
        result += "'MENU_ITEM'), "

    result = result[:-2] + "]"

    return result
    
def answer_structure(item, size, q):
    return "[" + item + ", " + size + ", " + str(q_to_int[q]) + "]"

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

def generalize(w):
    x = w.lower()
    x = x.replace(",", "")
    
    if "burger" in x:
        return "burger"
    elif "fries" in x:
        return "fries"
    elif "nuggets" in x:
        return "nuggets"
    elif "burrito" in x:
        return "burrito"
    elif "salad" in x:
        return "salad"
    elif "tenders" in x:
        return "tenders"
    elif "strips" in x:
        return "chicken strips"
    elif "soda" in x:
        return "soda"
    elif "– " in x:
        return x.replace("– ", "")
    elif "(" in x and ")" in x:
        i1 = x.index("(")
        i2 = x.index(")")

        return x[:(i1 - 1)] + x[(i2 + 1):]        
    else:
        return w
    
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
def open_json(filename, restaurant):
    with open(filename) as f:
        data = json.load(f)

    return data[restaurant]

def get_item(m):
    item = random.choice(range(0, len(m)))
    item_name = list(m[item].keys())[0]
    item_size = m[item][item_name]["size"]
    
    return [item_name, item_size]

def sentence(j):
    sentence = ""
    answer = ""
    orders = sentence_order_weighted()
    modify_item = False
    modified_item = ""
    original_q = ""
    original_s = ""
    items_list = []

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

        item = get_item(j)
        if item[1] != "" and flip_coin():
            sentence += item[1] + " "

        if tenP() and not modify_item:
            modify_item = True
            modified_item = generalize(item[0])
            original_q = q.lower()
            original_s = item[1]
        else:
            answer += answer_structure(generalize(item[0]), item[1], q) + " "
            items_list.append(generalize(item[0]))

        sentence += generalize(item[0]) + " "

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

        answer += answer_structure(modified_item, original_s, new_q)
        items_list.append(modified_item) 

    if twentyfiveP():
        sentence += random.choice(thanks) + " "

    sentence = sentence[:-1] + "."
    sentence = fix_capitalization(sentence)
    answer = answer.lower()
    entities = entity_structure(sentence, items_list)

    return [sentence, answer, entities]

def full_sample(j):
    return sentence(j)

def output_s(fs):
    f = open(SAMPLES, "w")
    f.write("")
    
    for x in fs:
        f.write(x[0] + "\n")

    f.close()

def output_a(fs):
    f = open(ANSWERS, "w")
    f.write("")

    for x in fs:
        f.write(x[0] + "\n" + x[1] + "\n\n")

    f.close()

def output_e(fs):
    f = open(ENTITIES, "w")
    f.write("")

    for x in fs:
        f.write(x[2] + "\n")

    f.close()

def main(x, restaurant):
    j = open_json(menus, restaurant)
    fs = []
    for i in range(0, x):
        fs.append(full_sample(j))

    output_s(fs)
    output_a(fs)
    output_e(fs)

if __name__ == "__main__":
    # arg1: number of samples
    # arg2: name of restaurant i.e. mcdonalds
    main(int(sys.argv[1]), sys.argv[2])
