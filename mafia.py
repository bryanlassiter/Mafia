from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/mafia.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
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


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_users():
    db = get_db()
    cur = db.execute('select firstName, lastName from users order by firstName')
    users = cur.fetchall()
    return render_template('show_entries.html', users=users)

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
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_users'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_users'))

class Player(object):
    def __init__(self, id, isDead, lat, lng, userID, isWerewolf):
        self.id = id
        self.isDead = isDead
        self.lat = lat
        self.lng = lng
        self.userID = userID
        self.isWerewolf = isWerewolf
va

if __name__ == '__main__':
    init_db()
    app.run()
