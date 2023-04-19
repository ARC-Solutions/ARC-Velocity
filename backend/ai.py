import requests
from PIL import Image
from io import BytesIO
import time
import uuid


def save_data(command):
    for _ in range(0, 10):
        response = requests.get('http://192.168.43.112:8080/video')

    Image.open(BytesIO(response.content)).convert('L').save('../data_tmp/{}_{}.jpg'.format(uuid.uuid1(), command))
