#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/15 上午9:57
# @Author  : vyouzhi
# @File    : kafka_log.py.py
# @Software: PyCharm
import json


from kafka import KafkaConsumer
from kafka import KafkaProducer
import sys
from websocket_server import WebsocketServer
from threading import Thread
from log_proto import *

_servers = {}



# Called for every client connecting (after handshake)


def new_client(client, server):
    # print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")
    _servers[server] = client


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + '..'
    server.send_message(client, message)
    print("Client(%d) said: %s" % (client['id'], message))


class kafka_log(object):
    """
    classdocs
    """

    def __init__(self, topic_name):
        """
        doc
        """
        self._topic = topic_name

    def ws(self):
        PORT = 9001
        server = WebsocketServer(host='0.0.0.0', port=PORT)
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(message_received)
        server.run_forever()

    def sendMsg(self, data):
        # print(data)
        for key in _servers.keys():
            try:
                key.send_message(_servers[key], data)
            except BrokenPipeError:
                print("Oops ..")

    def consumer(self):

        consumer_instance = self.get_kafka_consumer()
        consumer_instance.subscribe([self._topic])
        dictMsg = {}
        # topic, tp.partition, record.offset, record.timestamp,
        # record.timestamp_type, key, value, headers, record.checksum,
        # key_size, value_size, header_size
        color = ["\x1B", "[0m", "[31m", "[32m", "[33m", "[34m",
                 "[35m", "[36m", "[37m", "[93m", "[1m", "[4m"]

        pl = ParserLog()
        for msg in consumer_instance:
            # data = json.dumps(msg).encode('utf-8')
            # print(msg)
            dictMsg["topic"] = msg.topic
            dictMsg["timestamp"] = msg.timestamp
            # dictMsg["value"] = str(msg.value.decode("utf-8"))
            pl.getData(msg.value)
            dictMsg["value"], idx =   pl.toClass()

            if len(msg.headers) > 0:
                dictMsg["thread_id"] = str(msg.headers[0][1].decode("utf-8"))
            else:
                dictMsg["thread_id"] = ""
                # for cor in color:
                #     dictMsg["value"] = dictMsg["value"].replace(cor, "")

                # print(dictMsg["value"])

            dictMsg['offset'] = msg.offset
            # logger.info(dictMsg)
            data = json.dumps(dictMsg)
            self.sendMsg(data)

    def get_kafka_consumer(self, servers=['localhost:9092']):
        _consumer = None
        try:
            _consumer = KafkaConsumer(bootstrap_servers=servers)
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))
        finally:
            return _consumer


def te():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send('e2l-log', key=None, value=b'1234',
                  headers=[('content-encoding', b'base64')])


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:

        topic_name = "e2l-log"
        consumer = kafka_log(topic_name)

        t = Thread(target=consumer.ws)
        t.start()

        consumer.consumer()
    else:
        te()
