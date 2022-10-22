from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io

# Create your views here.
def index(request):
    return render(request, 'ui/index.html')

def dashboard(request):
    if request.method =='GET':
        message = "Please upload a file !!"
        return render(request,'ui/index.html')
    if request.method =='POST':
        if len(request.FILES) == 0:
            message = "No file found!!"
            return render(request,'ui/index.html', {"message": message})
        
    uploaded_file = request.FILES['document']
    df = pd.read_csv(io.BytesIO(uploaded_file.read()))
    data = df.to_dict('split')
    return render(request,'ui/dashboard.html', {"data": data})