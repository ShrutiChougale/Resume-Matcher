import pandas as pd

skills = pd.read_csv("skills.csv")["skill"].tolist()

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in skills if skill in text]
    return list(set(found))
