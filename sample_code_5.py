import pandas as pd
import numpy as np
import nltk
import spacy
from spellchecker import SpellChecker
from spacy.symbols import nsubj, VERB
from collections import Counter

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:  # Done
    de_a = sum(a ** 2) ** (1 / 2)
    de_b = sum(b ** 2) ** (1 / 2)
    if (de_a == 0) or (de_b == 0):
        return 0.0

    sim = sum(a * b) / (de_a * de_b)

    return sim

def score_essay_coherence(essay):
# def score_essay_coherence(essay,filename,df):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(essay)
    embeddings = [sent.vector for sent in doc.sents]
    
    # embeddings = get_sentence_embeddings(essay)
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = cosine_similarity(embeddings[i], embeddings[i + 1])
        similarities.append(sim)
    
    sim_mean = np.mean(similarities)
    std_dev = np.std(similarities)
    scores = [1 if abs(sim - sim_mean) > 3 * std_dev else 
              2 if abs(sim - sim_mean) > 2.5 * std_dev else
              3 if abs(sim - sim_mean) > 2 * std_dev else
              4 if abs(sim - sim_mean) > std_dev else 
              5 for sim in similarities]
    score = np.mean(scores)

    # grade = df[df["filename"] == filename]['grade'].iloc[0]
    # result = pd.DataFrame([{'filename': filename, 'score': score,'grade':grade}])
    # result.to_csv('coherence_scores.csv', mode='a',  index=False)

    return score

    # final_score = 5 - int(np.round(score))  # Assuming 1 is least coherent and 5 most coherent
    
    # return final_score
