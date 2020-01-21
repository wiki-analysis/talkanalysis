import xml.etree.ElementTree as ET
import re
import io
import difflib as df
import dateutil.parser
import vandalism

diff=df.Differ()
aa = 0
flag = 0
f = io.open("2t_trail.txt","w+", encoding = "utf-8")
g = io.open("2nm_trail.txt","w+", encoding = "utf-8")
count=0

def refrain(ttext):
    print('refrain')
    ch=[]
    if ('"' in ttext):
        c=re.findall(r'".*?"',ttext)
    for ja in c:
        ch.append(ja)
    return ch

#def revert(ttext):

def modify(ttext):
    c=[]
    ch=[]
    if '"' in ttext:
        c=re.findall((r'".*?"',ttext))
    for ja in c:
        ch.append(ja)
    return ch

def rewrite(ttext):
    c=[]
    if '"' in ttext:
        c=re.findall(r'".*?"',ttext)
    ch=[]
    if c!=None:
     for ja in c:
        ch.append(ja)
    return ch

def POV(ttext):
        ch=[]


        if ('"' in ttext):
            #print('here')
            c=re.findall(r'"(.*?)"',ttext)
            for ja in c:
                ch.append(ja)
            #print('" usinf this ', ch)


        if ('-' in ttext):
            ttext = re.split('[-]', ttext)
            if 'POV' in ttext[0]:
                c =ttext[1]
            else:
                c =ttext[0]
            ch.append(c)
        print('\nPOV ch\n\n', ch)
        return ch
def point (ttext):
    ch=[]
    lttext=ttext.lower()
    flag2=1
    #print('falg is :',flag2)
    if(flag2==1):
        if('removed' in lttext):
            #print("found remoed in ss")
            ch=re.findall(r'"(.*?)"',ttext)
            #print('\nremoved ch: \n',ch)
    return ch
def beremoved(ttext):
    c = []
    if '"' in ttext:
        c = re.findall(r'".*?"', ttext)
    ch = []
    if c != None:
        for ja in c:
            ch.append(ja)
    return ch



def parsef(file):
    ua=0
    global count
    global ch
    global flag
    tree=ET.parse(file)
    root=tree.getroot()
    for x in root.findall("{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision"):
              ursname=''
              usrid=''
              count=count+1
              #print(count)
              flag=0
              s=''
              ch=''
              print(count)
              f.write('\n')
              f.write(str(count))

              f.write('\n')
              for y in x:
                 # if count<=100:
                    if y.tag == "{http://www.mediawiki.org/xml/export-0.10/}contributor":
                        for name in y:
                            if name.tag=='{http://www.mediawiki.org/xml/export-0.10/}username':
                                usrname=name.text
                            if name.tag=='{http://www.mediawiki.org/xml/export-0.10/}id':
                                usrid=name.text
                    if y.tag=="{http://www.mediawiki.org/xml/export-0.10/}timestamp":
                        tts=y.text
                        dateutil.parser.parse(tts)

                    if y.tag=="{http://www.mediawiki.org/xml/export-0.10/}text":

                        if(count==1):
                            ttext=y.text
                            ttext1=y.text

                        else:
                            ttext=y.text
                            if(ttext!=None):
                                s = ttext
                                zline = ttext1.split('\n')
                                for nline in zline:
                                    if nline == ' ':
                                        s = s.replace(nline, ' ')
                                    elif nline in s:
                                        s = s.replace(nline, '')

                            ttext = s
                            ttext1 = ttext1 + ttext
                            ttext = ttext.replace('\n\n\n', '')

                        f.write(ttext)
                        f.write('\n\n')

                        #print(ttext)
                        flag=0
                        if 'POV' in ttext:
                            ch=POV(ttext)
                            for i in ch:
                                 print(i)
                        if 'vandal' in ttext:
                            print('vandalism')
                            v=vandalism.vandal(0,0,tts)
                            if v==1:
                                flag=2
                                print('yes')
                        if 'point of view' in ttext:
                            print('here2')
                            ch=point(ttext)
                        if count==1:
                            print(ttext)
                        elif 'remov' in ttext:
                            if ' be removed ' in ttext:
                                print('br')
                                ch=beremoved(ttext)
                            if ' remove ' in ttext:
                                print('remove')
                                ch=beremoved(ttext)
                            if ' removing ' in ttext:
                                print('ing')
                                ch=beremoved(ttext)

                            elif 'removed' in ttext:
                                print('ed')
                                flag=2

                        elif 'delete' in ttext:
                            ch = beremoved(ttext)

                        elif 'modify' in ttext:
                            ch=modify(ttext)
                        elif 'refrain' in ttext:
                            ch=refrain(ttext)
                        elif 'rewrite' in ttext:
                            ch=rewrite(ttext)
                        elif 'reverted' in ttext:
                            flag=2
                        elif 'erasing' in ttext:
                            ch=beremoved(ttext)
                        ta = mpage(ch, tts, flag, count)
              if (ta-ua)==1:
                            g.write('\nREVISION: \nuser name - ')
                            g.write(usrname)
                            g.write('\nid    ')
                            g.write(usrid)
                            g.write('\nRevision text:\n')
                            g.write(ttext)
              ua=ta

    return ta



def mpage(ch,tts,flag,count):
    global aa
    check=0
    muname=''
    muid=''
    if flag==0:
      nmtree=ET.parse("Book.xml")
      myroot=nmtree.getroot()
      for x1 in myroot.findall("{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision"):
         if flag==0:
                for z in x1:
                    if z.tag == "{http://www.mediawiki.org/xml/export-0.10/}contributor":
                        for name in z:
                            if name.tag == '{http://www.mediawiki.org/xml/export-0.10/}username':
                                muname = name.text
                            if name.tag == '{http://www.mediawiki.org/xml/export-0.10/}id':
                                muid = name.text

                    if z.tag=="{http://www.mediawiki.org/xml/export-0.10/}text":
                        nmtext=z.text
                        ##print(type(nmtext))
                    if z.tag=="{http://www.mediawiki.org/xml/export-0.10/}timestamp":
                        nmts=z.text
                        dateutil.parser.parse(nmts)
                        ##print(ch)
                        if nmts>tts:
                          if nmtext==None:
                                continue
                           ##print(count,ch,'  ',type(ch))
                            ##print('this is timestamp: ',nmts)
                          for e in ch:
                            if (e not in nmtext):
                                check=1
                          if check==1:
                                aa=aa+1
                                flag=1
                                g.write('\n\n\n')
                                g.write(str(count))
                                g.write('\nMAIN PAGE: \nuser name-   ')
                                g.write(muname)
                                g.write('\nid -  ')
                                g.write(muid)
                                g.write('\n Main Page Text:\n')
                                g.write(nmtext)
    if flag==2:
             tree2=ET.parse('nm.xml')
             root2=tree2.getroot()
             for p in root2.findall("{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision"):
                 for z in p:
                     if z.tag == "{http://www.mediawiki.org/xml/export-0.10/}contributor":
                         for name in z:
                             if name.tag == '{http://www.mediawiki.org/xml/export-0.10/}username':
                                 muname = name.text
                             if name.tag == '{http://www.mediawiki.org/xml/export-0.10/}id':
                                 muid = name.text
                     if z.tag=="{http://www.mediawiki.org/xml/export-0.10/}text":
                         nmtext=z.text
             aa=aa+1
             g.write('\n\n\n')
             g.write(str(count))
             g.write('\nMAIN PAGE: \nuser name-   ')
             g.write(muname)
             g.write('\nid -  ')
             g.write(muid)
             g.write('\n Main Page Text:\n')
             g.write(nmtext)
    print("after this revision aa is ",aa)


    return aa


p=parsef('Book_talk.xml')
print('ta finaly is',p)
f.close()
g.close()
