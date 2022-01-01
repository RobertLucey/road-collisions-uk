from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'boto3',
    'road-collisions-base'
)

setup(
    name='road_collisions_uk',
    version='0.0.3',
    python_requires='>=3.6',
    description='Road collision data for the UK',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-uk',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'load_road_collisions_uk = road_collisions_uk.bin.load:main',
        ]
    }
)
