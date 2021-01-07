import os
import boto3
import io
from .S3AudioObject import S3AudioObject

class AwsS3Resource:

    def __init__(self):
        session = boto3.Session(aws_access_key_id=os.environ['AWS_KEY'],
                                aws_secret_access_key=os.environ['AWS_SECRET'])
        s3 = session.resource('s3')
        self.bucket = s3.Bucket(os.environ['BUCKET_NAME'])

    def getStreamData(self, file_name):
        object = self.bucket.Object(file_name)
        audioStream = io.BytesIO()
        metadata = object.metadata
        object.download_fileobj(audioStream)
        audioData = S3AudioObject(metadata, audioStream.getvalue())
        return audioData

    def removeFile(self, file_name):
        object = self.bucket.Object(file_name)
        object.delete()
