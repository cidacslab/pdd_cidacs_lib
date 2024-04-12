from bib_pdd_cidacs import BibPddCidacs


client = BibPddCidacs()
client.authentication('/home/marconso/.pdd_cidacs.json')
dbs = client.list_db()

for db in dbs:
    print(db)

res_query = client.query_db(
    'Casos e óbitos de SRAG no Brasil - 2009 a 2019',
    query='alter table'
)
print(res_query)
