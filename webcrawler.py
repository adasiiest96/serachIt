

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def add_to_index(index,keyword,url):
    if keyword in  index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


def add_page_to_index(index,url,content):
    list_of_keyword = content.split()
    for e in list_of_keyword:
        add_to_index(index,e,url)

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages


    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages

            #Insert Code Here
            for e in graph:
                if page in graph[e]:
                    newrank += (d * ranks[e])/len(graph[e])

            newranks[page] = newrank
        ranks = newranks
    return ranks

def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    return None

def lookup_best(index,keyword,ranks):

    if keyword in index:
        best_url = index[keyword][0]
        maxi = ranks[best_url]

        for url in index[keyword]:
            if ranks[url] > maxi:
                maxi = ranks[url]
                best_url = url
        return best_url
    return None
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    i =0
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            #print content
            add_page_to_index(index,page,content)
            links = get_all_links(content)

            graph[page] = links

            union(tocrawl,links)
            crawled.append(page)
            i = i +1
    return index,graph

index , graph = crawl_web('https:')
ranks = compute_ranks(graph)


#print index
#print ranks
print "Enter END for ending the season"

while True :
    query = raw_input('Enter Your Query >>')
    if query == 'END':
        break
    #print lookup_best(index,query,ranks)
    print lookup(index,query)

