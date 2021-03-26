from scholarly import scholarly, ProxyGenerator

class Articles:
    def __init__(self, title, url, abstract): 
        self.title = title
        self.url = url
        self.abstract = abstract

    def __str__(self):
        return "Title: %s\nUrl: %s\nAbstract: %s\n" % \
     (self.title, self.url, self.abstract)

def get_research_articles(max_num, num_tries = 3):
   if (num_tries <= 0):
      print('failed to find relevant articles after multiple tries\n')
      return None

   # temporary hardcoded in - may wanna test with more examples
   # for actual implementation: extract movie title and movie director and feed into scripts  
   #search_query = None
   try:
      pg = ProxyGenerator()
      #ip = 'http://lum-customer-hl_a1431ac1-zone-static:r67n4k2l324c@127.0.0.1:24000'
      ip = 'http://lum-customer-hl_a1431ac1-zone-static:r67n4k2l324c@zproxy.lum-superproxy.io:22225'
      pg.SingleProxy(http = ip, https = ip)
      o = scholarly.use_proxy(pg)
      search_query = scholarly.search_pubs('Concussion Peter Landesman Public Health')
      output = ''
      # prints top 10 results
      for i in range(0, max_num):
            curr = next(search_query)
            #scholarly.pprint(curr)
            a = Articles(curr['bib']['title'], curr['pub_url'], curr['bib']['abstract'])
            output += f"<li>\n\t<a href=\"{a.url}\">{a.title}</a>\n\t<br>\n\t<p>{a.abstract}</p>\n</li>\n"

      return output
   except:
      print('failed to find results in search query\n')
      return 'Nope'

output = get_research_articles(10)

print(output)
"""
import requests
s = requests.Session()
addr = "http://lum-customer-hl_a1431ac1-zone-static:r67n4k2l324c@zproxy.lum-superproxy.io:24000"
s.proxies = {
    "http": addr,
    "https": addr,
}
r = s.get("http://lumtest.com/myip.json")
r.raise_for_status()
print(r.json())
"""