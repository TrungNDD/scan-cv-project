from calendar import c
from itertools import count
from os import listdir
from tkinter import *
from tkinter import filedialog
import asyncio
import pandas as pd
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

import numpy
from convertPdf2Image import convertPdf2Image

btnFont = ('Be Vietnam', 16)
headerFont = ('Be Vietname Bold', 24, 'bold')

btnWidth = 20

def addApplicant():
    # file type
    filetypes = [
        ('PDF files', '*.pdf')
    ]
    # show the open file dialog
    file = filedialog.askopenfile(mode='rb',filetypes=filetypes)

    if file:
        return convertPdf2Image(file)


def readAllSample():
    listSampleFilename = [filename for filename in listdir('tmp/') if '.txt' in filename]
    contour = []
    for filename in listSampleFilename:
        with open('tmp/'+filename, 'r',encoding='utf8') as file:
            text = file.read()
        
        contour.append({"sample": filename, "content": text})

    #print(contour)
    return contour

criteriaTable = [(1, 'Tốt nghiệp đại học', 5),
                (2, 'Biết tiếng anh', 10),
                (3, 'Sáng tạo', 15),
                (4, 'Tư duy logic', 5),
                (5, 'Chủ động', 10),
                (6, 'Chuyên nghiệp', 14),
                (7, 'Nhiệt tình', 16),]

def simpleMethod():
    contour = readAllSample()
    contourPoints = []

    for c in contour:
        total_point = 0
        for criteria in criteriaTable:
            if criteria[1].lower() in c['content'].lower():
                total_point += criteria[2]
        contourPoints.append({'sample': c['sample'], 'point': total_point})
    
    #print(contourPoints)
    return contourPoints
        
def tfidfMeasure():
    contour = readAllSample()
    total_pairwise_similarity = numpy.ndarray((len(contour)+1, len(contour)+1), numpy.float64)

    contourPoints = []
    for c in contour:
        contourPoints.append({'sample': c['sample'], 'point': 0})

    for criteria in criteriaTable:
        documents = [criteria[1]]

        for c in contour:
            documents.append(c['content'])
                
        tfidf_vectorizer=TfidfVectorizer(use_idf=True)
        tfidf = tfidf_vectorizer.fit_transform(documents)

        #get tfidf vector for first document 
        #first_document_vector=tfidf[0] 

        #print the scores 
        #df = pd.DataFrame(first_document_vector.T.todense(),index=tfidf_vectorizer.get_feature_names_out(), columns=["tfidf"]) 
        #print(df.sort_values(by=["tfidf"],ascending=False).head(20))

        #print(tfidf)
        # no need to normalize, since Vectorizer will return normalized tf-idf
        pairwise_similarity = tfidf * tfidf.T
        
        # print keyword and its score in each records here
        #print(pairwise_similarity.A)

        total_pairwise_similarity += pairwise_similarity.A

    for i in range(len(contourPoints)):
        contourPoints[i]['point'] += total_pairwise_similarity[i+1][0]

    #print(contourPoints)
    return contourPoints