from flask import Flask, render_template, request, redirect, url_for, Response
import mysql.connector
import os

import cv2
from tensorflow import keras
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from PIL import Image
import numpy as np

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="deteksi_katarak"
)
mycursor = mydb.cursor()

#deteksi mata
def deteksi_Mata(path_model,image_path):
    img = cv2.imread(image_path)
    model =cv2.CascadeClassifier(path_model)
    abu = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    prediksi = model.detectMultiScale(abu,1.2,20)
    return prediksi

#lihat hasil deteksi
# def lihat(koordinat, path_image):
#     img = cv2.imread(path_image)
#     for (x,y,w,h) in koordinat:
#         cv2.rectangle(img,(x,y), (x+w, y+h), (255,255,0),2)
#     cv2.imshow('mata',img)
#     cv2.waitKey(0)

#meyimpan crop mata
def simpanMata(koordinat, path_image):
    img = cv2.imread(path_image)
    count=0
    for (x,y,w,h) in koordinat:
        cv2.rectangle(img,(x,y), (x+w, y+h), (255,255,0),2)
        roi = img[y:y+h,x:x+w]
        cv2.imwrite("gambar/mata/mata_%d.jpg" %count, roi)
        count=+1

#extrak mata
def proses_Deteksi_Mata(input,model):
    mataDetec=deteksi_Mata(model,input)
    terdeteksi = len(mataDetec)
    if (terdeteksi==2):
        simpanMata(mataDetec,input)
        # lihat(mataDetec,input)
        return 1
    else:
        return 0
        
#deteksi katarak
def deteksi_Katrak(path_model, path_input):
    model = keras.models.load_model(path_model)
    img = np.array(Image.open(path_input).resize((94, 55)))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    pred = model.predict(img)
    # return pred
    if pred[0] == 1: 
        return 0
    else:
        return 1
    
#simpan hasil deteksi katarak
def simpanHasil(hasil, gambar):
    mycursor.execute("SELECT * FROM datapendertakatarak ORDER BY id DESC limit 1")
    data = mycursor.fetchall()
    for item in data:
        id = item[0]
        # kondisi = item[6]
    img = cv2.imread(gambar)
    if hasil ==1: 
        cv2.imwrite("gambar/hasil/katarak/image_{}.jpg".format(id), img)
    else :
        cv2.imwrite("gambar/hasil/normal/image_{}.jpg".format(id), img)

def deteksi_hasil(hasil):
    katarak = hasil
    mycursor.execute("SELECT * FROM datapendertakatarak ORDER BY id DESC limit 1")
    data = mycursor.fetchall()
    for item in data:
        id = item[0]
    mycursor.execute("""UPDATE `datapendertakatarak` SET `hasil_deteksi` = '{}' WHERE `datapendertakatarak`.`id` = '{}';""".format(katarak,id))
    mydb.commit()
    return katarak

@app.route('/deteksi')
def deteksi():
    mycursor.execute("SELECT * FROM datapendertakatarak ORDER BY id DESC limit 1")
    data = mycursor.fetchall()
    for item in data:
        id = item[0]
        nama = item[1]
        nik = item[2]
        ttl = item[3]
        pekerjaan = item[4]
        kelamin = item[6]
        
    input = "static/{}.jpg" .format(id)
    modelMata = 'model/haarcascade_eye.xml'
    modelKatarak = 'model/deteksiKatarak.h5'
    kanan = 'gambar/mata/mata_0.jpg'
    kiri = 'gambar/mata/mata_1.jpg'
    deteksi=proses_Deteksi_Mata(input,modelMata)
    print(deteksi)
    if deteksi==1: 
        # print ("foto baik")
        mataKanan = deteksi_Katrak(modelKatarak,kanan)
        mataKiri = deteksi_Katrak(modelKatarak,kiri)
        simpanHasil(mataKanan,kanan)
        simpanHasil(mataKiri,kiri)
        hasil_deteksi=""
        if mataKanan ==1 and mataKiri ==1:
            hasil_deteksi= "normal"
            deteksi_hasil(hasil_deteksi)
            return render_template("halaman_hasil.html",id=id,nama=nama,nik=nik,kelamin=kelamin,ttl=ttl,pekerjaan=pekerjaan, hasil=hasil_deteksi)
        else:
            hasil_deteksi= "katarak"
            deteksi_hasil(hasil_deteksi)
            return render_template("halaman_hasil.html",id=id,nama=nama,nik=nik,kelamin=kelamin,ttl=ttl,pekerjaan=pekerjaan, hasil=hasil_deteksi)
    else:
        # print("kualitas gambar kurang bagus")
        hasil_deteksi= "kualitas gambar kurang bagus edit!"
        deteksi_hasil(hasil_deteksi)
        return render_template("halaman_hasil.html",id=id,nama=nama,nik=nik,kelamin=kelamin,ttl=ttl,pekerjaan=pekerjaan, hasil=hasil_deteksi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/HapusHasil/<id>')
def HapusHasil(id):
    mycursor.execute("DELETE FROM datapendertakatarak WHERE `datapendertakatarak`.`id` = {}".format(id))
    mydb.commit()
    return redirect(url_for('home'))

@app.route('/editHasil/<id>')
def editHasil(id):
    mycursor.execute("SELECT * FROM `datapendertakatarak` WHERE id = {}".format(id))
    data = mycursor.fetchone()
    return render_template('edit.html', data=data)

@app.route('/update_submit/<id>', methods=['POST'])
def update_submit(id):
    nama = request.form.get('txtname')
    kelamin = request.form.get('kelamin')
    nik = request.form.get('nik')
    tanggal_lahir = request.form.get('tgl_lahir')
    pekerjaan = request.form.get('Pekerjaan')
    hasil = request.form.get('hasil')
    mycursor.execute("UPDATE datapendertakatarak SET nama ='{}', nik = '{}', tangal_lahir = '{}', pekerjaan = '{}', kelamin = '{}',hasil_deteksi= '{}' WHERE id= {}".format(nama,nik,tanggal_lahir,pekerjaan,kelamin,hasil,id))
    mydb.commit()
    return redirect(url_for('home'))


@app.route('/home')
def home():
    mycursor.execute("SELECT * FROM `datapendertakatarak`")
    data = mycursor.fetchall()
    return render_template('indexmin.html', data=data)

@app.route('/addprsn')
def addprsn():
    mycursor.execute("select ifnull(max(id) + 1, 101) from datapendertakatarak")
    row = mycursor.fetchone()
    nbr = row[0]
    return render_template('addprsn.html', newnbr=int(nbr))


@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    id = request.form.get('txtnbr')
    nama = request.form.get('txtname')
    kelamin = request.form.get('kelamin')
    nik = request.form.get('nik')
    tanggal_lahir = request.form.get('tgl_lahir')
    pekerjaan = request.form.get('Pekerjaan')
    mycursor.execute("""INSERT INTO `datapendertakatarak`(`id`, `nama`, `nik`, `tangal_lahir`, `pekerjaan`, `kelamin`) VALUES 
                     ('{}','{}','{}','{}','{}','{}')""".format(id, nama, nik,tanggal_lahir, pekerjaan, kelamin))
    mydb.commit()
    return redirect(url_for('vfdataset_page'))

@app.route('/vfdataset_page')
def vfdataset_page():
    mycursor.execute("SELECT * FROM datapendertakatarak ORDER BY id DESC limit 1")
    data = mycursor.fetchall()
    for item in data:
        id = item[0]
        nama = item[1]
    return render_template('upload.html',nama= nama, id=id)

@app.route('/upload', methods=['POST'])
def upload_file():
    mycursor.execute("SELECT * FROM datapendertakatarak ORDER BY id DESC limit 1")
    data = mycursor.fetchall()
    file = request.files['image']
    for item in data:
        id = item[0]
    file.save("static/{}.jpg" .format(id))
    # file.save("static/{}.jpg" .format(id))
    return redirect(url_for('deteksi'))

if __name__ == "__main__":

    app.run(host='127.0.0.1', port=5001, debug=True)