import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

veri=pd.read_csv('rdany_conversations_2016-03-01.csv')
chat=veri.iloc[:,0:2]
text=chat.iloc[:,1]
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib
import nltk
from nltk.corpus import stopwords
sw=set(stopwords.words('english'))

text1=[]

for i in text:
    if(i != sw):
        i=i.lower()
        if(i != '[start]' and i!= '[voice]' and i!='[document]'): 
            text1.append(i)
text1=[' '.join(text1)]
        
    
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=1000)
X=cv.fit_transform(text1).toarray()  #bagımsız degısken
# üstte kelimelerin cumle içinde ne kadar gectıgını berilten vektor oluşturuldu.
y=text.values #bagımlı degışken
text2=[]
for i in text1:
    if(i=='😀'):
        text2.append(i)


text = str(text1)

wordcloud = WordCloud().generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
