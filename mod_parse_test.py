import spacy
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")
with open('./training_data/samplesentences.txt', 'r') as f:
    sents = f.read().splitlines()
for s in range(len(sents)):
    if len(sents[s]) > 0:
        tkns = nlp(sents[s])
        print(sents[s])
        print("Modifiers: ")
        for t in tkns:
            if t.dep_ == 'amod':
                print(t.text)
        print('\n')
