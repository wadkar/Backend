from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
import pandas as pd
import numpy as np

class CoronaAppTestCase(APITestCase):
    def testList(self):
    	#Using the standard RequestFactory API to create a form POST request
    	factory = APIRequestFactory()
    	df = pd.read_csv('bengaluru_latlng_test.csv')
    	data_len = df.shape[0]
    	d = df.values

    	for i in range(0, 2):
    		name_bar = d[0][i]
    		status_bar = d[1][i]
    		latitude_bar = d[2][i]
    		longitude_bar = d[3][i]

    		request = factory.post('/corona_app/', {'name': name_bar, 'status': status_bar, 'latitude': latitude_bar, 'longitude': longitude_bar})
