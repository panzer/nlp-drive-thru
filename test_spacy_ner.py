from typing import List, Dict
import spacy
from spacy.analysis import Doc, Token, Span
from pathlib import Path
from data_management import output_filepath
from word2number import w2n
from dataclasses import dataclass, field

output_dir = output_filepath("spacy_ner")
output_dir = Path(output_dir)

TEST_SET = [
    "A lobster, five cheeseburgers, one desk, and a soda please.",
    "Three orders of McNuggets.",
    "A milkshake, which is not on the menu",
    "Can I please have a large fries, four Big Macs, and a large iced coffee",
    "I'll just have two Filet-O-Fish"
]

# test the saved model
print("Loading from", output_dir)
nlp = spacy.load(output_dir)

def find_numbers_in_document(doc: Doc) -> List[int]:
    """ Returns indexes of entities which are numbers in the document """
    result = list()
    for i, ent in enumerate(doc.ents):  # type: (int, Span)
        if ent.label_ == "CARDINAL":
            result.append(i)
    return result

@dataclass
class Modifier:
    name: str

@dataclass
class MenuItem:
    name: str
    available_modifiers: List[Modifier] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name}"

@dataclass
class Restaurant:
    name: str
    menu: List[MenuItem]

@dataclass
class OrderedItem:
    menu_item: MenuItem
    amount: int
    modifier: Modifier

    def __str__(self) -> str:
        return f"{self.menu_item} ({self.amount})"

@dataclass
class OrderSummary:
    ordered_items: List[OrderedItem]

    def __str__(self) -> str:
        return "\n".join(
            [f"- {ordered_item}" for ordered_item in self.ordered_items]
        )


def parse_doc(doc: Doc) -> OrderSummary:
    number_token_indices = find_numbers_in_document(doc)
    ordered_items = list()
    for i, ent in enumerate(doc.ents):  # type: Span
        if ent.label_ == "MENU_ITEM":
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
    return OrderSummary(ordered_items=ordered_items)


for test_text in TEST_SET:
    print()
    print(test_text)
    doc = nlp(test_text)
    print(parse_doc(doc))
    
