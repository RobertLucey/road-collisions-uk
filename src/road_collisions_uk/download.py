import os

import boto3
from botocore import UNSIGNED
from botocore.client import Config


def download_data():
    os.makedirs(
        '/opt/road_collisions/uk',
        exist_ok=True
    )

    s3 = boto3.client(
        's3',
        region_name='eu-west-1',
        config=Config(signature_version=UNSIGNED)
    )

    paginator = s3.get_paginator('list_objects')
    for result in paginator.paginate(Bucket='road-collisions-uk'):
        for key in result.get('Contents', []):
            if os.path.exists(os.path.join('/opt/road_collisions/uk', key['Key'])):
                continue
            s3.download_file(
                'road-collisions-uk',
                key['Key'],
                os.path.join('/opt/road_collisions/uk', key['Key'])
            )
            os.utime(
                os.path.join(
                    '/opt/road_collisions/uk',
                    key['Key']
                ),
                (
                    key['LastModified'].timestamp(),
                    key['LastModified'].timestamp()
                )
            )


def ensure_data_downloaded():
    download_data()
