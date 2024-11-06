from bib_pdd_cidacs import BibPddCidacs
from pprint import pprint as print


client = BibPddCidacs()
client.authentication(cred={'email': 'adicione_aqui_seu_belo_email',
                            'token': 'adicione_aqui_seu_token_ultra_secreto'})
list_db = client.list_db()
print(list_db)
