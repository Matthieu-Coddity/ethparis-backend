import flask
import web3
from flask_cors import CORS
from flask import request
import pandas as pd
from flask import request

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "hello world"

'''
#route pour ajouter un nouveau produit
@app.route('/new_product', methods=['POST'])
def add_product():
    global num_file
    global bdd
    num_file +=1
    my_json = request.get_json()

    product = my_json['file']
    licence = my_json['number']
    price = my_json['price']

    file_name = "new_file_"+str(num_file) 
    new_file = open(file_name,"w")
    new_file.write(product)
    new_file.close()


    #calcul du hash du produit
    my_hash = num_file

    #ajout du produit à la bdd
    bdd = bdd.append({"file":file_name,"licence":licence,"price":price, "hash":my_hash},ignore_index=True)
    save_bdd()

    return flask.jsonify(True)
'''

if __name__ == "__main__":
    app.run()



'''
num_file = 0

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

csv_file = "file.csv"
bdd = pd.DataFrame()

#fonction d'initialisation de la bdd pour les test
def init_bdd():
    global bdd 
    bdd = pd.DataFrame({"file":["file1","file2"],"licence":[1,5],"price":[1,1]})
    bdd['hash'] = bdd.apply(calcul_hash,axis=1)

#calcul le hash d'un item
def calcul_hash(item):
    global num_file
    num_file+=1
    return str(num_file)


#route pour ajouter un nouveau produit
@app.route('/new_product', methods=['POST'])
def add_product():
    global num_file
    global bdd
    num_file +=1
    my_json = request.get_json()

    product = my_json['file']
    licence = my_json['number']
    price = my_json['price']

    file_name = "new_file_"+str(num_file) 
    new_file = open(file_name,"w")
    new_file.write(product)
    new_file.close()


    #calcul du hash du produit
    my_hash = num_file

    #ajout du produit à la bdd
    bdd = bdd.append({"file":file_name,"licence":licence,"price":price, "hash":my_hash},ignore_index=True)
    save_bdd()

    return flask.jsonify(True)

#route pour ajouter une nouvelle licence à un produit
@app.route('/new_licence', methods=['POST'])
def add_licence():
    global bdd
    my_json = request.get_json()
    
    license = my_json["number"]
    price = my_json["price"]
    hash = my_json["hash"]
    file = bdd[bdd["hash"]==hash]["hash"].iloc[0]
    #get id du produit, le nombre d'unité et le prix associé à ce nombre 
    bdd = bdd.append({"file":file,"licence":license,"price":price, "hash":hash},ignore_index=True)
    save_bdd()
    return flask.jsonify(True)

#route pour acheter un produit
@app.route('/buy', methods=['POST'])
def buy():
    #récupère la clé publique de l'utilisateur et celle de l'ensemble produit-"licence"
    #récupère la valeur en eth de l'ensemble produit licence

    pass
 
#envois les information au contrat 
def execute_contract(prix,user_key):
    #execute le contrat 

    #retourne si échec ou réussite 
    pass

#retourne une pièce à partir d'un hash 
@app.route('/piece_from_hash', methods=['POST'])
def get_piece_from_hash():
    my_json = request.get_json()
    item = bdd[bdd["hash"]==my_json['hash']]
    if len(item)>0:
        return flask.jsonify(item.to_dict("records")[0])
    else:
        return flask.jsonify(False)
    


#rertourne l'ensemble des pièces et leurs prix (front pour afficher)
@app.route('/all_piece', methods=['GET'])
def get_all_piece():
    return flask.jsonify(bdd.to_dict("records"))

#load the BDD  
def load_bdd():
    global bdd
    bdd = pd.read_csv(csv_file)
     
def save_bdd():
    global bdd
    bdd.to_csv(csv_file)
    

if __name__ == "__main__":
    init_bdd()
    app.run()
'''
