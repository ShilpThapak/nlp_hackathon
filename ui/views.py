from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io
import os
from expertai.nlapi.cloud.client import ExpertAiClient


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
    if len(df.columns) != 1:
        message = "Please upload a file with one column only!"
        return render(request,'ui/index.html', {"message": message})
    df.columns = ["text"]
    df = sentiment(df)
    data = df.to_dict('split')
    return render(request,'ui/dashboard.html', {"data": data})

def sentiment(df):
    os.environ["EAI_USERNAME"] = 'sudurima.banerjee@rakuten.com'
    os.environ["EAI_PASSWORD"] = 'Rima@280'
    client = ExpertAiClient()

    list = []
    for i in range(0,len(df)):
        text=df['text'].iloc[i]
        language= 'en'
        document = client.specific_resource_analysis(
        body={"document": {"text": text}}, 
        params={'language': language, 'resource': 'sentiment'})
        list.append(document.sentiment.overall)

    df['Sentiment score'] = list
    return df