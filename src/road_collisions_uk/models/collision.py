import datetime
import os
import tarfile
import glob

import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.generic import (
    GenericObjects,
    GenericObject
)
from road_collisions_base.models.raw_collision import RawCollision


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', RawCollision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext == '.tgz':
            tar = tarfile.open(filepath, "r:gz")
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(os.path.dirname(filepath) + '/**', recursive=True):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv')
                    ).to_dict(orient='records')
                    data.extend(csv_data)
        else:
            raise Exception()

        collisions = Collisions()
        for collision_dict in data:
            obj = Collision.parse(
                collision_dict
            )

            # TODO: filter the object out here by whatever prop params
            # and save some mem

            collisions.append(obj)

        return collisions

    @staticmethod
    def from_dir(dirpath, region=None):
        collisions = Collisions()
        if region is None:
            search_dir = f'{dirpath}/**'
        else:
            search_dir = f'{dirpath}/{region}/**'
        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz'}:
                continue
            collisions.extend(
                Collisions.from_file(
                    filename
                )._data
            )

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
    def load_all(region=None):
        import road_collisions_uk
        return Collisions.from_dir(
            os.path.join(road_collisions_uk.__path__[0], 'resources'),
            region=region
        )


class Collision(GenericObject, RawCollision):

    def __init__(self, **kwargs):
        # keep all the props given as kwargs for the moment
        self.data = kwargs

        super().__init__()

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

    def serialize(self):
        return {
            'id': self.id,
            'lat': self.geo[0],
            'lng': self.geo[1],
            'year': self.year,
            'accident_reference': self.accident_reference,
            'accident_severity': self.accident_severity,
            'age_band_of_casualty': self.age_band_of_casualty,
            'age_band_of_driver': self.age_band_of_driver,
            'age_of_casualty': self.age_of_casualty,
            'age_of_driver': self.age_of_driver,
            'age_of_vehicle': self.age_of_vehicle,
            'bus_or_coach_passenger': self.bus_or_coach_passenger,
            'car_passenger': self.car_passenger,
            'carriageway_hazards': self.carriageway_hazards,
            'casualty_class': self.casualty_class,
            'casualty_home_area_type': self.casualty_home_area_type,
            'casualty_imd_decile': self.casualty_imd_decile,
            'casualty_reference': self.casualty_reference,
            'casualty_severity': self.casualty_severity,
            'casualty_type': self.casualty_type,
            'date': self.date,
            'day_of_week': self.day_of_week,
            'did_police_officer_attend_scene_of_accident': self.did_police_officer_attend_scene_of_accident,
            'driver_home_area_type': self.driver_home_area_type,
            'driver_imd_decile': self.driver_imd_decile,
            'engine_capacity_cc': self.engine_capacity_cc,
            'first_point_of_impact': self.first_point_of_impact,
            'first_road_class': self.first_road_class,
            'first_road_number': self.first_road_number,
            'generic_make_model': self.generic_make_model,
            'hit_object_in_carriageway': self.hit_object_in_carriageway,
            'hit_object_off_carriageway': self.hit_object_off_carriageway,
            'journey_purpose_of_driver': self.journey_purpose_of_driver,
            'junction_control': self.junction_control,
            'junction_detail': self.junction_detail,
            'junction_location': self.junction_location,
            'light_conditions': self.light_conditions,
            'local_authority_district': self.local_authority_district,
            'local_authority_highway': self.local_authority_highway,
            'local_authority_ons_district': self.local_authority_ons_district,
            'location_easting_osgr': self.location_easting_osgr,
            'location_northing_osgr': self.location_northing_osgr,
            'lsoa_of_accident_location': self.lsoa_of_accident_location,
            'number_of_casualties': self.number_of_casualties,
            'number_of_vehicles': self.number_of_vehicles,
            'pedestrian_crossing_human_control': self.pedestrian_crossing_human_control,
            'pedestrian_crossing_physical_facilities': self.pedestrian_crossing_physical_facilities,
            'pedestrian_location': self.pedestrian_location,
            'pedestrian_movement': self.pedestrian_movement,
            'pedestrian_road_maintenance_worker': self.pedestrian_road_maintenance_worker,
            'police_force': self.police_force,
            'propulsion_code': self.propulsion_code,
            'road_surface_conditions': self.road_surface_conditions,
            'road_type': self.road_type,
            'second_road_class': self.second_road_class,
            'second_road_number': self.second_road_number,
            'sex_of_casualty': self.sex_of_casualty,
            'sex_of_driver': self.sex_of_driver,
            'skidding_and_overturning': self.skidding_and_overturning,
            'special_conditions_at_site': self.special_conditions_at_site,
            'speed_limit': self.speed_limit,
            'time': self.time,
            'towing_and_articulation': self.towing_and_articulation,
            'trunk_road_flag': self.trunk_road_flag,
            'urban_or_rural_area': self.urban_or_rural_area,
            'vehicle_direction_from': self.vehicle_direction_from,
            'vehicle_direction_to': self.vehicle_direction_to,
            'vehicle_leaving_carriageway': self.vehicle_leaving_carriageway,
            'vehicle_left_hand_drive': self.vehicle_left_hand_drive,
            'vehicle_location_restricted_lane': self.vehicle_location_restricted_lane,
            'vehicle_manoeuvre': self.vehicle_manoeuvre,
            'vehicle_reference': self.vehicle_reference,
            'vehicle_type': self.vehicle_type,
            'weather_conditions': self.weather_conditions
        }

    @property
    def date(self):
        return self.data['date']

    @property
    def geo(self):
        return [self.data['latitude'], self.data['longitude']]

    @property
    def timestamp(self):
        return datetime.datetime.strptime(
            f'{self.data["date"]} {self.data["time"]}',
            '%d/%m/%Y %I:%M'
        )

    @property
    def year(self):
        return self.timestamp.year

    @property
    def accident_reference(self):
        return self.data['accident_reference']

    @property
    def accident_severity(self):
        return self.data['accident_severity']

    @property
    def accident_year(self):
        return self.data['accident_year']

    @property
    def age_band_of_casualty(self):
        return self.data['age_band_of_casualty']

    @property
    def age_band_of_driver(self):
        return self.data['age_band_of_driver']

    @property
    def age_of_casualty(self):
        return self.data['age_of_casualty']

    @property
    def age_of_driver(self):
        return self.data['age_of_driver']

    @property
    def age_of_vehicle(self):
        return self.data['age_of_vehicle']

    @property
    def bus_or_coach_passenger(self):
        return self.data['bus_or_coach_passenger']

    @property
    def car_passenger(self):
        return self.data['car_passenger']

    @property
    def carriageway_hazards(self):
        return self.data['carriageway_hazards']

    @property
    def casualty_class(self):
        return self.data['casualty_class']

    @property
    def casualty_home_area_type(self):
        return self.data['casualty_home_area_type']

    @property
    def casualty_imd_decile(self):
        return self.data['casualty_imd_decile']

    @property
    def casualty_reference(self):
        return self.data['casualty_reference']

    @property
    def casualty_severity(self):
        return self.data['casualty_severity']

    @property
    def casualty_type(self):
        return self.data['casualty_type']

    @property
    def day_of_week(self):
        return self.data['day_of_week']

    @property
    def did_police_officer_attend_scene_of_accident(self):
        return self.data['did_police_officer_attend_scene_of_accident']

    @property
    def driver_home_area_type(self):
        return self.data['driver_home_area_type']

    @property
    def driver_imd_decile(self):
        return self.data['driver_imd_decile']

    @property
    def engine_capacity_cc(self):
        return self.data['engine_capacity_cc']

    @property
    def first_point_of_impact(self):
        return self.data['first_point_of_impact']

    @property
    def first_road_class(self):
        return self.data['first_road_class']

    @property
    def first_road_number(self):
        return self.data['first_road_number']

    @property
    def generic_make_model(self):
        return self.data['generic_make_model']

    @property
    def hit_object_in_carriageway(self):
        return self.data['hit_object_in_carriageway']

    @property
    def hit_object_off_carriageway(self):
        return self.data['hit_object_off_carriageway']

    @property
    def journey_purpose_of_driver(self):
        return self.data['journey_purpose_of_driver']

    @property
    def junction_control(self):
        return self.data['junction_control']

    @property
    def junction_detail(self):
        return self.data['junction_detail']

    @property
    def junction_location(self):
        return self.data['junction_location']

    @property
    def light_conditions(self):
        return self.data['light_conditions']

    @property
    def local_authority_district(self):
        return self.data['local_authority_district']

    @property
    def local_authority_highway(self):
        return self.data['local_authority_highway']

    @property
    def local_authority_ons_district(self):
        return self.data['local_authority_ons_district']

    @property
    def location_easting_osgr(self):
        return self.data['location_easting_osgr']

    @property
    def location_northing_osgr(self):
        return self.data['location_northing_osgr']

    @property
    def lsoa_of_accident_location(self):
        return self.data['lsoa_of_accident_location']

    @property
    def number_of_casualties(self):
        return self.data['number_of_casualties']

    @property
    def number_of_vehicles(self):
        return self.data['number_of_vehicles']

    @property
    def pedestrian_crossing_human_control(self):
        return self.data['pedestrian_crossing_human_control']

    @property
    def pedestrian_crossing_physical_facilities(self):
        return self.data['pedestrian_crossing_physical_facilities']

    @property
    def pedestrian_location(self):
        return self.data['pedestrian_location']

    @property
    def pedestrian_movement(self):
        return self.data['pedestrian_movement']

    @property
    def pedestrian_road_maintenance_worker(self):
        return self.data['pedestrian_road_maintenance_worker']

    @property
    def police_force(self):
        return self.data['police_force']

    @property
    def propulsion_code(self):
        return self.data['propulsion_code']

    @property
    def road_surface_conditions(self):
        return self.data['road_surface_conditions']

    @property
    def road_type(self):
        return self.data['road_type']

    @property
    def second_road_class(self):
        return self.data['second_road_class']

    @property
    def second_road_number(self):
        return self.data['second_road_number']

    @property
    def sex_of_casualty(self):
        return self.data['sex_of_casualty']

    @property
    def sex_of_driver(self):
        return self.data['sex_of_driver']

    @property
    def skidding_and_overturning(self):
        return self.data['skidding_and_overturning']

    @property
    def special_conditions_at_site(self):
        return self.data['special_conditions_at_site']

    @property
    def speed_limit(self):
        return self.data['speed_limit']

    @property
    def time(self):
        return self.data['time']

    @property
    def towing_and_articulation(self):
        return self.data['towing_and_articulation']

    @property
    def trunk_road_flag(self):
        return self.data['trunk_road_flag']

    @property
    def urban_or_rural_area(self):
        return self.data['urban_or_rural_area']

    @property
    def vehicle_direction_from(self):
        return self.data['vehicle_direction_from']

    @property
    def vehicle_direction_to(self):
        return self.data['vehicle_direction_to']

    @property
    def vehicle_leaving_carriageway(self):
        return self.data['vehicle_leaving_carriageway']

    @property
    def vehicle_left_hand_drive(self):
        return self.data['vehicle_left_hand_drive']

    @property
    def vehicle_location_restricted_lane(self):
        return self.data['vehicle_location_restricted_lane']

    @property
    def vehicle_manoeuvre(self):
        return self.data['vehicle_manoeuvre']

    @property
    def vehicle_reference(self):
        return self.data['vehicle_reference']

    @property
    def vehicle_type(self):
        return self.data['vehicle_type']

    @property
    def weather_conditions(self):
        return self.data['weather_conditions']
