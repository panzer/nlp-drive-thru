from test_spacy_ner import OrderSummary, OrderedItem, Modifier
from data_management import input_filepath

# SENTENCES = input_filepath()
# TRUTH = input_filepath()

def main():
    inp = "[apple slices, 2 bags, 2] [burger, , 1] "
    print(OrderSummary.deserialize(inp))

if __name__ == "__main__":
    main()