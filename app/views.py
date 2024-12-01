from dotenv import load_dotenv
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import os
import time
import json
from utils.llm import translate_util

def index(request):
    return render(request, 'app/index.htm')

def translate(request):
    sentence = request.GET.get("sentence")
    source = request.GET.get("source")
    destination = request.GET.get("destination")
    llm = request.GET.get("llm")
    
    return HttpResponse(json.dumps(translate_util(sentence, source, destination, llm)))