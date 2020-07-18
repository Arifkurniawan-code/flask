from flask import Flask,render_template,request,url_for,session,redirect,flash
from Prepocessing_sentence import text_prepocessing
from lstm_model import LSTM_model
import sqlite3
from instagram_scrape.ScrapeInstagram import go_url

def get_session():
    if 'username' in session:
        s=session['username']
        return s
def loading():
    print('INI LOADER')
    return render_template('loader.html')

def login():
    connection = sqlite3.connect('data/Admin.db')
    conn=connection.cursor()
    print('database loaded')
    if request.method=='POST':
        try:
            get_username=request.form['username']
            get_password=request.form['password']
            user=conn.execute("SELECT username FROM admin_login where username=(?)",[get_username])
            username_true=user.fetchone()
            pwd=conn.execute("SELECT password FROM admin_login where password=(?)",[get_password])
            password_true=pwd.fetchone()
            conn.close()
            connection.commit()
            connection.close()
            if username_true:
                if password_true:
                    session['username'] = get_username
                    return  redirect("admin_home")
                else:
                    flash("Kata sandi anda salah")
            else:
                flash("Nama Pengguna Tidak Ditemukan")
        except:
            connection.rollback()
            flash("Terjadi kesalahan dalam mengisi form login")
    return render_template('login.html')

def tambah_data():
    connection = sqlite3.connect('data/Admin.db')
    conn=connection.cursor()
    x = get_session()
    if x:
        if request.method=='POST':
            kalimat=request.form['kalimat']
            label = request.form['label']
            print(kalimat)
            print(label)
            if label=='Label...':
                flash('Data Tidak Lengkap',category='danger')
            else:
                if label=='Cyberbullying':
                    label=0
                elif label=='Irrelevant':
                    label=1
                elif label=='Netral':
                    label=2
                else:
                    label=3
                print(label)
                print(kalimat)
                conn.execute('INSERT INTO train (field1,field2) VALUES ((?),(?))', (kalimat,label))
                conn.close()
                connection.commit()
                connection.close()
                flash('Berhasil Menambahkan Data',category='success')
            return redirect('/admin_home')
    else:
        return render_template('session.html', message='No Session Available')

def perbarui_model():
    x = get_session()
    if x:
        outcome=loading()
        model=LSTM_model().new_model()
        return render_template('admin_homepage.html',message='Berhasil memperbarui Model')
    else:
        return render_template('session.html', message='No Session Available')

def hasil_postingan():
    x = get_session()
    if x:
        connection = sqlite3.connect('data/riwayat_instagram.db')
        conn = connection.cursor()
        print('database loaded')
        url = request.args.get('url')
        cursor = conn.execute('SELECT * FROM "{}"'.format(url))
        item = cursor.fetchall()
        conn.close()
        connection.commit()
        connection.close()
        return render_template('hasil_postingan.html', items=item)
    else:
        return render_template('session.html', message='No Session Available')

def bot_instagram():
    x=get_session()
    if x:
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            id = request.args.get('id')
            url='https://www.instagram.com/{}/'.format(username)
            print(url)
            post = go_url().profile_screenshoot(username,password,url)
            if post==True:
                connection=sqlite3.connect('data/Admin.db')
                conn=connection.cursor()
                conn.execute('UPDATE instagram SET username="{}",password="{}" where id=1'.format(username,password))
                connection.commit()
                conn.close()
                connection.close()
                flash('Username dan Password anda berhasil diperbarui', category='success')
                return redirect('/bot_instagram')
            else:
                flash('Username atau Password anda salah',category='danger')
                return redirect('/bot_instagram')
        else:
            return render_template('bot_instagram.html')
    else:
        return render_template('session.html', message='No Session Available')

def admin_homepage():
    x=get_session()
    if x:
        print('Session Available')
        connection = sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        print('database loaded')
        num_cb=conn.execute('select count(field1) from train WHERE field2=0').fetchone()[0]
        num_ir = conn.execute('select count(field1) from train WHERE field2=1').fetchone()[0]
        num_net = conn.execute('select count(field1) from train WHERE field2=2').fetchone()[0]
        num_non = conn.execute('select count(field1) from train WHERE field2=3').fetchone()[0]
        cursor = conn.execute('SELECT * FROM train')
        item=cursor.fetchall()
        conn.close()
        connection.commit()
        connection.close()
        return render_template('admin_homepage.html',items=item,num_cb=num_cb,num_ir=num_ir,num_net=num_net,num_non=num_non)
    else:
        return render_template('session.html',message='No Session Available')

def lihat_data():
    x = get_session()
    if x:
        connection = sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        print('database loaded')
        label = request.args.get('score')
        cursor = conn.execute('SELECT * FROM train WHERE field2=(?)', [label])
        item=cursor.fetchall()
        conn.close()
        connection.commit()
        connection.close()
        return render_template('lihat_data.html', items=item)
    else:
        return render_template('session.html', message='No Session Available')

def grafik():
    x = get_session()
    if x:
        return render_template('grafik_model.html')
    else:
        return render_template('session.html', message='No Session Available')

def riwayat_uji():
    x = get_session()
    if x:
        connection = sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        cursor=conn.execute('SELECT * FROM riwayat')
        item = cursor.fetchall()
        connection.commit()
        conn.close()
        connection.close()
        connection = sqlite3.connect('data/riwayat_instagram.db')
        conn = connection.cursor()
        cursor = conn.execute('SELECT * FROM riwayat_instagram')
        item2 = cursor.fetchall()
        connection.commit()
        conn.close()
        connection.close()
        return render_template('riwayat_uji.html',item1=item,item2=item2)
    else:
        return render_template('session.html', message='No Session Available')

def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('admin')
    else:
        return '<p>user already logged out</p>'