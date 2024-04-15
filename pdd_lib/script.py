from bib_pdd_cidacs import BibPddCidacs


client = BibPddCidacs()
client.authentication('/home/marconso/.pdd_cidacs.json')
# dbs = client.list_db()

# print(dbs)

query = """
select * From 1 limit 20
"""

# res_query = client.download(query)
res_query = client.download(query)
