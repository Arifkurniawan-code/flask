from flask import Flask,render_template,request,url_for,session,redirect,flash
from Prepocessing_sentence import text_prepocessing
from lstm_model import LSTM_model
from instagram_scrape.ScrapeInstagram import go_url
app=Flask(__name__)
app.secret_key = 'super secret key'
import os
import pandas as pd
import sqlite3

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/admin',methods=['GET','POST'])
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

@app.route('/session')
def get_session():
    if 'username' in session:
        s=session['username']
        return s

def loading():
    print('INI LOADER')
    return render_template('loader.html')

@app.route('/tambah_data',methods=['GET','POST'])
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

@app.route('/perbarui_model',methods=['GET','POST'])
def perbarui_model():
    x = get_session()
    if x:
        outcome=loading()
        model=LSTM_model().new_model()
        return redirect('admin',message='Berhasil memperbarui Model')
    else:
        return render_template('session.html', message='No Session Available')

@app.route('/hasil_postingan',methods=['GET','POST'])
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

@app.route('/bot_instagram',methods=['GET','POST'])
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

@app.route('/admin_home',methods=['GET','POST'])
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

@app.route('/lihat_data',methods=['GET','POST'])
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

@app.route('/instagram_post',methods=['GET','POST'])
def instagram_post():
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
    post=go_url().login_page('https://www.instagram.com/p/Bd47GDYB_Bu/')
    # post = go_url().login_page('https://www.instagram.com/p/CA7ChUxnBRQ/')
    # arif.post_page('https://www.instagram.com/p/CA1c8b4DIFA/')
    return 'Success'

@app.route('/grafik',methods=['GET','POST'])
def grafik():
    x = get_session()
    if x:
        return render_template('grafik_model.html')
    else:
        return render_template('session.html', message='No Session Available')

@app.route('/riwayat_uji',methods=['GET','POST'])
def riwayat_uji():
    x = get_session()
    if x:
        connection = sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        cursor=conn.execute('SELECT * FROM riwayat')
        item = cursor.fetchall()
        cursor=conn.execute('SELECT * FROM riwayat_instagram')
        item2=cursor.fetchall()
        connection.commit()
        conn.close()
        connection.close()
        return render_template('riwayat_uji.html',item1=item,item2=item2)
    else:
        return render_template('session.html', message='No Session Available')

@app.route('/instagram',methods=['GET','POST'])
def post():
    df=pd.read_excel('instagram_scrape/komentar/CA1c8b4DIFA.xlsx')
    return render_template('post.html',column_names=df.columns.values,row_data=list(df.values.tolist()),link_column='name',zip=zip)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('admin')
    else:
        return '<p>user already logged out</p>'

@app.route('/prediction',methods=['POST',"GET"])
def predict_sentiment():
    if request.method=='POST':
        comment_text=request.form['kalimat']
        comment_text=text_prepocessing(comment_text)
        print(comment_text)
        model=LSTM_model()
        dict={}
        dict=model.predict_comment(comment_text)
        print(dict['class'])
        print(dict['probabilities'][1])
        if(dict['class']==[0]):
            Label=0
            sentiment='Cyberbullying'
        elif(dict['class']==[1]):
            Label = 1
            sentiment='Irrelevant'
        elif (dict['class'] == [2]):
            Label = 2
            sentiment = 'Netral'
        else:
            Label = 3
            sentiment='Bukan Cyberbullying'
        connection = sqlite3.connect('data/Admin.db')
        conn=connection.cursor()
        conn.execute('INSERT INTO riwayat(kalimat,label) VALUES ((?),(?))',(comment_text,Label))
        connection.commit()
        conn.close()
        connection.close()
    return render_template('index.html',text=comment_text,classification=sentiment,prob_cyb=dict['probabilities'][0],
                           prob_ir=dict['probabilities'][1],prob_net=dict['probabilities'][2],
                           prob_non=dict['probabilities'][3])

if __name__=='__main__':
    app.run()