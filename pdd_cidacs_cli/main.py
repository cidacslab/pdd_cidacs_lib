from datetime import datetime
import re
import click

from era5land import Era5Land


args_variables = [
    '2m_dewpoint_temperature',
    '2m_temperature',
    'skin_temperature',
    'soil_temperature_level_1',
    'soil_temperature_level_2',
    'soil_temperature_level_3',
    'soil_temperature_level_4',
    'lake_bottom_temperature',
    'lake_ice_depth',
    'lake_ice_temperature',
    'lake_mix_layer_depth',
    'lake_mix_layer_temperature',
    'lake_shape_factor',
    'lake_total_layer_temperature',
    'snow_albedo',
    'snow_cover',
    'snow_density',
    'snow_depth',
    'snow_depth_water_equivalent',
    'snowfall',
    'snowmelt',
    'temperature_of_snow_layer',
    'skin_reservoir_content',
    'volumetric_soil_water_layer_1',
    'volumetric_soil_water_layer_2',
    'volumetric_soil_water_layer_3',
    'volumetric_soil_water_layer_4',
    'forecast_albedo',
    'surface_latent_heat_flux',
    'surface_net_solar_radiation',
    'surface_net_thermal_radiation',
    'surface_sensible_heat_flux',
    'surface_solar_radiation_downwards',
    'surface_thermal_radiation_downwards',
    'evaporation_from_bare_soil',
    'evaporation_from_open_water_surfaces_excluding_oceans',
    'evaporation_from_the_top_of_canopy',
    'evaporation_from_vegetation_transpiration',
    'potential_evaporation',
    'runoff',
    'snow_evaporation',
    'sub-surface_runoff',
    'surface_runoff',
    'total_evaporation',
    '10m_u_component_of_wind',
    '10m_v_component_of_wind',
    'surface_pressure',
    'total_precipitation',
    'leaf_area_index,_high_vegetation',
    'leaf_area_index,_low_vegetation',
]

args_years = [str(year) for year in range(1950, datetime.now().year)]
args_months = [f'{month:02d}' for month in range(1, 13)]
args_days = [f'{day:02d}' for day in range(1, 32)]
args_time = [f'{time:02d}:00' for time in range(0, 24)]
args_format = ['netcdf.zip', 'grib', 'netcdf']
args_area = ['N', 'S', 'W', 'E']


@click.group()
def cli():
    ...


@click.command()
@click.option('--add_token', help='Your Token (Era5-land)')
def add_token(add_token):
    click.echo(f'token: {add_token=}')


@click.command()
@click.option('-v',
              '--variable',
              multiple=True,
              help='\n'.join(args_variables)
              )
@click.option('-y',
              '--year',
              # multiple=True,
              help='\n'.join(args_years))
@click.option('-m',
              '--month',
              # multiple=True,
              help='\n'.join(args_months))
@click.option('-d',
              '--day',
              # multiple=True,
              help='\n'.join(args_days))
@click.option('-t',
              '--time',
              # multiple=True,
              help='\n'.join(args_time)
              )
@click.option('-f',
              '--format',
              # multiple=True,
              help='\n'.join(args_format)
              )
@click.option('-a',
              '--area',
              multiple=True,
              help='\n'.join(args_area)
              )
@click.option('--file',
              help='Path to config file (.json)'
              )
def download(
    variable,
    year,
    month,
    day,
    time,
    format,
    area,
    file
):
    era5 = Era5Land('8471:29d6d571-c97b-4251-a166-89201e845bab')
    var_times = list(map(lambda x: int(x.split(':')[0]),
                         [year, month, day, time]))

    era5.validate_time(*var_times)

    if len(variable) == 1:
        variable = ','.join(variable[0]).split(',')
    if len(variable) > 1:
        variable = ','.join(variable).split(',')

    if len(area) == 1:
        area = ','.join(area[0]).split(',')
    if len(area) > 1:
        area = ','.join(area).split(',')

    click.echo('''parametros:
            {}, {}, {}, {}, {}, {}, {}, {}
    '''.format(variable, year, month, day, time, format, area, file))

    print(variable, year, month, day, time, format, area, file)
    era5.download(variable, year, month, day, time, format, area, file=file)


cli.add_command(add_token)
cli.add_command(download)


if __name__ == '__main__':
    cli()
