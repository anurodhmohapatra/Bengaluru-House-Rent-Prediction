from django.shortcuts import render
import pickle
import json
import pandas as pd

# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))
map_add = json.load(open('map.json', 'r'))

def predict(Address,Size):
    X = pd.DataFrame([[Address,Size]],columns=['Address','Size(Acres)'])
    X['Address'] = X['Address'].map(map_add)
    prediction = model.predict(X)
    return int(prediction)

def index(request):
    address = request.GET.get('address','others')
    size = request.GET.get('size',500)
    print(address)
    print(size)
    return render(request,'index.html')