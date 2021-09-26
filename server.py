from flask import Flask,request,send_from_directory
import pymysql.cursors

db = pymysql.connect(host='sql5.freemysqlhosting.net',
                     user='sql5436558',
                     password='4wlHZNFSWd',
                     db='sql5436558',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
baglanti = db.cursor()

app = Flask(__name__, static_url_path='')

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('web/images', path)

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
    brand = request.args.get('brand')
    baglanti.execute('SELECT id, name,start_year,end_year FROM vehicles WHERE brand=%s',[brand])
    modeller = baglanti.fetchall()
    list = []
    for k in modeller:

        list.append({
            "id": k.get('id'),
            "model": k.get('name'),
            "model_start": k.get('start_year'),
            "model_end": k.get('end_year'),
        })

    return {
        "data": list
    }




@app.route('/get-products')
def products():
    vehicle = request.args.get('vehicle')
    baglanti.execute('SELECT p.id, p.bracket_group, p.product_name, p.image FROM products as p LEFT JOIN vehicle_product as vp ON vp.bracket_group = p.bracket_group WHERE vp.vehicle_id=%s', [vehicle])
    productsAll = baglanti.fetchall()
    list = []
    for k in productsAll:

        list.append({
            "id": k.get('id'),
            "bracket_group": k.get('bracket_group'),
            "product_name": k.get('product_name'),
            "image": k.get('image')
        })

    return {
        "data": list
    }


if __name__ == '__main__':  # pragma: no cover
    app.run(port=8080)