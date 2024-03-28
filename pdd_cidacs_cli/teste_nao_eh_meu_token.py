import cdsapi

c = cdsapi.Client(
    key='8471:29d6d571-c97b-4251-a166-89201e845bab',
    url='https://cds.climate.copernicus.eu/api/v2')

c.retrieve(
    'reanalysis-era5-land',
    {
        'variable': [
            # '10m_u_component_of_wind', '10m_v_component_of_wind',
            # '2m_dewpoint_temperature', '2m_temperature',
            # 'evaporation_from_bare_soil',
            # 'evaporation_from_open_water_surfaces_excluding_oceans',
            # 'evaporation_from_the_top_of_canopy',
            # 'evaporation_from_vegetation_transpiration', 'forecast_albedo',
            # 'lake_bottom_temperature', 'lake_ice_depth',
            # 'lake_ice_temperature', 'lake_mix_layer_depth',
            # 'lake_mix_layer_temperature', 'lake_shape_factor',
            # 'lake_total_layer_temperature', 'leaf_area_index_high_vegetation',
            'leaf_area_index_low_vegetation', 'potential_evaporation',
            # 'runoff', 'skin_reservoir_content', 'skin_temperature',
            # 'snow_albedo', 'snow_cover', 'snow_density', 'snow_depth',
            # 'snow_depth_water_equivalent', 'snow_evaporation', 'snowfall',
            # 'snowmelt', 'soil_temperature_level_1', 'soil_temperature_level_2',
            # 'soil_temperature_level_3', 'soil_temperature_level_4',
            # 'sub_surface_runoff', 'surface_latent_heat_flux',
            # 'surface_net_solar_radiation', 'surface_net_thermal_radiation',
            # 'surface_pressure', 'surface_runoff', 'surface_sensible_heat_flux',
            # 'surface_solar_radiation_downwards',
            # 'surface_thermal_radiation_downwards', 'temperature_of_snow_layer',
            # 'total_evaporation', 'total_precipitation',
            # 'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2',
            # 'volumetric_soil_water_layer_3', 'volumetric_soil_water_layer_4',
        ],
        'year': '2021',
        'month': '12',
        'day': [
            '31',
        ],
        'area': [
            90, -180, -90,
            180,
        ],
        'time': '23:00',
        'format': 'netcdf.zip',
    },
    'download.netcdf.zip')
