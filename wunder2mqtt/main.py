# Copyright (c) 2016 Jasper Spaans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import time

import paho.mqtt.client as mqtt
import requests
import yaml


log = logging.getLogger(__name__)


def get_temp_from_wunderground(config):
    now = time.time()
    max_age = config['max_age']

    for station in config['stations']:
        url = 'http://api.wunderground.com/api/%s/conditions/q/%s.json' % (config['wunderground_api_key'], station)
        try:
            conditions = requests.get(url).json()
            observation = conditions['current_observation']
            timestamp = int(observation['observation_epoch'])
            age = now - timestamp
            if age <= max_age:
                temp_c = float(observation['temp_c'])
                log.info("Current observation: %.1f (station: %s, age: %d)",
                         temp_c, station, age)
                return temp_c
        except:
            log.exception("Error while fetching weather data")
    log.warning("No valid observation found!")


def send_temp_to_mqtt(config, temp):
    mqttc = mqtt.Client()
    mqttc.connect(config['mqtt']['host'], config['mqtt']['port'])
    mqttc.loop_start()
    mqttc.publish(config['mqtt']['target'], temp)
    mqttc.loop_stop()


def main():
    logging.basicConfig(level=logging.WARNING)

    with file("wunder2mqtt.yaml") as f:
        config = yaml.load(f.read())

    temp = get_temp_from_wunderground(config)
    if temp is not None:
        send_temp_to_mqtt(config, temp)


if __name__ == '__main__':
    main()
