from sample_code_1 import score_length
from sample_code_1 import score_spelling
from sample_code_2 import score_subject_verb_agreement
from sample_code_2 import score_verb_usage
from sample_code_3 import score_syntactic_form
from sample_code_4 import score_evaluate_essay
from sample_code_5 import score_essay_coherence

import pandas as pd
import os
import glob


def read_text_files(folder_path):
    file_pattern = os.path.join(folder_path, '*.txt')
    text_files = glob.glob(file_pattern)
    
    for file_path in text_files:
        essay_filename = os.path.basename(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            essay = file.read()
            df = pd.read_csv("essays_dataset\index.csv", sep=';')
            # di = score_evaluate_essay(essay,essay_filename, df)
            # score_essay_coherence(essay,essay_filename, df)

            # Calculate and print the scores
            print("\nCalculating scores...")
            # Calculate each score
            a = score_length(essay)
            b = score_spelling(essay)  # Note that this score is on a 0 to 4 scale
            ci = score_subject_verb_agreement(essay)
            cii = score_verb_usage(essay)
            ciii = score_syntactic_form(essay)
            # df = pd.read_csv("essays_dataset\index.csv", sep=';')
            di = score_evaluate_essay(essay,essay_filename, df)
            dii = score_essay_coherence(essay)


            # Print the scores
            print(f"\nLength score (a): {a}")
            print(f"Spelling score (b): {b} (on a scale of 0 to 4)")
            print(f"Subject-Verb agreement score (c.i): {ci}")
            print(f"Verb tense usage score (c.ii): {cii}")
            print(f"Syntactic-form score (c.iii): {ciii}")
            print(f"essay evaluation (di): {di}")
            print(f"Essay Coherence (dii): {dii} ")
            final_score = 2*a - b + ci + cii + 2*ciii + 3*di + dii

            grade = df[df["filename"] == essay_filename]['grade'].iloc[0]
            result = pd.DataFrame([{'filename': essay_filename, 'score': final_score,'grade':grade}])
            result.to_csv('final_scores_spacy_version.csv', mode='a',  index=False)

folder_path = 'essays_dataset\essays'
read_text_files(folder_path)
# used to check code 4 with different similarities

