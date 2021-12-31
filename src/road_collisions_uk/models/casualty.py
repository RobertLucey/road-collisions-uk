class Casualties():

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
        casualties = Casualties()
        if isinstance(data, list):
            for d in data:
                if isinstance(d, dict):
                    casualties.append(
                        Casualty(
                            **d
                        )
                    )
                else:
                    raise NotImplementedError()
        elif isinstance(data, dict):
            casualties.append(
                Casualty(
                    **data
                )
            )
        else:
            raise NotImplementedError()

        return casualties


class Casualty():

    __slots__ = [
        'vehicle_reference',
        'casualty_reference',
        'casualty_class',
        'sex_of_casualty',
        'age_of_casualty',
        'age_band_of_casualty',
        'casualty_severity',
        'pedestrian_location',
        'pedestrian_movement',
        'car_passenger',
        'bus_or_coach_passenger',
        'pedestrian_road_maintenance_worker',
        'casualty_type',
        'casualty_home_area_type',
        'casualty_imd_decile',
    ]

    def __init__(self, *args, **kwargs):
        self.vehicle_reference = int(kwargs['vehicle_reference'])
        self.casualty_reference = int(kwargs['casualty_reference'])
        self.casualty_class = int(kwargs['casualty_class'])
        self.sex_of_casualty = int(kwargs['sex_of_casualty'])
        self.age_of_casualty = int(kwargs['age_of_casualty'])
        self.age_band_of_casualty = int(kwargs['age_band_of_casualty'])
        self.casualty_severity = int(kwargs['casualty_severity'])
        self.pedestrian_location = int(kwargs['pedestrian_location'])
        self.pedestrian_movement = int(kwargs['pedestrian_movement'])
        self.car_passenger = int(kwargs['car_passenger'])
        self.bus_or_coach_passenger = int(kwargs['bus_or_coach_passenger'])
        self.pedestrian_road_maintenance_worker = int(kwargs['pedestrian_road_maintenance_worker'])
        self.casualty_type = int(kwargs['casualty_type'])
        self.casualty_home_area_type = int(kwargs['casualty_home_area_type'])
        self.casualty_imd_decile = int(kwargs['casualty_imd_decile'])

    def serialize(self):
        return {
            'vehicle_reference': self.vehicle_reference,
            'casualty_reference': self.casualty_reference,
            'casualty_class': self.casualty_class,
            'sex_of_casualty': self.sex_of_casualty,
            'age_of_casualty': self.age_of_casualty,
            'age_band_of_casualty': self.age_band_of_casualty,
            'casualty_severity': self.casualty_severity,
            'pedestrian_location': self.pedestrian_location,
            'pedestrian_movement': self.pedestrian_movement,
            'car_passenger': self.car_passenger,
            'bus_or_coach_passenger': self.bus_or_coach_passenger,
            'pedestrian_road_maintenance_worker': self.pedestrian_road_maintenance_worker,
            'casualty_type': self.casualty_type,
            'casualty_home_area_type': self.casualty_home_area_type,
            'casualty_imd_decile': self.casualty_imd_decile,
        }
