class Vehicles():

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
    def parse(data):
        vehicles = Vehicles()
        if isinstance(data, list):
            for d in data:
                if isinstance(d, dict):
                    vehicles.append(
                        Vehicle(
                            **d
                        )
                    )
                else:
                    raise NotImplementedError()
        elif isinstance(data, dict):
            vehicles.append(
                Vehicle(
                    **data
                )
            )
        else:
            raise NotImplementedError()

        return vehicles


class Vehicle():

    __slots__ = [
        'age_band_of_driver',
        'age_of_driver',
        'age_of_vehicle',
        'driver_home_area_type',
        'driver_imd_decile',
        'engine_capacity_cc',
        'first_point_of_impact',
        'generic_make_model',
        'hit_object_in_carriageway',
        'hit_object_off_carriageway',
        'journey_purpose_of_driver',
        'junction_location',
        'propulsion_code',
        'sex_of_driver',
        'skidding_and_overturning',
        'towing_and_articulation',
        'vehicle_direction_from',
        'vehicle_direction_to',
        'vehicle_leaving_carriageway',
        'vehicle_left_hand_drive',
        'vehicle_location_restricted_lane',
        'vehicle_manoeuvre',
        'vehicle_reference',
        'vehicle_type',
    ]

    def __init__(self, *args, **kwargs):
        self.age_band_of_driver = kwargs['age_band_of_driver']
        self.age_of_driver = kwargs['age_of_driver']
        self.age_of_vehicle = kwargs['age_of_vehicle']
        self.driver_home_area_type = kwargs['driver_home_area_type']
        self.driver_imd_decile = kwargs['driver_imd_decile']
        self.engine_capacity_cc = kwargs['engine_capacity_cc']
        self.first_point_of_impact = kwargs['first_point_of_impact']
        self.generic_make_model = kwargs['generic_make_model']
        self.hit_object_in_carriageway = kwargs['hit_object_in_carriageway']
        self.hit_object_off_carriageway = kwargs['hit_object_off_carriageway']
        self.journey_purpose_of_driver = kwargs['journey_purpose_of_driver']
        self.junction_location = kwargs['junction_location']
        self.propulsion_code = kwargs['propulsion_code']
        self.sex_of_driver = kwargs['sex_of_driver']
        self.skidding_and_overturning = kwargs['skidding_and_overturning']
        self.towing_and_articulation = kwargs['towing_and_articulation']

        self.vehicle_direction_from = kwargs['vehicle_direction_from']
        self.vehicle_direction_to = kwargs['vehicle_direction_to']
        self.vehicle_leaving_carriageway = kwargs['vehicle_leaving_carriageway']
        self.vehicle_left_hand_drive = kwargs['vehicle_left_hand_drive']
        self.vehicle_location_restricted_lane = kwargs['vehicle_location_restricted_lane']
        self.vehicle_manoeuvre = kwargs['vehicle_manoeuvre']
        self.vehicle_reference = kwargs['vehicle_reference']
        self.vehicle_type = kwargs['vehicle_type']

    def serialize(self):
        return {
            'age_band_of_driver': self.age_band_of_driver,
            'age_of_driver': self.age_of_driver,
            'age_of_vehicle': self.age_of_vehicle,
            'driver_home_area_type': self.driver_home_area_type,
            'driver_imd_decile': self.driver_imd_decile,
            'engine_capacity_cc': self.engine_capacity_cc,
            'first_point_of_impact': self.first_point_of_impact,
            'generic_make_model': self.generic_make_model,
            'hit_object_in_carriageway': self.hit_object_in_carriageway,
            'hit_object_off_carriageway': self.hit_object_off_carriageway,
            'journey_purpose_of_driver': self.journey_purpose_of_driver,
            'junction_location': self.junction_location,
            'propulsion_code': self.propulsion_code,
            'sex_of_driver': self.sex_of_driver,
            'skidding_and_overturning': self.skidding_and_overturning,
            'towing_and_articulation': self.towing_and_articulation,
            'vehicle_direction_from': self.vehicle_direction_from,
            'vehicle_direction_to': self.vehicle_direction_to,
            'vehicle_leaving_carriageway': self.vehicle_leaving_carriageway,
            'vehicle_left_hand_drive': self.vehicle_left_hand_drive,
            'vehicle_location_restricted_lane': self.vehicle_location_restricted_lane,
            'vehicle_manoeuvre': self.vehicle_manoeuvre,
            'vehicle_reference': self.vehicle_reference,
            'vehicle_type': self.vehicle_type,
        }
