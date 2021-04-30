import os
import requests


class Mapper:

    def __init__(self):
        self.mapper_url = os.getenv('MAPPER_URL')

    def send_inference_result_mapper(self, data: dict) -> dict:
        response = requests.post(url=self.mapper_url, json=data)
        return response.json()
