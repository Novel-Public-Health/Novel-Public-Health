from scholarly import scholarly

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
      print('failed to find results in search query\ntrying again...\n')
      num_tries -= 1
      return get_research_articles(max_num, num_tries)

output = get_research_articles(10)

print(output)