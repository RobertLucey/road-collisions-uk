import datetime
import os
import glob
import csv

from pandas import DataFrame
import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.raw_collision import RawCollision

from road_collisions_uk.utils import extract_tgz
from road_collisions_uk.models.vehicle import Vehicles
from road_collisions_uk.models.casualty import Casualties


class Collisions():

    def __init__(self, *args, **kwargs):
        self._data = kwargs.get('data', [])

    def __getitem__(self, i):
        return self._data[i]

    def __iter__(self):
        return (i for i in self._data)

    def __len__(self):
        return len(self._data)

    def append(self, data):
        self._data.append(data)

    def extend(self, data):
        self._data.extend(data)

    def serialize(self):
        return [
            d.serialize() for d in self
        ]

    @staticmethod
    def from_dir(dirpath, region=None, year=None):
        if region is None:
            search_dir = f'{dirpath}/**'
        else:
            search_dir = f'{dirpath}/{region}/**'

        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue

            # TODO: Don't extract every time
            extract_tgz(filename)

        print('Loading accidents')

        accident_data = []
        with open(os.path.join(dirpath, region, 'accident.csv')) as csvfile:
            data = csv.DictReader(csvfile)
            done = 0
            for row in data:
                if year is None or int(row['accident_year']) == year:
                    accident_data.append(row)
                done += 1

        accident_df = DataFrame(accident_data)
        accident_df = accident_df.set_index('accident_reference')

        print('Loaded accidents')

        print('Loading casualties')

        casualty_data = []
        with open(os.path.join(dirpath, region, 'casualty.csv')) as csvfile:
            data = csv.DictReader(csvfile)
            done = 0
            for row in data:
                if year is None or int(row['accident_year']) == year:
                    casualty_data.append(row)
                done += 1

        casualty_df = DataFrame(casualty_data)
        casualty_df = casualty_df.set_index('accident_reference')

        print('Loaded casualties')

        print('Loading vehicles')

        vehicle_data = []
        with open(os.path.join(dirpath, region, 'vehicle.csv')) as csvfile:
            data = csv.DictReader(csvfile)
            done = 0
            for row in data:
                if year is None or int(row['accident_year']) == year:
                    vehicle_data.append(row)
                done += 1

        vehicle_df = DataFrame(vehicle_data)
        vehicle_df = vehicle_df.set_index('accident_reference')

        print('Loaded vehicles')

        print('Parsing collisions')
        collisions = Collisions()
        for index, row in accident_df.iterrows():
            accident_vehicles = vehicle_df.loc[index]
            accident_casualties = casualty_df.loc[index]

            if isinstance(accident_vehicles, pd.core.series.Series):
                vehicles = Vehicles.parse(
                    accident_vehicles.to_dict()
                )
            else:
                vehicles = Vehicles.parse(
                    accident_vehicles.to_dict(orient='records')
                )

            if isinstance(accident_casualties, pd.core.series.Series):
                casualties = Casualties.parse(
                    accident_casualties.to_dict()
                )
            else:
                casualties = Casualties.parse(
                    accident_casualties.to_dict(orient='records')
                )

            row_data = row.to_dict()
            row_data.update({
                'accident_index': index,
                'vehicles': vehicles,
                'casualties': casualties
            })

            collisions.append(
                Collision(
                    **row_data
                )
            )

        print('Finished parsing collisions')

        return collisions

    def filter(self, **kwargs):
        '''
        By whatever props that exist
        '''
        logger.debug('Filtering from %s' % (len(self)))

        filtered = [
            d for d in self if all(
                [
                    getattr(d, attr) == kwargs[attr] for attr in kwargs.keys()
                ]
            )
        ]

        return Collisions(
            data=filtered
        )

    @staticmethod
    def load_all(year=None):
        import road_collisions_uk
        return Collisions.from_dir(
            '/opt/road_collisions/',
            region='uk',
            year=year
        )


class Collision(RawCollision):

    __slots__ = [
        'accident_index',
        'accident_year',
        'location_easting_osgr',
        'location_northing_osgr',
        'longitude',
        'latitude',
        'police_force',
        'accident_severity',
        'number_of_vehicles',
        'number_of_casualties',
        'date',
        'time',
        'local_authority_district',
        'local_authority_ons_district',
        'local_authority_highway',
        'first_road_class',
        'first_road_number',
        'road_type',
        'speed_limit',
        'junction_detail',
        'junction_control',
        'second_road_class',
        'second_road_number',
        'pedestrian_crossing_human_control',
        'pedestrian_crossing_physical_facilities',
        'light_conditions',
        'weather_conditions',
        'road_surface_conditions',
        'special_conditions_at_site',
        'carriageway_hazards',
        'urban_or_rural_area',
        'did_police_officer_attend_scene_of_accident',
        'trunk_road_flag',
        'lsoa_of_accident_location',
    ]

    # Do casualties and vehicles fo in slots?

    def __init__(self, **kwargs):

        self.accident_index = kwargs['accident_index']
        self.accident_severity = int(kwargs['accident_severity'])
        self.accident_year = int(kwargs['accident_year'])

        self.carriageway_hazards = int(kwargs['carriageway_hazards'])
        self.date = kwargs['date']
        self.did_police_officer_attend_scene_of_accident = int(kwargs['did_police_officer_attend_scene_of_accident'])
        self.first_road_class = int(kwargs['first_road_class'])
        self.first_road_number = int(kwargs['first_road_number'])
        self.junction_control = int(kwargs['junction_control'])
        self.junction_detail = int(kwargs['junction_detail'])
        self.latitude = float(kwargs['latitude']) if kwargs['latitude'] != 'NULL' else None
        self.light_conditions = int(kwargs['light_conditions'])
        self.local_authority_district = int(kwargs['local_authority_district'])
        self.local_authority_highway = kwargs['local_authority_highway']
        self.local_authority_ons_district = kwargs['local_authority_ons_district']
        self.location_easting_osgr = int(kwargs['location_easting_osgr']) if kwargs['latitude'] != 'NULL' else None
        self.location_northing_osgr = int(kwargs['location_northing_osgr']) if kwargs['latitude'] != 'NULL' else None
        self.longitude = float(kwargs['longitude']) if kwargs['latitude'] != 'NULL' else None
        self.lsoa_of_accident_location = kwargs['lsoa_of_accident_location']
        self.number_of_casualties = int(kwargs['number_of_casualties'])
        self.number_of_vehicles = int(kwargs['number_of_vehicles'])
        self.pedestrian_crossing_human_control = int(kwargs['pedestrian_crossing_human_control'])
        self.pedestrian_crossing_physical_facilities = int(kwargs['pedestrian_crossing_physical_facilities'])
        self.police_force = int(kwargs['police_force'])
        self.road_surface_conditions = int(kwargs['road_surface_conditions'])
        self.road_type = int(kwargs['road_type'])
        self.second_road_class = int(kwargs['second_road_class'])
        self.second_road_number = int(kwargs['second_road_number'])
        self.special_conditions_at_site = int(kwargs['special_conditions_at_site'])
        self.speed_limit = int(kwargs['speed_limit'])
        self.time = kwargs['time']
        self.trunk_road_flag = int(kwargs['trunk_road_flag'])
        self.urban_or_rural_area = int(kwargs['urban_or_rural_area'])
        self.weather_conditions = int(kwargs['weather_conditions'])

        self.casualties = kwargs['casualties']
        self.vehicles = kwargs['vehicles']

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        if isinstance(data, dict):
            if 'data' in data.keys():
                return Collision(
                    **RawCollision.parse(
                        data
                    ).data
                )
            else:
                # from serialization
                return Collision(
                    **data
                )

    @property
    def id(self):
        return self.data['accident_index']

    @property
    def geo(self):
        return [self.latitude, self.longitude]

    @property
    def timestamp(self):
        return datetime.datetime.strptime(
            f'{self.date} {self.time}',
            '%d/%m/%Y %I:%M'
        )

    def serialize(self):
        return {
            'accident_index': self.accident_index,
            'accident_year': self.accident_year,

            'location_easting_osgr': self.location_easting_osgr,
            'location_northing_osgr': self.location_northing_osgr,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'police_force': self.police_force,
            'accident_severity': self.accident_severity,
            'number_of_vehicles': self.number_of_vehicles,
            'number_of_casualties': self.number_of_casualties,
            'date': self.date,
            'time': self.time,
            'local_authority_district': self.local_authority_district,
            'local_authority_ons_district': self.local_authority_ons_district,
            'local_authority_highway': self.local_authority_highway,
            'first_road_class': self.first_road_class,
            'first_road_number': self.first_road_number,
            'road_type': self.road_type,
            'speed_limit': self.speed_limit,
            'junction_detail': self.junction_detail,
            'junction_control': self.junction_control,
            'second_road_class': self.second_road_class,
            'second_road_number': self.second_road_number,
            'pedestrian_crossing_human_control': self.pedestrian_crossing_human_control,
            'pedestrian_crossing_physical_facilities': self.pedestrian_crossing_physical_facilities,
            'light_conditions': self.light_conditions,
            'weather_conditions': self.weather_conditions,
            'road_surface_conditions': self.road_surface_conditions,
            'special_conditions_at_site': self.special_conditions_at_site,
            'carriageway_hazards': self.carriageway_hazards,
            'urban_or_rural_area': self.urban_or_rural_area,
            'did_police_officer_attend_scene_of_accident': self.did_police_officer_attend_scene_of_accident,
            'trunk_road_flag': self.trunk_road_flag,
            'lsoa_of_accident_location': self.lsoa_of_accident_location,

            'casualties': self.casualties.serialize(),
            'vehicles': self.vehicles.serialize(),
        }
