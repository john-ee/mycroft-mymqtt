from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from urllib2 import urlopen
import paho.mqtt.client as mqtt

__author__ = 'john_ee'

LOGGER = getLogger(__name__)

class mqtt_client(MycroftSkill):

    def __init__(self):
        super(mqtt_client, self).__init__(name="mqtt_client")

        self.protocol = self.config["protocol"]
	self.mqttssl = self.config["mqtt-ssl"]
	self.mqttca = self.config["mqtt-ca-cert"]
	self.mqtthost = self.config["mqtt-host"]
	self.mqttport = self.config["mqtt-port"]
	self.mqttauth = self.config["mqtt-auth"]
	self.mqttuser = self.config["mqtt-user"]
	self.mqttpass = self.config["mqtt-pass"]


    def initialize(self):
        self.load_data_files(dirname(__file__))
        self. __build_single_command()


    def __build_single_command(self):
        intent = IntentBuilder("publishIntent").require("PublishKeyword").require("Request")
        self.register_intent(intent, self.handle_publish_command)
        #intent = IntentBuilder("readIntent").require("ReadKeyword").require("TopicKeyword").require("TopicName")
        #self.register_intent(intent, self.handle_read_command)

    def handle_publish_command(self, message):
        words = message.data['TopicName'].split(' ')
        payload = words[len(words)-1]
        topic_name = ""
        for i in range(len(words)-1):
            topic_name += "/" + words[i]
        if (self.protocol == "mqtt"):
	    mqttc = mqtt.Client("MycroftAI")
	    if (self.mqttauth == "yes"):
	        mqttc.username_pw_set(self.mqttuser,self.mqttpass)
	    if (self.mqttssl == "yes"):
		    mqttc.tls_set(self.mqttca) #/etc/ssl/certs/ca-certificates.crt
        mqttc.connect(self.mqtthost,self.mqttport)
	    mqttc.publish(topic_name, payload)
	    mqttc.disconnect()
	    self.speak_dialog("cmd.sent")
        LOGGER.info("topic : " + topic_name + " payload : " + payload)

    #def handle_write_command(self, message):
        #topic_name = message.data['TopicName'].replace(' ','_')




    def stop(self):
        pass

def create_skill():
    return mqtt_client()
