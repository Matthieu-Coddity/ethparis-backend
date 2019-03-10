from flask_cors import CORS
from flask import Flask, request, g, make_response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask import request, jsonify
import hashlib
import base64
import os

BUFF_SIZE = 65536
num_file = 0

app = Flask(__name__)
app.config["DEBUG"] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://gijwlrdzcoofaf:759576add0f9d2b3b286e9c3d8ded25342696d99ff1887c4fe270d4315408df6@ec2-54-247-70-127.eu-west-1.compute.amazonaws.com:5432/dborcnojaqsrak'
CORS(app)

db = SQLAlchemy(app)

from models import Item

@app.route('/add/')
def webhook():
    hash_item = "ram"
    file_name = "ram@ram.com"
    i = Item(hash_item = hash_item, file_name = file_name)
    print("item created", i)
    db.session.add(i)
    db.session.commit()
    return "user created"

@app.route('/new_product', methods=['POST'])
def add_product():
    #global num_file
    #global bdd
    #num_file +=1
    my_json = request.get_json()
    product = my_json['file']
    my_b = bytes(product,'utf-8')
    my_str =  base64.b64decode(my_b).decode('utf-8')
    my_final_b =  bytes(my_str,'utf-8')    
    #licence = my_json['number']
    price = my_json['price']
    file_name = "temp"
    new_file = open(file_name,"wb")
    new_file.write(my_final_b)
    new_file.close()

    #calcul du hash du produit
    m = hashlib.sha256()
    file_r = open(file_name,"rb")
    while True:
        data = file_r.read(BUFF_SIZE)
        if not data:
            break
        m.update(data)
    file_r.close()

    my_hash = m.hexdigest()
    #ajout du produit à la bdd
    i = Item(hash_item = my_hash, file_name = file_name, price_item=price)
    print("item created", i)
    try:
        db.session.add(i)
        db.session.commit()
        return jsonify(my_hash)
    except:
        db.session.rollback()
        return make_response(jsonify(message=u'hash deja cree'), 500)

#retourne une pièce à partir d'un hash 
@app.route('/piece_from_hash', methods=['POST'])
def get_piece_from_hash():
    my_json = request.get_json()
    #result=db.session.query.filter_by(hash_item=my_json('hash')).first()
    result = Item.query.filter_by(hash_item=my_json.get('hash')).first()
    result_dict=result.__dict__
    del result_dict['_sa_instance_state']
    return jsonify(result_dict)


@app.route('/all_piece', methods=['GET'])
def get_all_piece():
    l=[]
    for u in db.session.query(Item).all():
         di=(u.__dict__)
         del di['_sa_instance_state']
         l.append(di)
    #jsonify([Users.serialize(user) for user in users]
    return jsonify(l)

#erase de la base
@app.route('/erase', methods=['POST'])
def erase():
    my_json = request.get_json()
    if my_json.get('erase') :
        try:
            num_rows_deleted = db.session.query(Item).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(True)
    else:
        return jsonify(False)

@app.route('/price_from_hash', methods=['POST'])
def price():
    hash_voulu = request.get_json().get('hash')
    try: 
        result = Item.query.filter_by(hash_item=hash_voulu).first()
        dictio = result.__dict__
        price = dictio['price_item']
        return jsonify({'price':price})
    except:
        return make_response(jsonify(message=u'probleme'), 500)


if __name__ == '__main__':
    app.run()


'''
csv_file = "file.csv"
bdd = pd.DataFrame()

def sqlite3_loading():
    db_connection = sqlite3.connect('database.db')
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute('CREATE TABLE TEST (a INTEGER);')
    except sqlite3.OperationalError:
        print("we have a problem")
    #conn = sqlite3.connect('database.db')
    #conn.execute('CREATE TABLE objets (file TEXT, licence TEXT, price TEXT, hash TEXT)')
    #conn.close()
    return

#load the BDD  
def load_bdd():
    global bdd
    bdd = pd.read_csv(csv_file)
     
def save_bdd():
    global bdd
    bdd.to_csv(csv_file)
    

#fonction d'initialisation de la bdd pour les test
def init_bdd():
    global bdd 
    bdd = pd.DataFrame({"file":[],"licence":[],"price":[]})
    bdd['hash'] = bdd.apply(calcul_hash,axis=1)

#calcul le hash d'un item
def calcul_hash(item):
    global num_file
    num_file+=1
    return str(num_file)


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
 

#retourne une pièce à partir d'un hash 
@app.route('/piece_from_hash', methods=['POST'])
def get_piece_from_hash():
    my_json = request.get_json()
    item = bdd[bdd["hash"]==my_json['hash']]
    if len(item)>0:
        file_name = item["file"].iloc[0]
        my_file = open(file_name)
        data = my_file.read()
        return flask.jsonify(data)
    else:
        return flask.jsonify(False)

#retourne une pièce à partir d'un hash 
@app.route('/price_from_hash', methods=['POST'])
def get_price_from_hash():
    my_json = request.get_json()
    item = bdd[bdd["hash"]==my_json['hash']]
    if len(item)>0:
        return flask.jsonify(item[["licence","price"]].to_dict("records"))
    else:
        return flask.jsonify(False)

#erase de la base
@app.route('/erase', methods=['POST'])
def erase():
    my_json = request.get_json()
    if my_json.get('erase') :
        init_bdd()
        save_bdd()
        for element in os.listdir('.'):
            if (not os.path.isdir(element)) & (element[0:4] == "new_"):
                os.remove(element)
        return flask.jsonify(True)
    else:
        return flask.jsonify(False)


#retourne l'ensemble des pièces et leurs prix (front pour afficher)
@app.route('/all_piece', methods=['GET'])
def get_all_piece():
    return flask.jsonify(bdd.to_dict("records"))

#retourne l'ensemble des pièces et leurs prix (front pour afficher)
@app.route('/all_piece', methods=['GET'])
def get_all_piece():

    for u in db.session.query(Item).all():
        return jsonify (u.__dict__)
   jsonify([Users.serialize(user) for user in users]
    #return "hello"




if __name__ == "__main__":

    app.run()

'''