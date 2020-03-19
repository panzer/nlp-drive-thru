import spacy
from pathlib import Path
from data_management import output_filepath

output_dir = output_filepath("spacy_ner")
output_dir = Path(output_dir)

TEST_SET = [
    "A lobster, one cheeseburgers, one desk, and a soda please.",
    "Three orders of McNuggets.",
    "A milkshake",
    "Can I please have a large fries and a large iced coffee",
    "I'll just have two Filet-O-Fish"
]

# test the saved model
print("Loading from", output_dir)
nlp = spacy.load(output_dir)

for test_text in TEST_SET:
    print()
    print(test_text)
    doc = nlp(test_text)
    print([ent.text for ent in doc.ents])
    