from kafka import KafkaConsumer

consumer = KafkaConsumer('dummy',
                         group_id='my-group',
                         bootstrap_servers=['localhost:29092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))



# import sys
#
# from confluent_kafka import *
#
# conf = {
#     "bootstrap.servers": 'kafka1:9092,kafka2:9093,kafka3:9094',
#     "group.id": "test",
#     "auto.offset.reset": "smallest"
# }
#
# consumer = Consumer(conf)
# running = True
# MIN_COMMIT_COUNT = 1
# TOPIC = ["test"]
#
#
# def consume_loop(_consumer, topics):
#     try:
#         _consumer.subscribe(topics)
#         msg_count = 0
#
#         while running:
#             msg = _consumer.poll(timeout=1.0)
#             if msg is None: continue
#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     sys.stderr.write('%% %s [%d] reached end at offset %d\n' %(msg.topic(), msg.partition(), msg.offset()))
#                 elif msg.error():
#                     raise KafkaException(msg.error())
#             else:
#                 # msg_process(msg)
#                 print("\nMsg: ", msg)
#                 msg_count += 1
#                 if msg_count % MIN_COMMIT_COUNT == 0:
#                     consumer.commit(asynchronous=True)
#     finally:
#         consumer.close()
#
#
# consume_loop(consumer, TOPIC)
