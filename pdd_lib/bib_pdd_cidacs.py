from datetime import datetime
import json
from pathlib import Path, PosixPath
import io
from typing import Union
from httpx import BasicAuth, Client
import pandas as pd
import tqdm


class BibPddCidacs:
    _auth = None

    def authentication(
        self, cred: Union[str | PosixPath | dict | None] = None
    ) -> dict:
        if not cred:
            try:
                self._auth = self._load_auth(
                    Path().home() / '.bib_pdd_cidacs.json'
                )
            except FileNotFoundError:
                raise FileNotFoundError('Você precisa se autenticar')

        elif isinstance(cred, str):
            cred = Path(cred)
            if cred.exists() and cred.is_file():
                self._load_auth(cred)
            else:
                raise FileNotFoundError(
                    'O arquivo não existe ou não foi digitado corretamente.'
                )

        elif isinstance(cred, PosixPath):
            if cred.exists() and cred.is_file():
                self._load_auth(cred)
            else:
                raise FileNotFoundError(
                    'O arquivo não existe ou não foi digitado corretamente.'
                )

        elif isinstance(cred, dict):
            self._auth = BasicAuth(cred['email'], cred['token'])

    def _load_auth(self, filepath: PosixPath) -> dict:
        with open(filepath) as fauth:
            data = json.load(fauth)
            self._auth = BasicAuth(data['email'], data['token'])

    def list_db(self):
        with Client() as client:

            conn = client.get(
                url='http://35.209.112.76:3000/list_db',
                auth=self._auth,
                timeout=None
            )
            if conn.status_code == 200:
                return conn.json()

    def _write_file(self, conn, filename, tqdm_params):
        with open(filename, 'wb') as fwb:
            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in conn.iter_raw(chunk_size=8192):
                    fwb.write(chunk)
                    pb.update(len(chunk))
        return f'Dados salvos em {filename}'

    def query(self, query):
        data = {
            'query': query,
        }
        with Client() as client:
            conn = client.post(
                url='http://35.209.112.76:3000/query',
                params=data,
                auth=self._auth,
                timeout=None
            )
            try:
                return pd.read_json(io.StringIO(conn.json()))
            except ValueError:
                return conn.json()
            
    def shape(self, dataset):
        shape = list()
        querys = ['SELECT COUNT(*) FROM %s'%(str(dataset)), 'SELECT * FROM %s LIMIT 1'%(str(dataset))]
        
        for i in range(2):
            data = {
                'query': querys[i]
            }
            with Client() as client:
                conn = client.post(url='http://35.209.112.76:3000/query',
                                   params=data,
                                   auth=self._auth,
                                   timeout=None
                                   )
                try:
                    if(i == 0): 
                        shape.append(pd.read_json(io.StringIO(conn.json()))['f0_'].to_list()[0])
                    else:
                        shape.append(len(pd.read_json(io.StringIO(conn.json())).columns.to_list()))
                except ValueError:
                    return conn.json()
                
        return shape  
    
    def list_columns(self, dataset):
         data = {
            'query': 'SELECT * FROM %s LIMIT 1'%(str(dataset))
        }
         with Client() as client:
            conn = client.post(url='http://35.209.112.76:3000/query',
                               params=data,
                               auth=self._auth,
                               timeout=None)
            try:
                return pd.read_json(io.StringIO(conn.json())).columns.to_list()
            except ValueError:
                return conn.json()  

    def download(self, query, filename=None):
        data = {
            'query': query,
        }
        with Client() as client:
            with client.stream(
                url='http://35.209.112.76:3000/download',
                params=data,
                auth=self._auth,
                timeout=None,
                method='POST',
            ) as conn:
                total = int(conn.headers.get('content-length', 0))
                tqdm_params = {
                    'desc': filename,
                    'total': total,
                    'miniters': 1,
                    'unit': 'B',
                    'unit_scale': True,
                    'unit_divisor': 1024
                }
                if filename is not None:
                    self._write_file(conn, filename, tqdm_params)
                elif filename is None:
                    date = datetime.now().strftime('%Y-%m-%d')
                    self._write_file(conn,
                                     f'download_pdd_cidacs_{date}.csv',
                                     tqdm_params)
