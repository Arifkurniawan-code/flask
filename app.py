from flask import Flask,render_template,request,url_for,session,redirect,flash
app=Flask(__name__)
app.secret_key = 'super secret key'
import admin
import user

@app.route('/',methods=['GET','POST'])
def home():
    return user.home()

@app.route('/uji_komentar',methods=['GET','POST'])
def uji_komentar():
    return user.uji_komentar()

@app.route('/post_identifikasi',methods=['GET','POST'])
def post_identifikasi():
    return render_template('post_identifikasi.html')

@app.route('/bot_post',methods=['GET','POST'])
def bot_post():
    return render_template('bot_post.html')
@app.route('/instagram_post',methods=['GET','POST'])
def instagram_post():
    return user.instagram_post()

@app.route('/admin',methods=['GET','POST'])
def login():
    return admin.login()

@app.route('/session')
def get_session():
    return admin.get_session()

@app.route('/tambah_data',methods=['GET','POST'])
def tambah_data():
    return admin.tambah_data()

@app.route('/perbarui_model',methods=['GET','POST'])
def perbarui_model():
    return admin.perbarui_model()

@app.route('/hasil_postingan',methods=['GET','POST'])
def hasil_postingan():
   return admin.hasil_postingan()

@app.route('/bot_instagram',methods=['GET','POST'])
def bot_instagram():
    return admin.bot_instagram()

@app.route('/admin_home',methods=['GET','POST'])
def admin_homepage():
    return admin.admin_homepage()

@app.route('/lihat_data',methods=['GET','POST'])
def lihat_data():
    return admin.lihat_data()

@app.route('/grafik',methods=['GET','POST'])
def grafik():
    return admin.grafik()

@app.route('/riwayat_uji',methods=['GET','POST'])
def riwayat_uji():
    return admin.riwayat_uji()

@app.route('/logout')
def logout():
    return admin.logout()

if __name__=='__main__':
    app.run(debug=True)