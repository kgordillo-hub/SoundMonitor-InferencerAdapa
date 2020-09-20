from kafka import KafkaConsumer

from inferencer.Adapatask5 import Dcase_Adapatask5

inferencer = Dcase_Adapatask5()

consumer = KafkaConsumer('audio_upload_event',
                         group_id='inferencer_group',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest')


for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    print(inferencer.runInferencer(message.value))