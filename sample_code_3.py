import pandas as pd
import numpy as np
import nltk
import spacy
from spellchecker import SpellChecker
from spacy.symbols import nsubj, VERB
from collections import Counter

def score_syntactic_form(essay):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(essay)
    errors = 0
    # sentence_list = []
    token_list = []
    for sentence in doc.sents:
        # print("Next Sentence:")
        # print(sentence)
        # print("\n")
        has_main_verb = False 
        sentence_start = sentence[0]
        has_aux = False
        has_subordinating_conj = False
        if sentence[-1].text == "?":
            # For question sentences
            if sentence_start.pos_ not in ["AUX", "VERB"] and sentence_start.tag_ not in ["WDT", "WP", "WP$", "WRB"]:
                errors += 0.1
                # print(f"Error: Question sentence does not start with an auxiliary or WH-word.")
        else:
            if sentence[-1].text not in [".", "!"]:
                errors += 0.1
                # print(f"Error: Non-question sentence does not end with proper punctuation.")
            
            # For declarative sentence starting incorrectly
            if sentence_start.pos_ == "VERB":
                errors += 0.1
                # print(f"Error: Declarative sentence starts with a verb.")
            elif sentence_start.pos_ not in ["NOUN", "PROPN", "ADP", "ADV"] and sentence_start.dep_ not in ["mark"]:
                errors += 0.1
                # print(f"Error: Declarative sentence does not start with a likely NP, PP, Adverb, or subordinate clause.")

        for token in sentence:
            # print(f"{token.text} ({token.tag_}, {token.dep_})")
            if token.dep_ == "mark":
                has_subordinating_conj = True
                if not any(t.dep_ == "VERB" for t in sentence[token.i+1:]):
                    errors += 0.5
                    # print("Subordinating conjunction without following main verb.")

            # Check modal and main verbs
            if token.tag_ == "MD":
                has_aux = True
            if token.pos_ == "VERB" and token.dep_ not in ["aux", "auxpass"]:
                has_main_verb = True

            # Handling errors with modal verbs not followed by a main verb
            if has_aux and token.pos_ == "VERB" and not has_main_verb:
                errors += 0.5
                # print("Error: not modal verb + main verb")
            # Ensuring a main verb if modal is used
            if has_aux and token == sentence[-1] and not has_main_verb:
                errors += 0.5
                # print("Error: modal used, no main verb")
            # Noun checks for determiners
            if token.pos_ == "NOUN":
                prev_token = doc[token.i - 1] if token.i > 0 else None
                if token.tag_ == "NNS": 
                    continue
                elif not (prev_token and prev_token.tag_ in ["DT"]):
                    errors += 0.5
                    # print(token.text)
                    # print("not plural need determiner")
            if token.pos_ == "PROPN":
                # check 专有名词 
                prev_token = doc[token.i - 1] if token.i > 0 else None
                if prev_token and prev_token.tag_ in ["DT"]:
                    errors += 0.5
                    # print("Error: PROPN does not need determiner")

            if token.pos_ == "ADP": # 介词
                next_token = doc[token.i + 1] if token.i + 1 < len(doc) else None
                if next_token and next_token.pos_ in ["NOUN", "PROPN"]:
                    prev_token = doc[next_token.i - 1] if next_token.i > 0 else None
                    if prev_token and prev_token.tag_ in ["DT"]:
                        errors += 0.1
                        # print("Error: noun/PROPN do not need determiner after ADP")

        if not has_main_verb:
            errors += 1
        #     print("Error: no main verb in the sentence")
        # print("Updated Error Count:", errors)

        # return token_list
    # return errors
    num_sentences = len(list(doc.sents))
    score = max(5 - (errors / num_sentences if num_sentences > 0 else 0), 1)
    return round(score, 2)  # Rounded to two decimal places

    # return sentence_list
    # return token_list