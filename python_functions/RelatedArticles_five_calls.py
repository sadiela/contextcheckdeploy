from newsapi import NewsApiClient
import random
import requests


def getarticles(inp, orig_url):
    api_key='b6a1f64d144b43c1bba5370b62d879e0'
    #api_key='c1ff125522de4c749e615dca5cba6eb5'
    # Init
    newsapi = NewsApiClient(api_key)

    keyword_str = " ".join(inp[1:]) # REMEMBER TO CHANGE!
    
    pagesize = '50'
    sort='relavency'

    #centerist source call
    url1 = ('http://newsapi.org/v2/everything?'
        f'q={keyword_str}&'
        f'sortBy={sort}&'
        'sources=associated-press&'
        'domains= reuters.com,cbsnews.com,abcnews.go.com,bloomburg.com,cnbc.com,thehill.com,politico.com$'
        f'pageSize={pagesize}&'
        'page = 1&'
        f'apiKey={api_key}')

    response1 = requests.get(url1)
    articles1 = response1.json()

    #skew left source call
    url2 = ('http://newsapi.org/v2/everything?'
        f'q={keyword_str}&'
        f'sortBy={sort}&'
        'sources=cnn&'
        'domains= nytimes.com,theguardian.com,msnbc.com,theatlantic.com,vox.com,washingtonpost.com,huffpost.com,thedailybeast.com&'
        f'pageSize={pagesize}&'
        'page = 1&'
        f'apiKey={api_key}')

    response2 = requests.get(url2)
    articles2 = response2.json()

    #partisan left source call
    url3 = ('http://newsapi.org/v2/everything?'
        f'q={keyword_str}&'
        f'sortBy={sort}&'
        'domains= slate.com,jacobinmag.com,rawstory.com,progressive.org&'
        f'pageSize={pagesize}&'
        'page = 1&'
        f'apiKey={api_key}')

    response3 = requests.get(url3)
    articles3 = response3.json()

    #partisan right source call
    url4 = ('http://newsapi.org/v2/everything?'
        f'q={keyword_str}&'
        f'sortBy={sort}&'
        'sources=fox-news&'
        'domains= dailywire.com,dailycaller.com,nationalreview.com&'
        f'pageSize={pagesize}&'
        'page = 1&'
        f'apiKey={api_key}')

    response4 = requests.get(url4)
    articles4 = response4.json()

    #skew right source call
    url5 = ('http://newsapi.org/v2/everything?'
        f'q={keyword_str}&'
        f'sortBy={sort}&'
        'domains= reason.com,nypost.com,washingtonexaminer.com,freebeacon.com &'
        f'pageSize={pagesize}&'
        'page = 1&'
        f'apiKey={api_key}')

    response5 = requests.get(url5)
    articles5 = response5.json()

    #politcal catagory arrays
    middle = ['']
    sleft = ['']
    sright = ['']
    pleft = ['']
    pright = ['']

    # print(articles1)

 #centristsources
    ap =  'apnews.com'
    re = 'reuters.com'
    cb = 'cbsnews.com'
    ab = 'abcnews.go.com'
    bl = 'bloomburg.com'
    ec = 'economist.com'
    fo = 'forbes.com'
    cc = 'cnbc.com'
    hi = 'thehill.com'
    po = 'politico.com'

    #skew left
    cn = 'cnn.com'
    nt = 'nytimes.com'
    gu = 'theguardian.com'
    ms = 'msnbc.com'
    al = 'theatlantic.com'
    vo = 'vox.com'
    wp = 'washingtonpost.com'
    hp = 'huffpost.com'
    db = 'thedailybeast.com'

    #skew right

    rs = 'reason.com'
    np = 'nypost.com'
    we = 'washingtonexaminer.com'
    fb = 'freebeacon.com'

    #partisan left
    jb = 'jacobinmag.com'
    ra = 'rawstory'
    pr = 'progressive.org'
    sl = 'slate.com'

    #partisan right
    dw ='dailywire.com'
    fn = 'foxnews.com'
    dc = 'dailycaller.com'
    nr = 'nationalreview.com'


    #all urls being sorted from json files into political catagory arrays
    
    try:
        for x in articles1['articles']:
            if x['url'] != orig_url: 
                middle.append({x['title']: x['url']})
    except:
        print(articles1)
    
    try:
        for x in articles2['articles']:
            if x['url'] != orig_url: 
                sleft.append({
                    x['title']: x['url']
                })
    except:
        print(articles1)
    try:
        for x in articles3['articles']:
            if x['url'] != orig_url: 
                pleft.append({
                    x['title']: x['url']
                })
    except:
        print(articles1)
    try:
        for x in articles4['articles']:
            if x['url'] != orig_url:
                pright.append({
                    x['title']: x['url']
                })
    except:
        print(articles1)
    try:
        for x in articles5['articles']:
            if x['url'] != orig_url:
                sright.append({
                    x['title']: x['url']
                })
    except:
        print(articles1)

    # print(pleft)
    # print(sleft)
    # print(middle)
    # print(sright)
    # print(pright)
    #this removes the blank space placeholder for each array
    related = []
    if len(pleft) > 1:
         pleft.remove('')
    if len(sleft) > 1:
        sleft.remove('')
    if len(middle) > 1:
        middle.remove('')
    if len(sright) > 1:
         sright.remove('')
    if len(pright) > 1:
        pright.remove('')

  
    pleft_sor =[]
    sleft_sor=[]
    middle_sor=[]
    sright_sor = []
    pright_sor = []
    #print(pleft)
    
    if pleft == ['']:
        pleft_sor.append({
            'Source': '',              
            'URL': '',
            'Headline': ''
        })
    else:
        pl = {
            jb: 'Jacobin',
            ra: 'Raw Story',
            pr: 'Progressive',
            sl: 'Slate'
        } 
        for x in pleft:
            for title, url in x.items():
                for key, value in pl.items():
                    if key in url:
                        pleft_sor.append({
                            'Source': value,              
                            'URL': url,
                            'Headline': title
                        })

    if sleft == ['']:
        sleft_sor.append({
            'Source': '',              
            'URL': '',
            'Headline': ''
        })
    else: 

        ps = {
            cn: 'CNN',
            nt: 'New York Times',
            gu: 'The Gurdian',
            ms: 'MSNBC',
            al: 'The Atlantic',
            vo: 'VOX',
            wp: 'Washington Post',
            hp: 'Huffington Post',
            db: 'The Daily Beast'

        } 
        for x in sleft:
            for title, url in x.items():
                for key, value in ps.items():
                    if key in url:
                        sleft_sor.append({
                            'Source': value,              
                            'URL': url,
                            'Headline': title
                        })

    if middle == ['']:
        middle_sor.append({
            'Source': '',              
            'URL': '',
            'Headline': ''
        })
    else: 
        md = {
            ap: 'Associated Press',
            re: 'Reuters',
            cb: 'CBC News',
            ab: 'ABC News',
            bl: 'Bloomburg',
            ec: 'Economist',
            fo: 'Forbes',
            cc: 'CNBC',
            hi: 'The Hill',
            po: 'Politico'

        } 

        for x in middle:
            for title, url in x.items():
                for key, value in md.items():
                    if key in url:
                        middle_sor.append({
                            'Source': value,              
                            'URL': url,
                            'Headline': title
                        }) 
    
    if sright == ['']:
        sright_sor.append({
            'Source': '',              
            'URL': '',
            'Headline': ''
        })
    else:                        
        sr = {
        rs: 'Reason',
        np: 'New York Post',
        we: 'Washington Examiner',
        fb: 'Washington Free Beacon',

        } 
        for x in sright:
            for title, url in x.items():
                for key, value in sr.items():
                    if key in url:
                        sright_sor.append({
                            'Source': value,              
                            'URL': url,
                            'Headline': title
                        }) 
                            
    if pright == ['']:
        pright_sor.append({
            'Source': '',              
            'URL': '',
            'Headline': ''
        })
    else: 
        pr = {
            dw: 'The Daily Wire',
            fn: 'Fox News',
            dc: 'The Daily Caller',
            nr: 'National Review',


        } 
        for x in pright:
            for title, url in x.items():
                for key, value in pr.items():
                    if key in url:
                        pright_sor.append({
                            'Source': value,              
                            'URL': url,
                            'Headline':title
                        }) 
                            

     #random selection for each political catagory
    related.append(random.choice(pleft_sor))
    related.append(random.choice(sleft_sor))
    related.append(random.choice(middle_sor))
    related.append(random.choice(sright_sor))
    related.append(random.choice(pright_sor))

    """     for x in related:
        if x == {'Source': '', 'URL': '', 'Headline': ''}:
            x = random.choice(middle_sor)
        if x == {'Source': '', 'URL': '', 'Headline': ''}:
            x = random.choice(sleft_sor) 
        if x == {'Source': '', 'URL': '', 'Headline': ''}:
            x = random.choice(sright_sor)
        if x == {'Source': '', 'URL': '', 'Headline': ''}:
            x = random.choice(pright_sor)
        if x == {'Source': '', 'URL': '', 'Headline': ''}:
            x = random.choice(pleft_sor)  
    """
    #returns array of articles, elements 0-4 is partisan left to partisan right respectively
    return related

# for x in getarticles('how much wood could a woodchuck joe biden'):
#        print (x)

