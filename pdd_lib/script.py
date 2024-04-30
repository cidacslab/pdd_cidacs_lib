from pathlib import Path
from bib_pdd_cidacs import BibPddCidacs
from pprint import pprint as print


client = BibPddCidacs()
client.authentication(Path().home() / '.pdd_cidacs.json')
list_db = client.list_db()

for db in list_db:
    shape_cur_db = client.shape(db)
    list_db.update({db: {'shape': shape_cur_db, 'desc': list_db[db]}})

print(list_db)
