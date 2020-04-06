import spacy
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
with open('./training_data/samplesentences.txt', 'r') as f:
    sents = f.read().splitlines()
key_unis = ['with', 'without', 'add', 'no']
for s in range(len(sents)):
    modifiers = []
    if len(sents[s]) > 0:
        tkns = nlp(sents[s])
        print(sents[s])
        print("Modifiers: ")
        for n in range(len(tkns)):
            t = tkns[n]
            #size and immediate modifiers
            if t.dep_ == 'amod':
                #remove 'Good morning'
                if not (n < len(tkns) - 1 and tkns[n+1].dep_ == 'npadvmod'):
                    modifiers.append(t.text)
            #for orders 'with' something TODO: May have to cross reference with menu items to prevent duplicates
            #Ex: sometimes 'with fries' makes 'fries' a modifier 
            elif n != 0 and (t.dep_ == 'pobj' or t.dep_ == 'ROOT') and tkns[n-1].text.lower() in key_unis:
                modifiers.append(tkns[n-1].text.lower() + " " + t.text)
        print(modifiers)
        print('\n')
