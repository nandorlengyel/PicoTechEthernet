import threading
import pytz
import os
import json
import requests

class AggregateThread(threading.Thread):
    def __init__(self, queue, panda_token=None):
        self.queue = queue
        self.panda_url = os.environ.get('PANDA_URL', None)

        self.panda_user = os.environ.get('PANDA_USER', None)
        self.panda_password = os.environ.get('PANDA_PASSWORD', None)

        self.panda_token = panda_token

        self.device_id = os.environ.get('PD_ID', None)
        self.time_stamp = None

        self.device_id_dict = {0:os.environ.get('PD_ID_0', None),1:os.environ.get('PD_ID_1', None),2:os.environ.get('PD_ID_2', None)}
        threading.Thread.__init__(self, target=self.aggregate_results, daemon=True) 

    def aggregate_results(self):
        while True:
            result_dict = self.queue.get()
            measurement_data = dict({self.device_id: {}})    

            for key, value in result_dict.items():           
                agg_value = sum(value)

                consumption_value = agg_value / 1000 * 230 / 1000 / 60
                measurement_data[self.device_id][self.device_id_dict[key]] = [{"time": self.localize_time(self.time_stamp), "value": consumption_value}] 
            print(self.put_to_api(json.dumps(measurement_data)))
    
    def localize_time(self, time):
        localtimezone = pytz.timezone('UTC')
        local_time = localtimezone.localize(time, is_dst=None)
        return local_time.strftime("%Y-%m-%d %H:%M:%S%z")

    def put_to_api(self, data):
        return requests.put(
            self.panda_url + 'api/meter/device_identifier/',
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + self.panda_token
            })
 
    def panda_login(self):
        url = self.panda_url + 'api/auth/'
        body = {
            'username': self.panda_user,
            'password': self.panda_password
        }

        response = requests.post(url, json=body)
        self.panda_token = response.json()['token']