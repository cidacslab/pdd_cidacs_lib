from bib_pdd_cidacs import BibPddCidacs


client = BibPddCidacs()
client.authentication('/home/marconso/.pdd_cidacs.json')
# dbs = client.list_db()

# print(dbs)

query = """
select * From 1 limit 10
"""

res_query = client.query_db(query=query,
                            download=False,
                            filename='meu_dataset.csv')
print(res_query)
