import sqlite3
def history(url, username, caption,likes):
    connection=sqlite3.connect('data/riwayat_instagram.db')
    conn=connection.cursor()
    try:
        conn.execute('INSERT INTO riwayat_instagram(url,username,caption,likes) VALUES(?,?,?,?)',
                     (url, username, caption, likes))
    except:
        conn.execute('UPDATE riwayat_instagram SET username="{}",caption="{}",likes="{}" WHERE url="{}"'.format(username, caption, likes,url))
    connection.commit()
    conn.close()
    connection.close()

def export(url,tuple,username,caption,likes):
    connection=sqlite3.connect('data/riwayat_instagram.db')
    print('database opened')
    print(url)
    print(tuple)
    conn=connection.cursor()
    try:
        print('a')
        conn.execute(
            'CREATE TABLE "{}"("id" INTEGER PRIMARY KEY AUTOINCREMENT,"komentar" TEXT,"names" TEXT,"label"	TEXT)'.format(url))
        try:
            print('b')
            conn.executemany('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
        except:
            print('c')
            conn.execute('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
    except:
        try:
            print('d')
            conn.executemany('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
        except:
            print('e')
            conn.execute('INSERT INTO "{}"(names,komentar,label) VALUES (?,?,?)'.format(url),tuple)
    connection.commit()
    conn.close()
    connection.close()
    history(url,username,caption,likes)
