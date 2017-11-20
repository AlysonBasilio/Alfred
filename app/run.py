import flask
import psycopg2
import flask_login
from app.models.User import User

app = flask.Flask(__name__, static_url_path='')
app.secret_key = 'comp18'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
con = psycopg2.connect(port="5432", host="localhost", user="alyson", password="123456",
                               dbname="alfredsDB")
cursor = con.cursor()

def validate(username):
    completion = False
    cursor.execute("SELECT \"Name\" FROM public.\"Users\"")
    rows = cursor.fetchall()
    for row in rows:
        dbUser = row[0]
        if dbUser==username:
            completion=True
            break
    return completion

@login_manager.user_loader
def user_loader(email):
    if not validate(email):
        return
    user = User(email)
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not validate(email):
        return

    user = User(email)

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.authenticate(request.form['password'])
    return user

@app.route('/')
def redirect():
    return flask.redirect(flask.url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template("login.html")

    if flask.request.method == 'POST':
        print(flask.request.form)

    email = flask.request.form['username']
    user = User(email)
    user.authenticate(flask.request.form['password'])
    if user.is_authenticated():
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/index', methods=['GET', 'POST'])
@flask_login.login_required
def index():
    if flask.request.method == 'POST':
        print(flask.request.form)
        if not InsertActivitiesOfDay(flask.request.form['hour'],flask.request.form['day'], flask.request.form['description'], flask.request.form['priority'], flask.request.form['tag']):
            return "<p>Você já tem um compromisso nesse dia e horário. <a href='/index'>Retornar</a></p>"
    return flask.render_template("index.html")

def InsertActivitiesOfDay(hour, day, description, priority, tag):
    try:
        cursor.execute("""  INSERT INTO public.\"Alfreds\"(\"Description\", \"Tag\", \"Priority\", day_of_week, \"Time\", username)
                            VALUES ('"""+description+"""','"""+tag+"""','"""+priority+"""','"""+day+"""','"""+hour+"""', '"""+flask_login.current_user.username+"""')""")
        con.commit()
        return True
    except Exception as e:
        con.commit()
        print(e)
        return False


@app.route('/static/<path:path>')
def send_js(path):
    return flask.send_from_directory('static', path)


@app.route('/loadbadges')
@flask_login.login_required
def background_process():
    try:
        cursor.execute("""  SELECT day_of_week
                            FROM public.\"Alfreds\"
                            WHERE username = '"""+flask_login.current_user.username+"""'""")
        list = {'MON':0,
                'TUE':0,
                'WED':0,
                'THU':0,
                'FRI':0,
                'SAT':0,
                'SUN':0}
        alarms = cursor.fetchall()
        for i in alarms:
            list[i[0]]+=1
        print(list)
        json = flask.jsonify(list)
        return json
    except Exception as e:
        print(e)
        return flask.jsonify(error=str(e))


@app.route('/getActivitiesOfDay')
@flask_login.login_required
def getActivitiesOfDay():
    try:
        text = str(flask.request.args.get('day_of_week'))
        print(text)
        cursor.execute("""  SELECT *
                            FROM public.\"Alfreds\"
                            WHERE day_of_week = '"""+text+"""'
                            AND username = '"""+flask_login.current_user.username+"""'""")
        alarms = cursor.fetchall()
        list=[]
        for i in alarms:
            list.append({
                'hour':i[4],
                'description':i[0],
                'priority':i[2],
                'tag':i[1]
            })
        json = flask.jsonify(list)
        return json
    except Exception as e:
        print(e)
        return flask.jsonify(error=str(e))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        if not addNewUser(flask.request.form['username'], flask.request.form['password']):
            return "<p>Usuário já existente: <a href='/register'>Voltar</a></p>"
        return "<p>Registrated: <a href='/login'>Login</a></p>"
    return flask.render_template("register.html")

def addNewUser(username,password):
    try:
        cursor.execute("""  INSERT INTO public.\"Users\"(\"Name\", \"Password\")
                                            VALUES ('""" + username + """','""" +
                      password + """')""")
        con.commit()
        return True
    except Exception as e:
        con.commit()
        print(e)
        return False

if __name__ == "__main__":
    print("Entrou aqui")
    app.run(host='0.0.0.0')