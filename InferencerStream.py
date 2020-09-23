from kafka import KafkaConsumer

from inferencer.Adapatask5 import DcaseAdapatask5

inferencer = DcaseAdapatask5()

consumer = KafkaConsumer('audio-upload-event',
                         group_id='inferencer-group',
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest')


for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    print(inferencer.runInferencer(message.value.decode('utf-8')))
