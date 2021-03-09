import os
import requests


class Mapper:

    def __init__(self):
        self.mapper_url = os.getenv('MAPPER_URL')

    def sendInferenceResultToMapper(self, tags: dict) -> dict:
        response = requests.post(url=self.mapper_url, json=tags)
        return response.json()
