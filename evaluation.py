from typing import List
import spacy
from test_spacy_ner import OrderSummary, OrderedItem, Modifier, MenuItem, find_numbers_in_document
from spacy.analysis import Doc, Token, Span
from data_management import input_filepath, output_filepath
from pathlib import Path
from word2number import w2n

output_dir = output_filepath("spacy_ner")
output_dir = Path(output_dir)

# test the saved model
print("Loading from", output_dir)
nlp = spacy.load(output_dir)

SENTENCES = "madlib/samples.txt"
TRUTH = "madlib/answers.txt"

def parse_sentence(sentence: str) -> OrderSummary:
    doc: Doc = nlp(sentence)
    print(doc.text)
    number_token_indices = find_numbers_in_document(doc)
    ordered_items = list()
    for i, ent in enumerate(doc.ents):  # type: Span
        if ent.label_ == "MENU_ITEM":
            print(ent)
            absolute_difference_function = lambda list_value : abs(list_value - i)
            try:
                # Get the nearest cardinal number (and remove from the available list after)
                # This assumes no two menu items use the same token/entity to specify their quantity
                # Also assumes quantity comes before menu item
                closest_num_token_idx = min(number_token_indices, key=absolute_difference_function)

                # Enforce quantity must come before menu item
                if closest_num_token_idx < i:
                    number_token_indices.remove(closest_num_token_idx)

                    num_span: Span = doc.ents[closest_num_token_idx]
                    quantity = w2n.word_to_num(num_span.text)
                else:
                    raise ValueError
            except ValueError:
                quantity = 1

            ordered_items.append(OrderedItem(
                menu_item=MenuItem(
                    name=ent.text,
                ),
                amount=quantity,
                modifier=Modifier(
                    name="",
                ),
            ))
    return OrderSummary(
        ordered_items=overwrite_duplicate_ordered_items(ordered_items)
    )

def overwrite_duplicate_ordered_items(ordered_items: List[OrderedItem]) -> List[OrderedItem]:
    ret_val = []
    added_indexes = []
    for i, item_a in enumerate(ordered_items):  # type: (int, OrderedItem)
        print(item_a)
        added = False
        for j, item_b in enumerate(ordered_items[i+1:], start=i+1):  # type: (int, OrderedItem)
            
            print(item_b)
            if item_a.menu_item.name == item_b.menu_item.name and j not in added_indexes:
                ret_val.append(item_b)
                added = True
                added_indexes.append(j)
                break

        if not added and i not in added_indexes:
            ret_val.append(item_a)
            added_indexes.append(i)
    return ret_val

def main():
    with open(SENTENCES) as f:
        sentences = f.read().splitlines()
    
    PREDICTIONS = output_filepath("predictions.txt")
    with open(PREDICTIONS, "w") as f:
        for sentence in sentences:
            order: OrderSummary = parse_sentence(sentence)
            f.write(f"{order.serialize()}\n")

        with open()

if __name__ == "__main__":
    main()