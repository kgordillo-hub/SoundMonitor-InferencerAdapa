from kafka import KafkaConsumer, KafkaProducer
from json import dumps
import io
import soundfile as sf
from inferencer.Adapatask5 import DcaseAdapatask5
from resources.awsS3Resource import AwsS3Resource
import logging
import os

logging.getLogger().setLevel(logging.INFO)
inferencer = DcaseAdapatask5()
awsS3 = AwsS3Resource()

consumer = KafkaConsumer(os.environ['AUDIO_UPLOAD_EVENT'],
                         group_id=os.environ['GROUP_ID'],
                         bootstrap_servers=[os.environ['KAFKA_SERVER']],
                         auto_offset_reset='earliest')
producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_SERVER']],
                         value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))


for message in consumer:
    fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
    logging.info("New Audio arrived ID {}".format(fileName))
    try:
        data, samplerate = sf.read(io.BytesIO(awsS3.getStreamData(fileName)))
        result = inferencer.runInferencer(fileName, data, samplerate)
        logging.info("Processing Finished for {}".format(fileName))
        logging.info("Sending result file:{} to topic inference-event".format(fileName))
        producer.send(os.environ['INFERENCE_EVENT'], value=result.to_json())
        logging.info("{} Jobs Finished".format(fileName))
    except Exception as e:
        logging.error('There was an error while Processing : {}'.format(str(e)))
