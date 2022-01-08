# These are the codes to bring informations from database and push it to the html.

# The modules for flask and connection.

from flask import Flask, request
import pymysql.cursors

# The connection Information;
db = pymysql.connect(host='167.99.211.234',
                     user='cemal',
                     password='Q1w2e3r4t5.!',
                     db='vehicles',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

baglanti = db.cursor()

# To reach to the root directory.
app = Flask(__name__,
            static_url_path='',
            static_folder='Public',
            template_folder='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/get-brands')
def brands():
    baglanti.execute('SELECT min(id) AS id , brand FROM vehicles GROUP BY brand')
    markalar = baglanti.fetchall()
    list = []
    for k in markalar:
        list.append(({"id": k.get("id"),
                     "brand": k.get("brand"),
                     }))
    return {
        "status": "success",
        "result": {
         "brands": list
    }
  }


@app.route('/add-product', methods=['POST'])
def addProduct():
    bracket = request.form['bracket']
    name = request.form['name']
    image = request.form['image']

    baglanti.execute('INSERT INTO `products` (`bracket_group`, `product_name`, `image`) VALUES (%s, %s, %s)',
                     [bracket, name, image])
    db.commit()

    return {
        "success": True
    }


@app.route('/add-vehicle', methods=['POST'])
def addVehicle():
    code = int(request.form['code'])
    model = request.form['model']
    startyear = int(request.form['startyear'])
    endyear = int(request.form['endyear'])
    brand = request.form['brand']

    if code < 1000 or code > 9999:
        return {
            "success": False
        }

    baglanti.execute("INSERT INTO vehicles (code, name, start_year, end_year, brand ) VALUES (%s, %s, %s, %s, %s)",
                     (code, model, startyear, endyear, brand))
    db.commit()

    return {
        "success": True
    }


@app.route('/get-models')
def models():
    brand = request.args.get("brand")
    baglanti.execute('SELECT id, name, start_year, end_year FROM vehicles WHERE brand=%s', [brand])
    modeller = baglanti.fetchall()
    list = []
    for k in modeller:
        list.append({"id": k.get("id"),
                     "model": k.get("name"),
                     "modelstart": k.get("start_year"),
                     "modelend": k.get("end_year")
                     })
    return {
        "data": list
    }

@app.route('/get-products')
def products():
    vehicle_id = request.args.get("vehicle")
    baglanti.execute('SELECT vp.bracket_group, p.product_name, p.image, p.category_id, c.category_name '
                     'FROM vehicle_product vp '
                     'INNER JOIN products p ON p.bracket_group = vp.bracket_group '
                     'INNER JOIN categories c ON p.category_id = c.id '
                     'WHERE vp.vehicle_id=%s '
                     'ORDER BY p.product_name', [vehicle_id])
    products = baglanti.fetchall()
    list = []
    for p in products:
        list.append({
                     "bracket_group": p.get("bracket_group"),
                     "product_name": p.get("product_name"),
                     "image": p.get("image"),
                    "category_id": p.get("category_id"),
                    "category_name": p.get("category_name")
                     })
    return {
        "data": list
    }

