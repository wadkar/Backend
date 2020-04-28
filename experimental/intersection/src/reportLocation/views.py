from django.http import HttpResponse
from django.utils.text import slugify
# Create your views here.
def main(request):
    if request.method=='POST':
        locationData = request.POST
        locationHistory = locationData['locationHistory']
        for row in locationHistory:
            with open("LocationData/"+slugify(timeslot)+".csv","a+") as timeslot_file:
                timeslot_file.write(locationData['uuid'],locationData['status'],row['lat'],row['lng'])
        return HttpResponse('API Request Received OK',statuscode=200)
    else:
        return HttpResponse('Failed')
