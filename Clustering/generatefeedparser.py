import feedparser
import re


def getwords(html) :

    # Remove all the html tags
    txt=re.compile(r'<[^>]+>').sub('',html)

    #Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    return [word.lower() for word in words if word!='']







def getwordcounts(url) :

    # Parsing the feed
    d=feedparser.parse(url)

    wc={}

    # Loop over all the entries
    for e in d.entries :
        if 'summary' in e :
            summary=e.summary
        else :
            summary=e.description
        words=getwords(e.title+' '+summary)

        for word in words :
            wc.setdefault(word,0)
            wc[word]+=1
    try :
     return d.feed.title,wc
    except AttributeError :
     return [None,None]



apcount={}
wordcounts={}
feedlist=[]

for feedurl in file('feedlist.txt') :
    title,wc=getwordcounts(feedurl.strip())
    if title==None : continue
    feedlist.append(feedurl.strip())
    wordcounts[title]=wc
    for word,count in wc.items() :
        apcount.setdefault(word,0)
        if count>1 :
            apcount[word]+=1


wordlist=[]

for w,bc in apcount.items() :
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5 : wordlist.append(w)


out=file('blogdata.txt','w')
out.write('Blog')
for word in wordlist : out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items() :
  out.write(blog.encode('utf-8'))
  for word in wordlist :
    if word in wc : out.write('\t%d' % wc[word])
    else : out.write('\t0')
  out.write('\n')
