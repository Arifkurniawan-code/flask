from flask import Flask,render_template,request,url_for,session,redirect,flash
from Prepocessing_sentence import text_prepocessing
from instagram_scrape.ScrapeInstagram import go_url
from lstm_model import LSTM_model
import sqlite3
import re

def home():
    return render_template('isi.html')

def uji_komentar():
    if request.method == 'POST':
        comment_text = request.form['kalimat']
        comment_text = text_prepocessing(comment_text)
        print(comment_text)
        model = LSTM_model()
        dict = {}
        dict = model.predict_comment(comment_text)
        print(dict['class'])
        print(dict['probabilities'][1])
        if (dict['class'] == [0]):
            Label=0
            image='https://img.icons8.com/doodle/480/000000/topic--v1.png'
            flash('Komentar anda termasuk komentar cyberbullying',category='black')
            alert='Setelah dianalisa, komentar yang anda masukan memiliki kecenderungan menyinggung orang lain karena memiliki makna kurang bagus ataupun ada unsur-unsur negatif lainya, Lebih berhati-hatilah dalam berkomentar'
        elif (dict['class'] == [1]):
            Label = 1
            image = 'https://img.icons8.com/doodle/480/000000/topic--v1.png'
            flash('Komentar anda termasuk komentar Irrelevant', category='gray')
            alert='Setelah dianalisa, komentar yang anda masukan adalah komentar yang tidak berkaitan dengan cyberbullying'
        elif (dict['class'] == [2]):
            Label = 2
            image = 'https://img.icons8.com/doodle/480/000000/topic--v1.png'
            flash('Komentar anda termasuk komentar Netral', category='yellow')
            alert='Setelah dianalisa, komentar anda memiliki makna yang netral, namun lebih baik lebih berhati-hati dalam berkomentar'
        else:
            Label = 3
            image = 'https://img.icons8.com/doodle/480/000000/topic--v1.png'
            flash('Komentar anda termasuk komentar Bukan cyberbullying', category='green')
            alert='Setelah dianalisa, komentar anda tidak memiliki unsur yang merugikan orang lain, teruslah berkomentar positif'
        connection = sqlite3.connect('data/Admin.db')
        conn = connection.cursor()
        conn.execute('INSERT INTO riwayat(kalimat,label) VALUES ((?),(?))', (comment_text, Label))
        connection.commit()
        conn.close()
        connection.close()
        return render_template('hasil.html', image=image,alert=alert)
    else:
        return render_template('uji_komentar.html')

def instagram_post():
    if request.method=='POST':
        url=request.form['kalimat']
        kode=request.form['kode']
        connection=sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        cursor=conn.execute('SELECT * from instagram')
        item=cursor.fetchone()
        connection.commit()
        conn.close()
        connection.close()
        # print(item.keys())
        username=item[0]
        password=item[1]
        print(username)
        print(password)
        print(kode)
        post=go_url().login_page(url,kode)
        name_image = re.sub(r'[^a-zA-Z0-9]', '', url)
        connection = sqlite3.connect('data/riwayat_instagram.db')
        conn = connection.cursor()
        cursor = conn.execute("SELECT * from '{}'".format(url))
        item = cursor.fetchall()
        cursor2 = conn.execute('SELECT * from riwayat_instagram WHERE url="{}"'.format(url))
        item2 = cursor2.fetchone()
        connection.commit()
        conn.close()
        conn.close()
        name_image = 'images/' + name_image + '.png'
        print(name_image)
    return render_template('tabel_identifikasi.html', item=item, name_image=name_image, item2=item2,kode=kode)