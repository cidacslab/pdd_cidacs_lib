from bib_pdd_cidacs import BibPddCidacs


client = BibPddCidacs()
client.authentication('/home/marconso/.pdd_cidacs.json')
db = client.list_db()

print(db)
print()
print(db['1'])
print()
print(db['6'])
