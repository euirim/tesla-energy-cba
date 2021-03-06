import pandas as pd
import numpy as np
import matplotlib as mpl
import requests
import json
from statistics import mean

SOLAR_DNI_DATA = '../data/us_dni_by_zip_98_09.csv'
IOU_ELECTRICITY_PRICE_DATA = [
    (2013, '../data/iouzipcodes2013.csv'),
    (2017, '../data/iouzipcodes2017.csv')
]
NONIOU_ELECTRICITY_PRICE_DATA = [
    (2013, '../data/noniouzipcodes2013.csv'),
    (2017, '../data/noniouzipcodes2017.csv')
]
SUNROOF_DATA = '../data/project-sunroof-postal_code-12072018.csv'
OUTPUT_FILE = '../data/preprocessed_data.csv'
CENSUS_DATA = '../data/ACS_17_5YR_DP05/ACS_17_5YR_DP05.csv'
ZCTA_DATA = '../data/all_zctas_18.csv'

def get_price_by_zip(df):
    """
    Return avg electricty price by zip code, in the form
    of a list of tuples. 
    """
    zip_prices = {} # zip_code: [price]
    for index, row in df.iterrows(): 
        zip_code = row['zip']
        if zip_code in zip_prices:
            zip_prices[zip_code].append(row['res_rate'])
        else:
            zip_prices[zip_code] = [row['res_rate']]
    
    return list(
        map(lambda x: (x[0], mean(x[1])), list(zip_prices.items()))
    )

def calc_roof_surface_area(row):
    """
    compute median roof surface area (in m^2)
    """
    return row['number_of_panels_median'] * 1.65 * 0.992

def get_sunroof_data(filename):
    df = pd.read_csv(
        filename, 
        dtype={'region_name': str}
    )
    df = df.rename(columns={'region_name': 'zip'})
    dropped_labels = [
        'lat_max', 
        'lat_min', 
        'lng_max', 
        'lng_min', 
        'install_size_kw_buckets_json'
    ]
    df = df.drop(labels=dropped_labels, axis=1)
    df['roof_area_in_msq'] = df.apply(
        lambda row: calc_roof_surface_area(row),
        axis=1
    )
    return df

def get_electricity_data(iou_filename, noniou_filename):
    result = []
    for i in range(len(iou_filename)):
        ioudf = pd.read_csv(iou_filename[i][1], dtype={'zip': str})
        non_ioudf = pd.read_csv(noniou_filename[i][1], dtype={'zip': str})
        edf = pd.concat([ioudf, non_ioudf])
        price_by_zip = pd.DataFrame(
            get_price_by_zip(edf), 
            columns=[
                'zip', 
                'avg_price_per_kwh_{}'.format(iou_filename[i][0])
            ]
        )
        result.append(price_by_zip)

    output = None
    for i in range(len(result) - 1):
        output = pd.merge(
            result[i],
            result[i + 1],
            on='zip'
        )

    return output

def get_solar_dni_data(filename):
    sdf = pd.read_csv(
        filename,
        dtype={'ZCTA5CE10': str}
    )
    sdf = sdf.drop(labels=['_min', '_max', 'AFFGEOID10', 'GEOID10'], axis=1)
    sdf = sdf.rename(
        columns={
            'ZCTA5CE10': 'zip',
            '_mean': 'mean_annual_dni',
            '_std': 'std_annual_dni',
            '_range': 'range_annual_dni',
            '_var': 'var_annual_dni',
            '_median': 'median_annual_dni'
        }
    )
    return sdf

def get_zctas(filename):
    df = pd.read_csv(
        filename,
        dtype={'ZCTA5CE10': str}
    )
    df = df.rename(
        columns={
            'ZCTA5CE10': 'zip'
        }
    )
    return df

def get_census_data(filename):
    labels = [
        'GEO.id2',
        'HC01_VC03',
        'HC02_VC03',
        'HC01_VC109',
        'HC02_VC109',
    ]
    df = pd.read_csv(
        filename,
        header=0,
        skiprows=[1],
        dtype={
            'GEO.id2': str,
            'HC02_VC03': float,
            'HC02_VC109': float,
        },
        usecols=labels,
    )
    df = df.rename(
        columns={
            'GEO.id2': 'zip',
            'HC01_VC03': 'total_pop_2017_estimate',
            'HC02_VC03': 'total_pop_2017_margin',
            'HC01_VC109': 'total_housing_2017_estimate',
            'HC02_VC109': 'total_housing_2017_margin',
        }
    )
    return df

def main():
    zcta_df = get_zctas(ZCTA_DATA)
    sunroof_df = get_sunroof_data(SUNROOF_DATA)
    price_by_zip_df = get_electricity_data(
        IOU_ELECTRICITY_PRICE_DATA, 
        NONIOU_ELECTRICITY_PRICE_DATA
    )
    solar_dni_df = get_solar_dni_data(SOLAR_DNI_DATA)
    census_df = get_census_data(CENSUS_DATA)

    result_df = pd.merge(
        zcta_df,
        sunroof_df,
        on='zip',
        how='left',
    )
    result_df = pd.merge(
        result_df,
        price_by_zip_df,
        on='zip',
        how='left',
    )
    result_df = pd.merge(
        result_df,
        solar_dni_df,
        on='zip',
        how='left',
    )
    result_df = pd.merge(
        result_df,
        census_df,
        on='zip',
        how='left',
    )

    result_df.to_csv(OUTPUT_FILE)

if __name__ == '__main__':
    main()