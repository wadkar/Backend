# Create your views here.
from corona_app.models import CoronaApp, MedicalMap
from corona_app.serializers import CoronaAppSerializer, MedicalMapSerializer
from corona_app.forms import MedicalMapForm
from corona_app.calculations import intersection_calculator, MedicalScoreCalculator

from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django_pandas.io import read_frame
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import geopandas as gpd
from geopandas import GeoDataFrame, GeoSeries, overlay
from shapely.geometry import Point, Polygon
from datetime import datetime
# from pstats import SortKey


# import cProfile, pstats, io
import numpy as np
import pandas as pd
import glob, os
import csv, json



class CoronaAppResult(APIView):
	
	def get(self, request, format=None):
		time_value_list = CoronaApp.objects.values_list('timeslot', flat=True).distinct()
		# data = CoronaApp.objects.get(timeslot = time_value_list[int(timeno)])
		# data = CoronaApp.objects.filter(timeslot = time_value_list[int(timeno)])

		for value in time_value_list:
			data = CoronaApp.objects.filter(timeslot = value)
			data_frame = read_frame(data)            # Transform queryset into pandas dataframe 
			data_frame.rename(columns={'uuid': 'UUID', 'degree': 'Status', 'latitude': 'Lat', 'longitude': 'Lng'}, inplace=True)
			exposed = intersection_calculator(data_frame)
			

			for person in exposed['UUID']:
				exposed_person = CoronaApp.objects.filter(uuid = person)
				exposed_t = datetime.strptime(value, '%H.%M.%m.%d.%Y')
				for times in exposed_person:
					t = datetime.strptime(times.timeslot, '%H.%M.%m.%d.%Y')
					if (t >= exposed_t):
						times.degree = 1
						times.save()

		return Response("Intersection Calculations Done")
		# return Response(exposed)              # Return the result in JSON via Django REST Framework

	def post(self, request, format=None):
		data = request.data
		status_dict = {'unknown': -1, 'positive': 0}

		for times in data["location_history"]:
			app_data = {'uuid': data['id'], 'timeslot': times['timeslot'], 'degree': status_dict[times['status']], 'latitude': times['lat'], 'longitude': times['long']}
			print(app_data)
			serializer = CoronaAppSerializer(data = app_data)
			if serializer.is_valid():
				serializer.save()
				print("saved")

		return Response(data['id'], status=status.HTTP_201_CREATED)


class IntersectMapResult(APIView):
	
	def get(self, request, status, format=None):

		status_dict = {'exposed': 1, 'positive': 0}

		status_objects = CoronaApp.objects.filter(degree = status_dict[status])
		status_uuids = status_objects.values_list('uuid', flat=True).distinct()
		status_df = pd.DataFrame()
		

		for person in status_uuids:
			person_objects = status_objects.filter(uuid = person)
			all_times = list(person_objects.values_list('timeslot', flat=True).distinct())
			res_times = [datetime.strptime(i, '%H.%M.%m.%d.%Y') for i in all_times] 
			max_time = all_times[res_times.index(max(res_times))]
			obj_df = read_frame(person_objects.filter(timeslot = max_time))
			obj_df = obj_df.drop(['id', 'degree'], axis=1)
			status_df = status_df.append(obj_df, ignore_index=True)
			
		status_json = status_df.to_json(orient='records')
		# status_json = status_json.replace('\\"', '\"')
		status_json = json.loads(status_json)
		return JsonResponse(status_json, safe=False) 

class UserExposure(APIView):
	def get(self, request, uuid, format=None):

		status_dict = {1: 'exposed', 0: 'positive', -1: 'unknown'}

		status_objects = CoronaApp.objects.filter(uuid = uuid)
		status_degrees = status_objects.values_list('degree', flat=True).distinct()
		# return Response(status_degrees)
		if (1 in status_degrees):
			return Response({"Exposure": status_dict[1]})

		elif (0 in status_degrees):
			return Response({"Exposure": status_dict[0]})

		else:
			return Response({"Exposure": status_dict[-1]})


# class CoronaAppTimeslots(APIView):
	
# 	def get(self, request, format=None):
# 		time_value_list = CoronaApp.objects.values_list('timeslot', flat=True).distinct()
# 		print(time_value_list)
# 		print(type(time_value_list))
# 		return Response(time_value_list)


class MedicalList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # snippets = MedicalMap.objects.all()
        # serializer = MedicalMapSerializer(snippets, many=True)
        # return Response(serializer.data)
        return Response("Post Medical Data here")

    def post(self, request, format=None):
    	### Removal of this line maybe necessary
    	MedicalMap.objects.all().delete()
        
        serializer = MedicalMapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get(self, request, med_uuid, format=None):
        snippet = MedicalMap.objects.get(med_uuid = med_uuid)
        serializer = MedicalMapSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, med_uuid, format=None):
        snippet = MedicalMap.objects.get(med_uuid = med_uuid)
        serializer = MedicalMapSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, med_uuid, format=None):
        snippet = MedicalMap.objects.get(med_uuid = med_uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MedicalResult(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get(self, request, med_uuid, format=None):
        snippet = MedicalMap.objects.get(med_uuid = med_uuid)
        # serializer = MedicalMapSerializer(snippet)
        F, Shades = MedicalScoreCalculator(snippet)
        score_json = {"score": str(F), "score_color": Shades}
        return JsonResponse(score_json, safe=False)



# def MedicalMapFormView(request):
# 	form = MedicalMapForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()

# 	context = {'form' : form}
# 	return render(request, 'corona_app/medical_data.html', context)


# def MedicalMapFormDetail(request, id):
# 	map = MedicalMap.objects.get(id = id)

# 	F, Shades = MedicalScoreCalculator(map)
	
# 	context = {'medmap': map, 'score': F, 'score_color': Shades}

# 	return render(request, 'corona_app/medical_result.html', context)



# class CoronaAppList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):

    
#     queryset = CoronaApp.objects.all()
#     serializer_class = CoronaAppSerializer

#     def get(self, request, *args, **kwargs):
#     	return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



# class CoronaAppDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = CoronaApp.objects.all()
#     serializer_class = CoronaAppSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)