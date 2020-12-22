from inferencer.Adapatask5 import DcaseAdapatask5
import io
import soundfile as sf
import os
import boto3

session = boto3.Session(
    aws_access_key_id=os.environ['AWS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET']
)

s3 = session.resource('s3')

bucket = s3.Bucket('sistemamonitoreoacustico')
object = bucket.Object('00_000066.wav')
audioStream = io.BytesIO()
object.download_fileobj(audioStream)

inferencer = DcaseAdapatask5()

audio = audioStream.getvalue()

data, samplerate = sf.read(io.BytesIO(audio))

result = inferencer.runInferencer(data, samplerate)

print(result)