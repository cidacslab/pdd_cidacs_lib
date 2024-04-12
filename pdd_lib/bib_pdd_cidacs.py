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
        elif isinstance(PosixPath):
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
                return conn.json()

    def select_db(self, view, limit=100, download=True, filename=None):
        data = {
            'view': view,
            'limit': limit,
            'download': download,
        }
        with Client() as client:
            conn = client.post(url='http://127.0.0.1:8000/select_view',
                               params=data,
                               auth=self._auth)
            if download and filename:
                with open(filename) as fw:
                    for data in conn.iter_raw():
                        fw.write(data)
                return f'Dados salvos em: {filename}'
            return pd.read_json(conn.json())

    def query_db(self, query):
        return
