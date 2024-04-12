import json
from pathlib import Path, PosixPath
from typing import Union
from httpx import BasicAuth, Client
import pandas as pd


def config_auth(cred: dict) -> None:
    if ('email' not in cred and 'token' not in cred) or \
            ('email' not in cred or 'token' not in cred):
        raise ValueError('Precisa setar valores de email e token válidos')
    else:
        with open(Path().home() / '.bib_pdd_cidacs.json', 'w') as fwauth:
            json.dump(cred, fwauth)


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
        elif isinstance(cred, PosixPath):
            if cred.exists() and cred.is_file():
                self._load_auth(cred)
        elif isinstance(cred, dict):
            self._auth = BasicAuth(cred['email'], cred['token'])

    def _load_auth(self, filepath: PosixPath) -> dict:
        with open(filepath) as fauth:
            data = json.load(fauth)
            self._auth = BasicAuth(data['email'], data['token'])

    def list_db(self):
        with Client() as client:

            conn = client.get(
                url='http://127.0.0.1:8000/list_db',
                auth=self._auth)
            if conn.status_code == 200:
                return list(conn.json().values())

    def _write_file(self, conn, filename):
        if filename is not None:
            with open(filename, 'wb') as fwb:
                for chunk in conn.iter_raw():
                    fwb.write(chunk)
            return f'Dados salvos em {filename}'

    def query_db(self,
                 view,
                 query='',
                 limit=100,
                 download=False,
                 filename=None):
        data = {
            'view': view,
            'limit': limit,
            'query': query,
        }
        with Client() as client:
            conn = client.post(url='http://127.0.0.1:8000/query',
                               params=data,
                               auth=self._auth)
            if download is True and filename is not None:
                self._write_file(conn, filename)
            elif download is True and filename is None:
                self._write_file(conn, view.replace(' ', '_').lower())
            if limit >= 1000:
                return {'Ui':
                        'Será que você da conta de tudo isso em memória? ;|'}
            try:
                return pd.read_json(conn.json())
            except ValueError:
                return conn.json()
