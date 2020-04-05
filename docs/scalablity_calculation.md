## Scalablity considerations: 

**1. Location data storage optimization**

Input Data format from APIs

```
{  id : "p1",

   location_history : [ 

       { timeslot: "00.00.01.15.2020", lat : "123456",long : "123456", status : "unknown"},

       { timeslot: "00.10.01.15.2020", lat : "123456",long : "123456", status : "unknown"},

       ...

       ]

}
```


1. Store the data in some DB like hadoop or something for processing it later in time 
2. Now convert each history data row from the request as following csv rows

	timeslot(in unix timestamp), lat, long, status, patient_id(or id) \
	1585692128, 123456, 123456, unknown, p1

	1585692128, 123456, 123456, unknown, p1

 3.	Now divide the timestamp of each row with 600 (60*10 = 10 mins) and find the remainder, and subtract that remainder from the timestamp

	1585692128 % 600 = 128

	1585692128 - 128 = **1585692000**

 4. Now in storage directory find/create the directory with name **1585692000**(timestamp) and create three files with names

	All_patient.csv, infected_patient.csv, level1_patient.csv

 5. In All_patient.csv append a row with all the incoming location history rows, if after performing the calc from step 3 in their timestamps yields **1585692000** and so on. And insert only infected patient location history in infected_patient.csv file and only level1 patients location history in level1_patient.csv

 6. Now for processing any time slot, just program your code to open all the points from all patient_history.csv of any timeslot, use the geopandas library to perform range search in this tree using the points from infected_patient.csv to find out level1 patients easily and populate our db accordingly and do a nearest neighbour search using points from level1_patient.csv to find out level2 patient list and so on.

**Note 1:** With this approach we can easily process the old location history as well by populating the appropriate files in appropriate directories (using timestamps) and running the nearest neighbour search in latest updated directories (can be fetched from OS)

**Note 2:** With this approach and 10 mins timeslot, we’ll be creating 576 files (innodes) daily so we should be fine with using a 20GB ext4 drive (about 1.2M innodes)

And we can actually process parallel workers to find out intersections in different directories and maintain a single db containing only patient_id and their infection level (infected, lvl1, lvl2, unknown etc) and this should work best on a ssd drive.
