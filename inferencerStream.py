from kafka import KafkaConsumer, KafkaProducer
from json import dumps, loads
import io
import soundfile as sf
import logging
import os
import uuid
from inferencer.Adapatask5 import DcaseAdapatask5
from resources.awsS3Resource import AwsS3Resource
from resources.mapper import Mapper
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
        logging.info("New Audio arrived ID %s to consumer %s", fileName, inferencer_identifier)
        try:
            storageData = awsS3.get_stream_data(fileName)
            data, samplerate = sf.read(io.BytesIO(storageData.storage_streamdata))
            startTime = datetime.now()
            result = inferencer.runInferencer(fileName, data, samplerate)
            finishTime = datetime.now()
            duration = finishTime - startTime
            logging.info("Processing Finished for %s with inference time of %s", fileName, duration.total_seconds())
            inference_result = loads(result.to_json())
            mapper = Mapper(inference_result)
            mapper_result = mapper.sendInferenceResultToMapper()
            dataToSend = {'device_info': storageData.storage_metadata, 'inference_result': inference_result,
                          'mapper': mapper_result, "inferencer_name": 'ADAPA2019'}
            logging.info("Sending result :%s to topic inference-event", dataToSend)
            producer.send(os.environ['INFERENCE_EVENT'], value=dataToSend)
            logging.info('Removing audio data from bucket')
            awsS3.remove_file(fileName)
            logging.info("%s Jobs Finished", fileName)
        except Exception as e:
            logging.error('Error: "%s" on Consumer "%s" for file "%s"', str(e), inferencer_identifier, fileName)

except Exception as e:
    logging.error('There was an error while Connecting: %s', str(e))
