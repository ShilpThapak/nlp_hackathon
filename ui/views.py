from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io
import os
from expertai.nlapi.cloud.client import ExpertAiClient
import ast
from .helpers import *


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

        # print(request.FILES, request.FILES.get('document'))
        filename = str(request.FILES.get('document'))
        print(filename)
        if filename[-4:] != '.csv':
            message = "Only .csv files allowed !!"
            return render(request,'ui/index.html', {"message": message})
        
    uploaded_file = request.FILES['document']
    df = pd.read_csv(io.BytesIO(uploaded_file.read()))
    if len(df.columns) != 1:
        message = "Please upload a file with one column only!"
        return render(request,'ui/index.html', {"message": message})
    df.columns = ["Text"]
    # df = sentiment(df)
    data = df.to_dict('split')
    return render(request,'ui/dashboard.html', {"data": data})


def sentiment_analysis(request):
    data = request.POST.get('data')
    data = ast.literal_eval(data)
    df = pd.DataFrame(data["data"])
    df.columns = ['Text']
    os.environ["EAI_USERNAME"] = 'sudurima.banerjee@rakuten.com'
    os.environ["EAI_PASSWORD"] = 'Rima@280'
    client = ExpertAiClient()

    list = []
    for i in range(0,len(df)):
        text = df['Text'].iloc[i]
        language= 'en'
        document = client.specific_resource_analysis(
        body={"document": {"text": text}}, 
        params={'language': language, 'resource': 'sentiment'})
        list.append(document.sentiment.overall)

    df['Sentiment score'] = list
    data = df.to_dict('split')
    context = senti_helper(df)
    return render(request,'ui/sentiment_analysis.html', {"data": data, "context": context})


def emotional_traits(request):
    data = request.POST.get('data')
    data = ast.literal_eval(data)
    df = pd.DataFrame(data["data"])
    df.columns = ['Text']
    os.environ["EAI_USERNAME"] = 'sudurima.banerjee@rakuten.com'
    os.environ["EAI_PASSWORD"] = 'Rima@280'
    client = ExpertAiClient()

    list2=[]
    for i in range(0,len(df["Text"])):
        text=df["Text"].iloc[i]
        taxonomy='emotional-traits'
        document = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy,'language': 'en'})

        categories = []
        scores = []
        for category in document.categories:
            categories.append(category.label)
            scores.append(category.frequency)
            
        if len(categories) == 0:
            list2.append('NA')
        else:
            list2.append(categories[0])
    df["traits"] = list2
    data = df.to_dict('split')
    return render(request,'ui/emotional_traits.html', {"data": data})
