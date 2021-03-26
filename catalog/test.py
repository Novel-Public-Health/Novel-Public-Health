from scholarly import scholarly
# temporary hardcoded in - may wanna test with more examples
# for actual implementation: extract movie title and movie director and feed into scripts
search_query = scholarly.search_pubs('Concussion Peter Landesman')

# prints top 10 results
for i in range(0, 10):
   scholarly.pprint(next(search_query))