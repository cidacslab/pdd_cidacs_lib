from datetime import datetime
import json
from pathlib import Path, PosixPath
from typing import Union
from httpx import BasicAuth, Client
import pandas as pd
import tqdm


class BibPddCidacs:
    _host = 'http://35.209.112.76:3000'
    _auth = None
    _client = Client(base_url=_host)

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
        conn = self._client.get(
            '/list_db',
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
            'query': query
        }
        conn = self._client.post(
            url='/query',
            json=data,
            auth=self._auth,
            timeout=None
        )

        try:
            return pd.DataFrame(conn.json()['rows'])
        except (ValueError, KeyError):
            return conn.json()

    def shape(self, dataset):
        data = {
            'query': str(dataset)
        }
        conn = self._client.post(
            '/shape',
            json=data,
            auth=self._auth,
            timeout=None
        )
        try:
            return conn.json()
        except ValueError:
            return conn.json()

        # return pd.DataFrame(conn.json()['rows'])

    def list_columns(self, dataset):
        data = {
            'query': f'SELECT * FROM {dataset} LIMIT 1'
        }
        conn = self._client.post('/query',
                                 json=data,
                                 auth=self._auth,
                                 timeout=None)
        try:
            return list(conn.json()['rows'][0].keys())
        except ValueError:
            return conn.json()

    def download(self, query, filename=None):
        data = {
            'query': query,
        }
        with self._client.stream(
            url='/download',
            json=data,
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
