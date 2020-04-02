import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame, GeoSeries, overlay
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import glob, os



def get_infected_users_at_timestamp(timestamp_string):
    data_frame = pd.read_csv(timestamp_string,header=None,names=["UUID","Status","Lat","Lng"])

    #print(data_frame)

    allPts = GeoDataFrame(data_frame,crs={"init":"EPSG:4326"},geometry=[Point(xy) for xy in zip(data_frame["Lat"], data_frame["Lng"])]).to_crs("EPSG:3395")

    positivePoints = allPts[allPts['Status']==1]
    negativePoints = allPts[allPts['Status']==0]

    #print(positivePoints)
    #print(negativePoints)

    positivePointsBuffered = positivePoints.set_geometry(positivePoints.geometry.buffer(20,resolution=16),inplace=False)
    negativePointsBuffered = negativePoints.set_geometry(negativePoints.geometry.buffer(20,resolution=16),inplace=False)
    #print(positivePointsBuffered)

    #ax=positivePointsBuffered.plot(color="red")
    #negativePointsBuffered.plot(ax=ax,color='green', alpha=0.5)


    #intersecting_points = negativePoints.intersection(positivePointsBuffered.unary_union)
    #print(intersecting_points)
    #print(negativePoints)


    #print(negativePoints.loc[negativePoints['geometry'].isin(intersecting_points.to_numpy())])
    #combined_infectious_points = positivePointGeometryBuffered.unary_union

    res_intersect = overlay(positivePointsBuffered,negativePointsBuffered,how='intersection')
    res_intersect=res_intersect.drop(['Status_1','UUID_1','Lat_1','Lng_1','geometry'],axis=1)
    res_intersect.rename(columns={'Status_2':'Status',
                          'UUID_2':'UUID',
                          'Lat_2':'Lat',
                          'Lng_2':'Lng'},inplace=True)
    #res_intersect['UUID_2'],res_intersect['Status_2']
    res_intersect.drop_duplicates(subset ="UUID",keep = "first", inplace = True)
    res_intersect['Timeslot']=timestamp_string
    return res_intersect

with open('InfectedUsers.csv','a+') as infected_file:
    for timestamp_file in glob.glob("LocationData/*.csv"):
        get_infected_users_at_timestamp(timestamp_file).to_csv(infected_file, header=None)
