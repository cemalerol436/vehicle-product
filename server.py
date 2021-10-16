from flask import Flask, request
import pymysql.cursors


db = pymysql.connect(host='localhost',
                     user='cemal',
                     password='Q1w2e3r4t5.!',
                     db='vehicles',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
baglanti = db.cursor()

app = Flask(__name__)


@app.route('/get-brands')
def brands():
    baglanti.execute('SELECT DISTINCT brand FROM vehicles')
    markalar = baglanti.fetchall()
    list = []
    for k in markalar:
        list.append(k.get('brand'))

    return {
        "data": list
    }


@app.route('/get-models')
def models():
    brand = request.args.get("brand")
    baglanti.execute('SELECT id, name, start_year, end_year FROM vehicles WHERE brand=%s', [brand])
    modeller = baglanti.fetchall()
    list = []
    for k in modeller:
        list.append({"id": k.get("id"),
                     "model":k.get("name"),
                     "modelstart":k.get("start_year"),
                     "modelend":k.get("end_year")
                     })

    return {
        "data": list
    }
@app.route('/get-products')
def products():
    vehicle = request.args.get("vehicle")
    baglanti.execute('SELECT id, name, start_year, end_year FROM vehicles WHERE brand=%s', [vehicle])
    products = baglanti.fetchall()
    list = []
    for k in products:
        list.append({"id": k.get("id"),
                     "bracket_group":k.get("bracket_group"),
                     "product_name":k.get("product_name"),
                     "image":k.get("image")
                     })

    return {
        "data": list
    }
