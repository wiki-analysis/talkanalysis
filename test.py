import xml.etree.ElementTree as ET
import gensim
from scipy import spatial
import numpy as np
import re
import difflib as df
model = gensim.models.Word2Vec.load('doc2vec.model')
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
    l1=[]
    r1=None
    for parent in root.findall('{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision'):
        tml=[]
        tml1=[]
        for child in parent:
            if child.tag=='{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                tml.append(child.text)
                tml1.append(child.text)
            if child.tag=='{http://www.mediawiki.org/xml/export-0.10/}text':
                tmp=child.text
                if  tmp==None:
                    break
                tmp = tmp.lower().strip()
                if r1==None:
                    r1=tmp
                    tml.append(r1)
                    tml1=list(set(r1.split()))
                else:
                    local=compare(r1,tmp)
                    tml.append(local)
                    tml1=list(set(local.split()))
                    r1=tmp
        li.append(tml)
        l1.append(tml1)
    return li,l1  
def data(li1,li2,l1,l2,model):
    length1=len(li1)
    length2=len(li2)
    print(length1,len(l1))
    print(length2,len(l2))
    bl=[]
    bl2=[]
    sp=0
    for x in range(length1):
        ts=li1[x][0]
        tmp=[]
        tmp1=[]
        tmp.append(model.infer_vector(l1[x]))
        tmp1.append(x)
        spd=None
        c=0
        counter=-1
        for i in range(sp,length2):
            if li2[i][0]>=ts:
                if spd==None:
                    sp=i
                    spd=True
                    tmp.append(model.infer_vector(l2[i]))
                    tmp1.append(i)
                else:    
                    tmp.append(model.infer_vector(l2[i]))
                    tmp1.append(i)
                if c==8:
                    break
                c+=1
                counter=0
        if counter==0:        
            bl.append(tmp)
            bl2.append(tmp1)
    return bl,bl2
def similarity(lis,lis1,ml1,ml2):
    c=0
    for x in lis:
        c1=1
        for i in x[1::]:
            if spatial.distance.cosine(x[0],i)<0.2: 
               print("main\n",ml2[lis1[c][c1]][1])
               print("compared\n",ml1[lis1[c][0]][1])
            c1+=1   
        c+=1    
t1=parse('tsx.xml')
t2=parse('page.xml')
t3=data(t1[0],t2[0],t1[1],t2[1],model)
similarity(t3[0],t3[1],t1[0],t2[0])
