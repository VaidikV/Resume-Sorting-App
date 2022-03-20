# Vaidik Vadhavana - 21/03/2022

# Refer libraries_needed.txt to download all the necessary libraries.

from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from spacy.matcher import Matcher
import spacy
import re


# ----------------------------------- EXTRACTING INFO FROM PDF -----------------------------------
class ResumeReader:
    def __init__(self, pdf_path, skill_keyword):
        self.name = ""
        self.mobile = 0
        self.email = ""
        self.skills = ""
        self.no_of_skills = 0
        self.education = ""
        self.pdf_path = pdf_path
        self.skill_keyword = skill_keyword

        resume_path = self.pdf_path
        skill_keyword_file = self.skill_keyword
        raw_text = extract_text(resume_path)

        nlp = spacy.load("en_core_web_sm")  # load pre-trained model
        doc = nlp(raw_text)
        noun_chunks = doc.noun_chunks
        stopwords_from_pdf = set(stopwords.words('english'))  # Grad all general stop words
        matcher = Matcher(nlp.vocab)  # initialize matcher with a vocab
        nlp_text = nlp(raw_text)

        # Education Degrees
        degree_keywords = [
            'BE', 'B.E.', 'B.E', 'BS', 'B.S',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'BSc',
            'B.A.', 'BA', 'B.A', 'MBA', 'M.B.A.', 'M.B.A'
        ]

        # ---------- EXTRACTING NAME ----------
        # This function helps in finding a pair of pronouns which are side by side. Used for finding names
        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

        matcher.add("PERSON", [pattern])

        matches = matcher(nlp_text)

        combinations = []
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            combinations.append(span)
        self.name = combinations[0]

        # ---------- EXTRACTING MOBILE NUMBER ----------
        phone = re.findall(re.compile(
            r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9]'
            r'[02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1'
            r'[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'),
            raw_text)

        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                self.mobile = '+' + number
            else:
                self.mobile = number

        # ---------- EXTRACTING EMAIL ----------
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", raw_text)
        if email:
            try:
                self.email = email[0].split()[0].strip(';')
            except IndexError:
                self.email = "Could not extract email."

        # ---------- EXTRACTING SKILLS ----------
        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]
        skills = []
        # reading the txt file
        with open(skill_keyword_file, "r") as file:
            skills_raw = file.read().splitlines()
            for i in skills_raw:
                skills.append(i.lower())
        skillset = []

        # check for one-grams (example: python)
        for token in tokens:
            # print(token)
            if token.lower() in skills:
                skillset.append(token)

        # check for bi-grams and tri-grams (example: machine learning)
        for token in noun_chunks:
            # print(token)
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        skills_list = [i.title() for i in set([i for i in skillset])]
        self.skills = ", ".join(skills_list)
        self.no_of_skills = len(skills_list)

        # ---------- EXTRACTING EDUCATION DEGREE ----------
        # Sentence Tokenizer
        nlp_text = [sent.text for sent in nlp_text.sents]

        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$.!,]', r'', tex)
                if tex.upper() in degree_keywords and tex not in stopwords_from_pdf:
                    edu[tex] = text

        # Extract year
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'((20|19)(\d{2}))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        try:
            self.education = f"{education[0][0]}:- {education[0][1]}"
        except IndexError:
            self.education = "Couldn't extract education details."
