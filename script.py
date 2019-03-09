import requests
import base64
url="http://localhost:5000/new_product"
#url="https://ethparis.herokuapp.com/new_product"

with open('CMJN_Logo_Toguna40_1.stl','rb') as f:
    data = f.read()
    encodedZip = base64.b64encode(data)

str_data = encodedZip.decode('utf-8')
print(type(str_data))

data = {
    'file' :str_data,
    'public_key' : '0xfae02c7188cd33b4fed7fecb5b2a442dd2638cf6', 
    'price' : "110"
}

response = requests.post(url, json=data,).text

print(response)