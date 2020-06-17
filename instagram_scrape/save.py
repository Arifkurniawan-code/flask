import sqlite3
def history(url):
    connection=sqlite3.connect('data/Admin.db')
    conn=connection.cursor()
    conn.execute('INSERT INTO riwayat_instagram(url) VALUES(?)',[url])
    connection.commit()
    conn.close()
    connection.close()

def export(names, comments, label, url,tuple):
    connection=sqlite3.connect('data/riwayat_instagram.db')
    print('database opened')
    print(url)
    conn=connection.cursor()
    try:
        conn.execute(
            'CREATE TABLE "{}"("id" INTEGER PRIMARY KEY AUTOINCREMENT,"komentar" TEXT,"names" TEXT,"label" INTEGER)'.format(url))
        try:
            conn.executemany('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
        except:
            conn.execute('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
    except:
        try:
            conn.executemany('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
        except:
            conn.execute('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
    connection.commit()
    conn.close()
    connection.close()
    history(url)