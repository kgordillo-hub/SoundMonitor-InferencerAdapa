"""
Main Class of Kafka stream
"""
import io
import logging
import os
import uuid
from datetime import datetime
from json import dumps, loads
import soundfile as sf
from kafka import KafkaConsumer, KafkaProducer
from inferencer.adapa_task5 import DcaseAdapatask5
from resources.aws_s3_resource import AwsS3Resource
from resources.mapper import Mapper

logging.getLogger().setLevel(logging.INFO)
inferencer = DcaseAdapatask5()
awsS3 = AwsS3Resource()
inferencer_identifier = uuid.uuid4().__str__()

try:

    consumer = KafkaConsumer(os.environ['DATA_UPLOAD_EVENT'],
                             group_id=os.environ['GROUP_ID'],
                             bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             auto_offset_reset='earliest',
                             enable_auto_commit='true',
                             client_id=inferencer_identifier)
    producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))


    for message in consumer:
        fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
        logging.info("New Audio arrived ID %s to consumer %s", fileName, inferencer_identifier)
        try:
            storageData = awsS3.get_stream_data(fileName)
            data, samplerate = sf.read(io.BytesIO(storageData.storage_streamdata))
            startTime = datetime.now()
            result = inferencer.run_inferencer(fileName, data, samplerate)
            finishTime = datetime.now()
            duration = finishTime - startTime
            logging.info("Processing Finished for %s with inference time of %s", fileName, duration.total_seconds())
            inference_result = loads(result.to_json())
            dataToSend = {'device_info': storageData.storage_metadata, 'inference_result': inference_result,
                          "inferencer_name": 'adapa', 'inference_time': duration.total_seconds()}
            mapper = Mapper()
            mapper_result = mapper.send_inference_result_mapper(dataToSend)
            dataToSend['mapper'] = mapper_result
            logging.info("Sending result :%s to topic %s", dataToSend, os.environ['PROCESS_RESULT_EVENT'])
            producer.send(os.environ['PROCESS_RESULT_EVENT'], value=dataToSend)
            logging.info("%s Jobs Finished", fileName)
        except Exception as e:
            logging.error('Error: "%s" on Consumer "%s" for file "%s"', str(e), inferencer_identifier, fileName)

except Exception as e:
    logging.error('There was an error while Connecting: %s', str(e))
