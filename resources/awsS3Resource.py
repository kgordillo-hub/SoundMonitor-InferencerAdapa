import os
import boto3
import io
from .S3AudioObject import S3AudioObject


class AwsS3Resource:

    def __init__(self):
        session = boto3.Session(region_name='us-east-1')
        s3_bucket = session.resource('s3').Bucket(os.environ['BUCKET_NAME'])
        self.bucket = s3_bucket

    def get_stream_data(self, file_name):
        s3_object = self.bucket.Object(file_name)
        audio_stream = io.BytesIO()
        metadata = s3_object.metadata
        s3_object.download_fileobj(audio_stream)
        audio_data = S3AudioObject(metadata, audio_stream.getvalue())
        return audio_data

    def remove_file(self, file_name):
        file = self.bucket.Object(file_name)
        file.delete()
