import xml.etree.ElementTree as ET
import dateutil.parser


def vandal(c,vcount,tt):
    v=0
    print('c')
    byte=[]
    count=0
    i=0
    tree = ET.parse('nm.xml')
    root=tree.getroot()
    for x in root.findall("{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision"):
        count=count+1
        for z in x:
          if(c==0):
            if z.tag=='{http://www.mediawiki.org/xml/export-0.10/}timestamp':
                tz=z.text
                dateutil.parser.parse(tz)
                if tt<tz:
                    print('here')
                    v=vandal1(count)
                    print('v is ',v)
                    return v


def vandal1(vcount):
    v=0
    print('here2 ',vcount)
    count = 0
    tree = ET.parse('nm.xml')
    root = tree.getroot()
    for x in root.findall("{http://www.mediawiki.org/xml/export-0.10/}page/{http://www.mediawiki.org/xml/export-0.10/}revision"):
        count = count + 1
        if (vcount-10<=count and count<=vcount+10):
          print(count)
          for z in x:
            if z.tag=='{http://www.mediawiki.org/xml/export-0.10/}text':
                print('text')
                if count==vcount-10:
                    b=z.attrib['bytes']
                    print(b)
                    b=int(b)
                    print('int of b ',b)
                else:
                    b1=z.attrib['bytes']
                   # print(b1)
                    b1=int(b1)
                    print('int of b1 ',b1)
                    b1=b1-b
                    if b1<0:
                        b1=0-b1
                    print('diff ',b1)
                    if (b1>1000):
                        print('vandal')
                        v=1
                        return v
    return v
