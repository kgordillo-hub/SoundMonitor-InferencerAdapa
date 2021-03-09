import os
import requests


class Mapper:

    def __init__(self):
        self.mapper_url = os.getenv('MAPPER_URL')

    def sendInferenceResultToMapper(self, data: dict) -> dict:
        response = requests.post(url=self.mapper_url, json=data)
        return response.json()
