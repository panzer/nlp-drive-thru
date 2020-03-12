# CS4120 NLP, Northeastern University 2020

import spacy
from tqdm import tqdm
from spacy.analysis import Token, Doc, Span
from data_management import output_filepath, input_filepath


def main():
    nlp = spacy.load("en_core_web_sm")

    docs = []

    with open(input_filepath("samplesentences.txt")) as f:
        for line in tqdm(f, desc="Parsing dataset"):
            if line.isspace():
                # skip blank lines
                continue
            else:
                doc: Doc = nlp(line)
                docs.append(doc)


    with open(input_filepath("training_tags_out.txt"), "w") as f:
        for doc in docs:  # type: Doc

            def token_info_string(token: Token):
                return f"{token.tag_}/{token.ent_type_}" 
                
            f.write(" ".join([token_info_string(token) for token in doc]))
            f.write("\n")


if __name__ == "__main__":
    main()
