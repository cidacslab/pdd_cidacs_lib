# pdd-cidacs-lib

## "apenas um esboço"


* SIM - modulo python

    - SIM.list_db()
    - SIM.get('')
    - SIM.download('')

```
from bib-pdd-cidacs import autenticacao
from bib-pdd-cidacs import SIM

autenticacao(json: List[str|PosixPath|dict|None] = None)

    autenticacao('/home/fulano/meu_token.json')
    autenticacao(Path('/home/fulano/meu_token.json'))
    autenticacao({'usuario:token'})

ex: auth =  {'usuario:token'}

SIM.list_db() # lista views disponiveis
['bonquiolite', 'dengue']

bronquiolite = SIM.get('bronquiolite') # cria um objeto a partir da view
bronquiolite # objeto tipo pdd-cidacs

bronquilite.columns # mostra as colunas da *view*
bronquilite.shape

bronquiolite.download('/home/fulando/Download/dataset.csv') # baixa conteudo do objeto

import pandas as pd
df = pd.read_csv('/home/fulando/Download/dataset.csv') # objeto tipo pandas DataFrame


# seleciona a informaçao selecionando as seeds e sobreescreve o objeto
broquiolite = broquiolite[
    (bronquilite.seed.str.startswith('bb') or
     (bronquilite.seed.str.startswith('10') or
      (bronquilite.seed.str.startswith('j') or
       (bronquilite.seed.str.startswith('r')
] 

broquiolite.count

bronquiolite.ano.distinct().count

filtrado = bronquiolite[(bronquiolite.idade == 12) & (bronquiolite.exemplo == 'exemplo')]

filtrado.download() # baixou filtrado por seed, idade e exemplo

filtrado.show()       # pensando em como implementar
filtrado.display()    # pensando em como implementar
filtrado.head()       # pensando em como implementar
filtrado.tail()       # pensando em como implementar

```
