from django.http import HttpResponse
import pandas as pd
# Create your views here.
def main(request):
    if request.method=='POST':
        checkData = request.POST
        UUID = checkData.get('UUID','No UUID Requested')
        if UUID!='No UUID Requested':
            df = pd.read_csv("../InfectedUsers.csv",header=None,memory_map=True,names=['Index','UUID','Status','Lat','Lng'])
            if UUID in df['UUID']:
                return HttpResponse('Potentially Exposed',statuscode=200)
            else:
                return HttpResponse('No Exposure Found',statuscode=200)
        else:
            return HttpResponse('No UUID in Request')
    else:
        return HttpResponse('Failed: Must submit POST')
