from django.shortcuts import render
import pickle
import json
import pandas as pd

# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))
map_add = json.load(open('map.json', 'r'))


def predict(Address, Size):
    X = pd.DataFrame([[Address, Size]], columns=['Address', 'Size(Acres)'])
    X['Address'] = X['Address'].map(map_add)
    prediction = model.predict(X)
    return int(prediction)


def home(request):
    params = {'add': list(map_add.keys())}
    return render(request, 'index.html', params)


def index(request):
    address = str(request.POST.get('address', 'others'))
    size = int(request.POST.get('size', '500'))
    pred = predict(address, size)
    params = {'add': list(map_add.keys()),
              'pred': f"Monthly Rent for {size} sqft in {address} is Rs {pred}"}
    return render(request, 'index.html', params)
