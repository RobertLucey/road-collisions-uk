from road_collisions_base import logger

from road_collisions_uk.models.collision import Collisions


def main():
    print('NOTE: Since UK data is so large, only loading data from 2020')
    collisions = Collisions.load_all(year=2020)

    logger.info('Loaded %s collisions', (len(collisions)))
    logger.info('Do something with the data in the variable \'collisions\'...')

    import pdb; pdb.set_trace()

    pass


if __name__ == '__main__':
    main()
