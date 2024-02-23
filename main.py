import flask_login
import html_forms
from candidate import Candidate
from pdf_manipulation import Pdf
from db_connection import DB_Handler
from AI_Handler import AI_Handler
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.secret_key = 'admin'  # Change this!

login_manager = LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def get_user(id):
    user = User()
    user.id = id
    return user

@login_manager.request_loader
def request_loader(request):
    all_emails = [users['Email'] for users in database.login_fetch_all()]
    email = request.form.get('email')
    if email not in all_emails:
        return

    user = User()
    user.id = email
    return user

database = DB_Handler()
@app.route("/register", methods=["GET", "POST"])
def register():
    form = html_forms.Resigter()
    if request.method == "GET":
        print(request)

        return render_template("register.html", form=form)

    if request.method == "POST":
        data = request.form
        database.register_user(data)
        user_details = database.get_user(data)[0]
        v = {"ID" : user_details[0], "username" : {user_details[1]}, "name" : f'{user_details[2]} {user_details[3]}'}
        database.info_add_id_and_name(v)

        return redirect("login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template("index.html")
        login_form = html_forms.Login()
        return render_template("/login.html" , form=login_form)

    if request.method == "POST":
        data = request.form
        print(data['password'])

        worked, response = database.login_db_check(data['email'],data['password'])
        if worked:
            user = User()
            print("worked")
            user.id = response[0]
            user.name = "Tom"
            flask_login.login_user(user)
            return redirect(url_for('protected'))
        else:
            print(response)

        return redirect("login")

@app.route('/My Dashboard')
@flask_login.login_required
def protected():
    if current_user.is_authenticated:
        id = current_user.get_id()
        user_info = (database.get_user_info(id))[0]
    return render_template("profile.html" ,user_info = user_info)

@app.route("/info_update" , methods=["GET", "POST"])
@flask_login.login_required
def info_update():
    info_update_form = html_forms.info_update_form()
    id =  current_user.get_id()
    if request.method == "GET" :
        return render_template("info_update.html" , form=info_update_form)

    if request.method == "POST":
        data = request.form
        person = Candidate(data)
        database.update_info(id,data)
        return render_template("info_update.html" , form=info_update_form)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("index")


# pdf = Pdf("Testing")
# ai_handler = AI_Handler()
# person.info_stats_pdf_gen()

if __name__ == "__main__":
    app.run(debug=True)
