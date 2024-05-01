# # # filename;prompt;grade
# # import pandas as pd
# # data = pd.read_csv('essays_dataset/index.csv', sep=';')
# # print(data)
# # # See the df of csv

# # (d.i) Does the essay address the topic?

import spacy
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize

def load_csv(csv_path):
    return pd.read_csv(csv_path, sep=';')

def get_vector(text):
    nlp = spacy.load('en_core_web_md')
    doc = nlp(text)
    vectors = [token.vector for token in doc if not token.is_stop and not token.is_punct and token.has_vector]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(300)

def cosine_similarity(vec1, vec2):
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def score_evaluate_essay(essay, filename, df):
    prompt = df[df['filename'] == filename]['prompt'].values[0]
    prompt_sentence = sent_tokenize(prompt)[1] 

    essay_vector = get_vector(essay)
    prompt_vector = get_vector(prompt_sentence)

    similarity = cosine_similarity(essay_vector, prompt_vector)

    if similarity < 0.70:
        score = 1
    elif similarity < 0.80:
        score = 2
    elif similarity < 0.90:
        score = 3
    elif similarity < 0.95:
        score = 4
    else:
        score = 5

    grade = df[df["filename"] == filename]['grade'].iloc[0]
    result = pd.DataFrame([{'filename': filename, 'sim':similarity, 'score': score,'grade':grade}])
    result.to_csv('sim_scores_sparcy.csv', mode='a',  index=False)
    return score

