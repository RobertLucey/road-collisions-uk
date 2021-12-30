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
    def load_all(region=None, year=None):
        import road_collisions_uk
        return Collisions.from_dir(
            '/opt/road_collisions/',
            region=region,
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
        self.accident_year = int(kwargs['accident_year'])

        self.location_easting_osgr = kwargs['location_easting_osgr']
        self.location_northing_osgr = kwargs['location_northing_osgr']
        self.longitude = kwargs['longitude']
        self.latitude = kwargs['latitude']
        self.police_force = kwargs['police_force']
        self.accident_severity = kwargs['accident_severity']
        self.number_of_vehicles = kwargs['number_of_vehicles']
        self.number_of_casualties = kwargs['number_of_casualties']
        self.date = kwargs['date']
        # skipping day of week as we have date
        self.time = kwargs['time']
        self.local_authority_district = kwargs['local_authority_district']
        self.local_authority_ons_district = kwargs['local_authority_ons_district']
        self.local_authority_highway = kwargs['local_authority_highway']
        self.first_road_class = kwargs['first_road_class']
        self.first_road_number = kwargs['first_road_number']
        self.road_type = kwargs['road_type']
        self.speed_limit = kwargs['speed_limit']
        self.junction_detail = kwargs['junction_detail']
        self.junction_control = kwargs['junction_control']
        self.second_road_class = kwargs['second_road_class']
        self.second_road_number = kwargs['second_road_number']
        self.pedestrian_crossing_human_control = kwargs['pedestrian_crossing_human_control']
        self.pedestrian_crossing_physical_facilities = kwargs['pedestrian_crossing_physical_facilities']
        self.light_conditions = kwargs['light_conditions']
        self.weather_conditions = kwargs['weather_conditions']
        self.road_surface_conditions = kwargs['road_surface_conditions']
        self.special_conditions_at_site = kwargs['special_conditions_at_site']
        self.carriageway_hazards = kwargs['carriageway_hazards']
        self.urban_or_rural_area = kwargs['urban_or_rural_area']
        self.did_police_officer_attend_scene_of_accident = kwargs['did_police_officer_attend_scene_of_accident']
        self.trunk_road_flag = kwargs['trunk_road_flag']
        self.lsoa_of_accident_location = kwargs['lsoa_of_accident_location']

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
