import ee
import pandas as pd
import os

def initialize_ee():
    ee.Initialize()

def download_point_timeseries(site_id, lat, lon,
                              start_date, end_date,
                              out_path):

    point = ee.Geometry.Point([lon, lat])

    bands = [
        'B1','B2','B3','B4','B5','B6','B7',
        'B8','B8A','B11','B12','SCL'
    ]

    s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(point)
            .filterDate(start_date, end_date)
            .select(bands))

    def extract(img):
        utc_time = ee.Date(img.get('system:time_start'))
        local_time = utc_time.advance(lon * 4, 'minute')

        reduced = img.reduceRegion(
            ee.Reducer.first(), point, scale=10, maxPixels=1e6
        )

        return ee.Feature(point, {
            'site_id': site_id,
            'datetime_utc': utc_time.format("YYYY-MM-dd'T'HH:mm"),
            'datetime_local': local_time.format("YYYY-MM-dd HH:mm"),
            'satellite': img.get('SPACECRAFT_NAME'),
            'system_index': img.id(),

            'obs_SZA': img.get('MEAN_SOLAR_ZENITH_ANGLE'),
            'obs_SAA': img.get('MEAN_SOLAR_AZIMUTH_ANGLE'),
            'obs_VZA': img.get('MEAN_INCIDENCE_ZENITH_ANGLE_B8'),
            'obs_VAA': img.get('MEAN_INCIDENCE_AZIMUTH_ANGLE_B8'),

            'B01': reduced.get('B1'),
            'B02': reduced.get('B2'),
            'B03': reduced.get('B3'),
            'B04': reduced.get('B4'),
            'B05': reduced.get('B5'),
            'B06': reduced.get('B6'),
            'B07': reduced.get('B7'),
            'B08': reduced.get('B8'),
            'B8A': reduced.get('B8A'),
            'B11': reduced.get('B11'),
            'B12': reduced.get('B12'),

            'SCL': reduced.get('SCL')
        })

    features = s2.map(extract)
    records = [f['properties'] for f in features.getInfo()['features']]
    df = pd.DataFrame(records)

    df = reorder_columns(df)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return df


def reorder_columns(df):

    ordered_cols = [
        'site_id',
        'datetime_utc',
        'datetime_local',
        'satellite',
        'system_index',
        'obs_SZA', 'obs_SAA',
        'obs_VZA', 'obs_VAA',
        'B01','B02','B03','B04','B05','B06','B07',
        'B08','B8A','B11','B12',
        'SCL'
    ]

    return df[ordered_cols]