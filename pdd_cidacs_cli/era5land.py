from datetime import datetime
from cdsapi import Client


class Era5Land():
    def __init__(self, key):
        self._key = key
        self._url = 'https://cds.climate.copernicus.eu/api/v2'

    def validate_time(self, year, month, day, hour):
        try:
            datetime(year, month, day, hour)
        except ValueError as e:
            raise f'ValueError {e}'

    def download(
        self, vars, year, month, day, time, format, area, file=None, fname
    ):
        if not file:
            c = Client(key=self._key, url=self._url)
            data_post = {
                'variable': vars,
                'year': year,
                'month': month,
                'day': day,
                'time': time,
                'area': area,
                'format': format
            }

            c.retrieve(
                'reanalysis-era5-land',
                data_post,
                f'{fname}.netcdf.zip'
            )
