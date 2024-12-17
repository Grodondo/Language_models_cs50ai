import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NP -> N | N N | Det N | Det NP | NP PP | NP Conj NP | Adj NP | NP Adv |
# DP -> Det NP | Det Adj | Det Adv | Det PP | Det Conj Det
# VP -> V | V V | V NP | V DP
# PP -> P NP | P NP Adv
NONTERMINALS = """
S -> NP VP | S Conj S | S Adv | S Adv S | S PP | S PP Adv | S PP Conj S | DP NP
NP -> N | N N | DP N | NP PP | NP Conj NP | ADP NP | NP Adv | 
DP -> Det | Det N | Det ADP | Det Adv | Det PP | Det Conj Det
VP -> V | V V | V NP | V DP
PP -> P NP | P NP Adv
ADP -> Adj | ADP Adj | Adj Adv | Adj PP | Adj Conj Adj

"""
# N V Det Adj Adj Adj

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        print("Parsing sentence...")
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.pytho
    """

    converted_sentence = [word for word in sentence.lower().split()]

    # for word in converted_sentence:
    # if not any(char.isalpha for char in word):
    #    converted_sentence.remove(word)

    converted_sentence = [
        "".join([char for char in word if char.isalpha()])
        for word in converted_sentence
    ]
    print(converted_sentence)

    return converted_sentence


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        # Check for the last "NP" subtrees on the sentence (It wont show "NP" if it contains another "NP" inside of it)
        # print(subtree)
        if not any(
            child_subtree.label() == "NP"
            for child_subtree in subtree.subtrees(lambda t: t != subtree)
        ):
            np_chunks.append(subtree)
            print(subtree)

    return np_chunks


if __name__ == "__main__":
    main()
