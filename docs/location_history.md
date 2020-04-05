### Location history reporting 

**1) Data Export**

**1.1  Request takeout**

1. Open google login in webview and let the user sign-in into their account
    1. Login Url => [https://accounts.google.com/ServiceLogin/signinchooser?continue=https%3A%2F%2Ftakeout.google.com](https://accounts.google.com/ServiceLogin/signinchooser?continue=https%3A%2F%2Ftakeout.google.com)
2. After successful sign-in use automation to request user’s **location history** on email
    2. URL after successful sign-in => [https://takeout.google.com/](https://takeout.google.com/)
3. Register a notification listener to intercept gmail notification of takeout archive. 

**1.2  Download takeout**
/
1. Show the user a notification to complete part 2 of the process.
2. Go gmail.com using the cookies from the previous session and automation download the takeout archive.
3. Save the json file downloaded into the user's smartphone 
4. The file will be then parsed by the goCorona App.

**2) Data Process and transmission** 

**2.1**


To parse json effectively without using the full memory of the phone, use Jackson streaming api as follows :
    [https://cassiomolin.com/2019/08/19/combining-jackson-streaming-api-with-objectmapper-for-parsing-json/](https://cassiomolin.com/2019/08/19/combining-jackson-streaming-api-with-objectmapper-for-parsing-json/)

Using this the location history can be read record by record.  

 	Use the Location History.json file in the root folder not the semantic location files 


**2.2 Data reporting**

 \
The app will round each record into the appropriate timeslots. It will Create entries for each timeslot ( 10 min window ) since starting time ( 00:00 on Jan 15, 2020 ( first case reported in india - Jan 30 ), and add user's times to the appropriate timestamp , ie anything from 00:00 - 00:10 on Jan 15 goes to the first table, next 00:11 to 00:20 to next table and so on.

We can expect the android application to push data from individual users in the format : 

POST api.gocorona.org/report - 

```
{  id : "p1",

   location_history : [ 

       { timeslot: "00.00.01.15.2020", lat : "123456",long : "123456", status : "unknown"},

       { timeslot: "00.10.01.15.2020", lat : "123456",long : "123456", status : "unknown"},

       ...

       ]

}
```

This is what we are expecting as a post request from the application. It is OK to send the data in chunks so that the request size doesn't get too large. Also it is okay to push multiple lat, longs in the same timeslot. **The fixed property is that the timeslots are standardized between the backend and android application to be 10 min intervals**, and this binning process is done on the client side in order to reduce workload on the server side which otherwise has to process multiple rounding operations from multiple patients.

The schema for the cumulative data would look like this on the backend side. 

```
{

all users : [ { timeslot : "00.00.01.15.2020",

	         records : [ {  id  : "p1", lat : "123456", long : "123456", status : "unknown" },

	                 {  id  : "p2", lat : "123456", long : "123456", status : "positive" },

	                 {  id  : "p1", lat : "123456", long : "123456", status : "unknown" }, ] 

 	        },

                    { timeslot : "00.00.01.15.2020",

	          records : [ {  id  : "p1", lat : "123456", long : "123456", status : "unknown" },

	                 {  id  : "p2", lat : "123456", long : "123456", status : "positive" },

	                 {  id  : "p1", lat : "123456", long : "123456", status : "unknown" }, ] 

 	        },

	        ....

                   ]

list_infected_users : [ p1,p2,p3....]

}
```

**3) MVP of functionality from intersection calculator  backend**               

The android application will query the backend endpoint with it's own patient id in order to check if it falls in the list of infected users, and use this in order to determine if the user is infected or not.

eg: 

`GET   api.gocorona.org/AmIExposed/<patient_id>`

returns ` { exposed: True  }` or `{ exposed: False }` from the server

**Enhancement (Step 2) in backend**

Later we will support degrees of transmission : 

`GET   api.gocorona.org/AmIExposed/<patient_id>`

returns `{ exposed: True, degree: 1 }` or `{ exposed: False , degree : 0 } ` from the server 

where
 degree = 0 : Means no exposure 
degree = 1 : Direct contact with infected person ( 1st level transmission )	
degree = 2 : Contact with a degree 1 person (ie contact with a person who was exposed an infected person)
degree = 3 : Contact with a degree 2 person, and so on....

**4. Data Annonymizer considerations/suggestions on App side.**

1. The patient id is a randomly generated UUID that is generated and saved on each user's phone.
2. In case the same location repeats over and over in multiple continuous timestamps and matches the home address of the user ( some tags are saved as such on google location history as "Home", or if marked by user as home ), then the app can choose to not send those coordinates over to the server multiple times , in order to protect user privacy. \

3. Following similar privacy policies as [https://www.apple.com/covid19/](https://www.apple.com/covid19/) we should discuss whether or not we should follow privacy policies described [here](https://www.apple.com/legal/privacy/en-ww/) and legal clauses [here](https://gist.github.com/codeJRV/712e64a0a5b2dbf733d93a0a9cc21ead) . \

    TLDR:
    * we do not store personal identifiable anything on our servers (unless in separate disconnected table)
    * we do not store user responses on our servers (unless in separate disconnected table)
    * we take explicit permission from the user that we are storing annonmyised location history into a database (permission for everything)