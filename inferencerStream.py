from kafka import KafkaConsumer, KafkaProducer
from json import dumps, loads
import io
import soundfile as sf
import logging
import os
import uuid
from inferencer.Adapatask5 import DcaseAdapatask5
from resources.awsS3Resource import AwsS3Resource
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)
inferencer = DcaseAdapatask5()
awsS3 = AwsS3Resource()
inferencer_identifier = uuid.uuid4().__str__()

try:

    consumer = KafkaConsumer(os.environ['AUDIO_UPLOAD_EVENT'],
                             group_id=os.environ['GROUP_ID'],
                             bootstrap_servers=[os.environ['KAFKA_SERVER']],
                             auto_offset_reset='earliest',
                             enable_auto_commit='true',
                             client_id=inferencer_identifier)
    producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_SERVER']],
                             value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))


    for message in consumer:
        fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
        logging.info("New Audio arrived ID {} to consumer {}".format(fileName, inferencer_identifier))
        try:
            storageData = awsS3.getStreamData(fileName)
            data, samplerate = sf.read(io.BytesIO(storageData.storage_streamdata))
            startTime = datetime.now()
            result = inferencer.runInferencer(fileName, data, samplerate)
            finishTime = datetime.now()
            duration = finishTime - startTime
            logging.info("Processing Finished for {}  with inference time of {}".format(fileName, duration.total_seconds()))
            dataToSend = {'device_info': storageData.storage_metadata, 'inference_result': loads(result.to_json()),
                          "inferencer_name": os.environ['INFERENCER_NAME']}
            logging.info("Sending result :{} to topic inference-event".format(dataToSend))
            producer.send(os.environ['INFERENCE_EVENT'], value=dataToSend)
            logging.info('Removing audio data from bucket')
            awsS3.removeFile(fileName)
            logging.info("{} Jobs Finished".format(fileName))
        except Exception as e:
            logging.error('Error: "{}" on Consumer "{}" for file "{}"'.format(str(e), inferencer_identifier, fileName))

except Exception as e:
    logging.error('There was an error while Connecting: {}'.format(str(e)))
