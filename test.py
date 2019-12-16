import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import difflib as df
def compare(t1,t2):
    t1=t1.splitlines()
    t2=t2.splitlines()
    d=df.Differ()
    res=d.compare(t1,t2)
    sen=''
    for x in res:
        if x.startswith("+"):
            sen+=x[1::]
    return sen        
def parse(filen):
    tree = ET.parse(filen)
    root = tree.getroot()
    li=[]
    r1=None
    for parent in root.findall('{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision'):
        tml=[]
        for child in parent:
            if child.tag=='{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                tml.append(child.text)
            if child.tag=='{http://www.mediawiki.org/xml/export-0.10/}text':
                tmp=child.text
                if  tmp==None:
                    break
                re.sub(r'[{}]', '',tmp)
                tmp.strip()
                if r1==None:
                    r1=tmp
                    tml.append(r1)
                else:    
                    tml.append(compare(r1,tmp))
                    r1=tmp
        li.append(tml)
    return li  
def data(li1,li2):
    length1=len(li1)
    length2=len(li2)
    bl=[]
    sp=0
    for x in range(length1):
        ts=li1[x][0]
        tmp=[]
        tmp.append(li1[x][1])
        spd=None
        c=0
        counter=-1
        for i in range(sp,length2):
            if li2[i][0]>=ts:
                if spd==None:
                    sp=i
                    spd=True
                    tmp.append(li2[i][1])
                else:    
                    tmp.append(li2[i][1])
                if c==8:
                    break
                c+=1
                counter=0
        if counter==0:        
            bl.append(tmp)
    return bl
def similarity(lis):
    l=[]
    for x in lis:
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(x)
        t=cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
        t1= np.amax(t[0][1:])
        t2=np.where(t[0][1:] == t1)
        if t1>0.3:
            for k in t2:
                for z in k:
                    print("main sentence\n\n",x[0]) 
                    print("compared\n\n",x[z+1])
                    print("--------end---------------")            
    return l            
l1=parse('tsx.xml')
l2=parse('page.xml')
print(similarity(data(l1,l2)))
