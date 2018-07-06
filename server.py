from flask import *
import sqlite3 
import numpy as np

app = Flask(__name__)
DATABASE = 'data.db'
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(DATABASE)
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
    
@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into remainder (id,name,date ) values (?, ?, ?)',
                 [int(np.random.randint(100000, size=1)),request.form['name'], request.form['date']])
    db.commit()
    return redirect('/')

@app.route('/add_page')
def add_enteries():
    return render_template('add.html')
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select * from remainder')
    entries = cur.fetchall()
    return render_template('index.html', data=entries)
    
@app.route('/update_page')
def update_page():
    db = get_db()
    cur = db.execute('select id from remainder')
    entries = cur.fetchall()
    return render_template('update.html',data=entries)
    
@app.route('/update', methods=['POST'])
def update_entries():
    db = get_db()
    db.execute('update remainder set name=?,date=? where id=?',[request.form['name'], request.form['date'], request.form['id']])
    db.commit()
    return redirect('/')


if __name__=="__main__":
    app.secret_key = 'hsnck#127sb!!2'
    app.debug = True
    app.run()
