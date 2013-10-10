import os
from daos import *
import datetime, time, random
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, json

app = Flask(__name__)

app.config.update(dict(
    DATABASE='/tmp/mafia.db',
    DEBUG=True,
    SECRET_KEY='development key'
))
app.config.from_envvar('MAFIA_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def check_authorization(username, password):
    db = get_db()
    cur = db.execute('select userName, hashedPassword from users')
    rows = cur.fetchall()
    for row in rows:
        if row[0] == username and row[1] == password:
            return bool(1)
    return bool(0)
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/game_show')
def show_games():
    db = get_db()
    cur = db.execute('select dateCreated, time from games order by dateCreated')
    games = cur.fetchall()
    cur1 = db.execute('select id from players order by id')
    players = cur1.fetchall() 
    return render_template('loggedin.html', games=games, players=players)

@app.route('/')
def show_users():
    db = get_db()
    cur = db.execute('select firstName, lastName from users order by firstName')
    users = cur.fetchall()
    return render_template('homepage.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    db = get_db()
    db.execute('insert into users (firstName, lastName, userName, hashedPassword, isAdmin) values (?, ?, ?, ?, ?)',
    [request.form['firstName'], request.form['lastName'], request.form['userName'], request.form['hashedPassword'], request.form['isAdmin']])
    db.commit()
    flash('New user was successfully posted')
    return redirect(url_for('show_users'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not check_authorization(request.form['username'], request.form['password']):
            error = 'Username/password combination are incorrect'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return render_template('loggedin.html', error=error)
    return render_template('login.html', error=error)

@app.route('/create_game', methods=['POST'])
def create_game():
    db = get_db()
    x = db.execute('select count(id) from games')
    y = x.fetchone()
    if y[0] < 1:
        Game(request.form['dayNight'], datetime.date.today())
        dayNight = request.form['dayNight']
        if dayNight == '' or dayNight <= 0:
            dayNight = 1
        db.execute('insert into games (dayNight, dateCreated) values (?, ?)',
        [dayNight, datetime.date.today()])
        db.commit()
    else:
        flash('A game is already created')
    return redirect(url_for('show_games'))

@app.route('/join_game', methods=['POST'])
def join_game():
    db = get_db()
    x = db.execute('select id from users where userName=?', [session['username']])
    y = x.fetchone()
    db.execute('insert into players (isDead, lat, lng, userID, isWerewolf) values (?, ?, ?, ?, ?)',
    (0, 0, 0, y[0], 0))
    db.commit()
    flash('You successfully joined a game')
    return redirect(url_for('show_games'))

@app.route('/start_game', methods=['POST'])
def start_game():
    db=get_db()
    x = db.execute('select count(*) from games')
    y = x.fetchone()
    a = db.execute('select count(*) from players')
    b = a.fetchone()
    if (y[0] == 1 and b[0] > 0) :
        werewolves = int(b[0] * .3)
        if werewolves == 0:
            werewolves = 1
        while (werewolves != 0):
            if b[0] == 1:
                value = 1
            else:
                value = random.randrange(1,b[0])
            p = db.execute('select isWerewolf from players where id=?', [value])
            q = p.fetchone()
            if q[0] == 1:
                continue
            db.execute('update players set isWerewolf=1 where id=?', [value])
            db.commit()
            werewolves = werewolves - 1
        start = time.time()
        db.execute('update games set time=?', [start])
        db.commit()
    else:
        flash('A game must first be created')
    return redirect(url_for('show_games'))

@app.route('/kill', methods=['POST', 'GET'])
def kill():
    db = get_db()
    k = db.execute('select * from users where userName=?', [session['username']] )
    l = k.fetchone()
    x = db.execute('select * from players where userID=?', [l[0]])
    y = x.fetchone()
    a = db.execute('select * from games')
    b = a.fetchone()
    diff = (time.time() - b[3])
    timeNow = (int(diff)/int(b[1]))
    if (timeNow/60) % 2 == 0:
        #y[5] == 1 b[0] != 0
        e = db.execute('select * from users where userName=?', [request.form['dropdown']])
        f = e.fetchall()
        m = db.execute('select * from players where isDead=0')
        n = m.fetchall()
        db.execute('insert into kills (killerID, victimID, timestamp, lat, lng) values (?, ?, ?, ?, ?)',
                    [x[0], f[0], time.time(), x[2], x[3]])
        db.execute('update players set isDead=1 where id=?', f[0])
        db.commit()
        flash('You killed ?', [request.form['dropdown']])
        return redirect(url_for('game_screen'))
    return redirect(url_for('game_screen'))   

@app.route('/game')
def game_screen():
    db = get_db()
    x = db.execute('select count(*) from games')
    y = x.fetchone()
    a = db.execute('select * from games')
    b = a.fetchone()
    z = db.execute('select id, isWerewolf from players where isDead=0')
    z1 = z.fetchall()
    if (y[0] == 1 and b[0] != None):
        status = 'Game in session'
        diff = (time.time() - b[3])
        timeNow = (int(diff)/int(b[1]))
        if (timeNow/60) % 2 == 0:
            timePeriod = 'Day'
        else:
            timePeriod = 'Night'
    else:
        status = 'Game not in session'
        timePeriod = 'N/A'
    return render_template('game.html', status=status, timePeriod=timePeriod, players=z1)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_users'))

@app.route('/game_home', methods=['GET', 'POST'])
def home_game():
    error = None
    return redirect(url_for('game_screen'))

if __name__ == '__main__':
    init_db()
    app.run(debug = True)
