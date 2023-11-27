#!/usr/bin/env python3
import os, socket
import json, msgpack, yaml

import paho.mqtt.client as mqtt

import rclpy
from rclpy.node import Node

from limo_msgs.msg import LimoStatus

MOTION = {0: 'skid_steer', 1: 'ackerman'}
VEHICLE = {0: 'active', 1: 'estop'}
CONTROL = {0: 'ROS', 1: 'Application'}

class MqttPsuedoBridge(Node):

    def __init__(self):
        super().__init__('mqtt_psuedo_bridge')

        # Define all the details for the MQTT broker
        self.mqtt_ip = os.getenv('MQTT_BROKER_IP', 'mqtt.lcas.group')
        self.mqtt_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
        self.mqtt_encoding = os.getenv('MQTT_ENCODING', 'json')
        self.mqtt_client = None

        # Specify the loading and dumping functions
        self.dumps = msgpack.dumps if self.mqtt_encoding == 'msgpack' else json.dumps
        self.loads = msgpack.loads if self.mqtt_encoding == 'msgpack' else json.loads

        # Define source information

        self.limo_name = os.getenv('ROBOT_NAME', socket.gethostname())

        # Initiate connections to ROS and MQTT
        self.connect_to_mqtt()
        self.connect_to_ros()

    def connect_to_mqtt(self):
        # MQTT management functions
        self.mqtt_client = mqtt.Client(self.limo_name+'_status_logger')
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(self.mqtt_ip, self.mqtt_port)
        self.mqtt_client.loop_start()


    def on_connect(self, client, userdata, flags, rc):
        print(" MQTT ->     | Connected")

    def on_message(self, client, userdata, msg):
        print(" MQTT        | Message received ["+msg.topic+"]")

    def connect_to_ros(self):
        self.sub = self.create_subscription(LimoStatus, '/limo_status', self.limo_status_cb, 10)

    def limo_status_cb(self, msg):
        ns = 'agilex/%s/status/'%self.limo_name
        self.mqtt_client.publish(ns+'battery_voltage', msg.battery_voltage, latch=True)
        self.mqtt_client.publish(ns+'motion_mode', MOTION[msg.motion_mode])
        self.mqtt_client.publish(ns+'vehicle_state', VEHICLE[msg.vehicle_state])
        self.mqtt_client.publish(ns+'control_mode', CONTROL[msg.control_mode])
        self.mqtt_client.publish(ns+'error_code', msg.error_code)

"""
battery voltage  9.9: 1f
battery voltage 10.1: 2f
battery voltage 10.2: 2f
battery voltage 10.3: 2f
battery voltage 11.9: charging
"""

def main(args=None):
    rclpy.init(args=args)

    MPB = MqttPsuedoBridge()
    rclpy.spin(MPB)

    MPB.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
