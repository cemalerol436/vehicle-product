from flask import Flask
import pymysql.cursors

db = pymysql.connect(host='sql5.freemysqlhosting.net',
                             user='sql5436558',
                             password='4wlHZNFSWd',
                             db='sql5436558',
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
    return 'Hello from Server'