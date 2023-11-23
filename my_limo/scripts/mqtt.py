#!/usr/bin/env python3

import os
import json, msgpack, yaml

import paho.mqtt.client as mqtt

import rclpy
from rclpy.node import Node

from rospy_message_converter import message_converter

from limo_msgs.msg import LimoStatus

class MqttPsuedoBridge(Node):

    def __init__(self):
        # Define all the details for the MQTT broker
        self.mqtt_ip = os.getenv('MQTT_BROKER_IP', 'mqtt.lcas.group')
        self.mqtt_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
        self.mqtt_encoding = os.getenv('MQTT_ENCODING', 'json')
        mqtt_client = None

        # Specify the loading and dumping functions
        self.dumps = msgpack.dumps if self.mqtt_encoding == 'msgpack' else json.dumps
        self.loads = msgpack.loads if self.mqtt_encoding == 'msgpack' else json.loads

        # Define source information
        self.limo_name = os.getenv('ROBOT_NAME', '')

        # Initiate connections to ROS and MQTT
        self.connect_to_mqtt()
        self.connect_to_ros()

    def connect_to_mqtt(self):
        # MQTT management functions
        self.mqtt_client = mqtt.Client(self.source + "_" + self.robot_name)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.mqtt_ip, self.mqtt_port)
        self.mqtt_client.loop_start()


    def on_connect(self, client, userdata, flags, rc):
        print(" MQTT ->     | Connected")

    def on_message(self, client, userdata, msg):
        print(" MQTT        | Message received ["+msg.topic+"]")

    def connect_to_ros(self):
        self.sub = rclpy.create_subscription('/limo_status', LimoStatus, self.limo_status_cb)

    def limo_status_cb(self, msg):
        self.mqtt_client.publish('agilex/limo/status/battery_voltage', msg.battery_voltage)
        





if __name__ == '__main__':
    super('limo_status_logger')
    mpb = MqttPsuedoBridge()
    rospy.spin()