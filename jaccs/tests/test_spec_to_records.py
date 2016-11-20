import collections

import pytest

import jaccs


@pytest.fixture(scope='session')
def usgs_json():
    return {
        "type": "FeatureCollection",
        "metadata": {
            "generated": 1479531393000,
            "url": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
            "title": "USGS All Earthquakes, Past Hour",
            "status": 200,
            "api": "1.5.2",
            "count": 1
        },
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "mag": 4.7,
                    "place": "152km SE of Taron, Papua New Guinea",
                    "time": 1479529250060,
                    "updated": 1479530318040,
                    "tz": 600,
                    "url": "http://earthquake.usgs.gov/earthquakes/eventpage/us10007ads",
                    "detail": "http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us10007ads.geojson",
                    "felt": None,
                    "cdi": None,
                    "mmi": None,
                    "alert": None,
                    "status": "reviewed",
                    "tsunami": 0,
                    "sig": 340,
                    "net": "us",
                    "code": "10007ads",
                    "ids": ",us10007ads,",
                    "sources": ",us,",
                    "types": ",cap,geoserve,origin,phase-data,",
                    "nst": None,
                    "dmin": 2.249,
                    "rms": 0.67,
                    "gap": 85,
                    "magType": "mb",
                    "type": "earthquake",
                    "title": "M 4.7 - 152km SE of Taron, Papua New Guinea"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        154.1414,
                        -5.2813,
                        153.07
                    ]
                },
                "id": "us10007ads"
            }
        ]
    }


def test_spec_to_records(usgs_json):
    spec = {
        'place': '_.features[0].properties.place',
        'mag': '_.features[0].properties.mag',
        'longitude': {'expr': '_.features[0].geometry.coordinates[0]'},
        'latitude': {'expr': '_.features[0].geometry.coordinates[1]'},
        'nope': {'expr': '_.nope', 'use_default': True, 'default': 'default'}
    }

    records = jaccs.spec_to_records(spec, [usgs_json])

    assert isinstance(records, collections.Iterator)
    assert list(records) == [{
        'place': '152km SE of Taron, Papua New Guinea',
        'mag': 4.7,
        'longitude': 154.1414,
        'latitude': -5.2813,
        'nope': 'default'
    }]
