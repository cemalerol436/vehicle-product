import pymysql.cursors
from tkinter import *
from tkinter.ttk import Combobox



db = pymysql.connect(host='sql5.freemysqlhosting.net',
                             user='sql5436558',
                             password='4wlHZNFSWd',
                             db='sql5436558',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
baglanti = db.cursor();

window=Tk()


def initWindow():
    getBrands();
    window.title('Select Your Vehicle')
    window.geometry("600x200+30+40")
    window.mainloop()



def getBrands():
    baglanti.execute('SELECT DISTINCT brand FROM vehicles')
    markalar = baglanti.fetchall()
    print(markalar)
    list = []
    for k in markalar:
        list.append(k.get('brand'))

    brand_cb=Combobox(window, values=list)
    brand_cb.place(x=20, y=20)
    def getVehicles(selection):
        brandName = brand_cb.get()
        baglanti.execute('SELECT name, start_year, end_year FROM vehicles WHERE brand = "' + brandName + '"')
        models = baglanti.fetchall()
        print(models)
        for l in markalar:
            list.append(l.get('brand'))






        print(brand_cb.get())
    brand_cb.bind('<<ComboboxSelected>>', getVehicles)





initWindow()

