#------ Flask imports
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
import flask_login

#---- Internal Imports
import html_forms
from candidate import Candidate
from pdf_manipulation import Pdf
from db_connection import DB_Handler
from AI_Handler import AI_Handler
from spoonacular_API import Spoonacular_Handler


app = Flask(__name__)
app.secret_key = 'admin'  # Change this!

login_manager = LoginManager()
login_manager.init_app(app)


def db_person_data_converstion(db_data):
    height = db_data['height_in_cm']
    weight = db_data['weight_in_kg']
    gender = db_data['gender']
    age = db_data['age']
    bmi = db_data['bmi']

    data = {'height': height,
            'weight': weight,
            'age': age,
            'gender': gender,
            'bmi': bmi
            }
    person = Candidate(data)

    return person

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

@app.route("/" , methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = html_forms.Resigter()
    if request.method == "GET":
        print(request)

        return render_template("register.html", form=form)

    if request.method == "POST":
        data = request.form
        database.register_user(data)
        user_details = database.get_user(data)[0]

        # Add some verification so if user already exists ...
        spoonacular = Spoonacular_Handler(username=user_details[1], first_name=user_details[2], last_name=user_details[3], email=user_details[4])
        r = spoonacular.create_user()

        v = {"ID" : user_details[0], "username" : {user_details[1]}, "name" : f'{user_details[2]} {user_details[3]}' , 'spoonacular_username':r['username'],'spoonacular_password':r['spoonacularPassword'],'spoonacular_hash': r['hash']}



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
            flask_login.login_user(user)
            return redirect(url_for('profile'))
        else:
            print(response)

        return redirect("login")

@app.route('/My Dashboard')
@flask_login.login_required
def profile():
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
        person.bmi_classifier()
        database.update_info(id,person.info)
        return render_template("info_update.html" , form=info_update_form)

@app.route("/Health Goals" , methods=["GET","POST"])
@flask_login.login_required
def health_goals():
    goals_form = html_forms.goals_form()
    if request.method=="GET":
        goals_form= html_forms.goals_form()
        return render_template("health goals.html", form=goals_form)

    if request.method == "POST":
        data = request.form
        id = current_user.get_id()
        user_info = database.get_user_info(id)[0]
        person = db_person_data_converstion(user_info)
        person.bmi_classifier()
        person.set_goals(goal=request.form['goal'], lifestyle=int(request.form['lifestyle']))
        person.macro_calc()
        
        database.update_info_macro_calc(id,person.info)
        print(person.info['kcal_breakdown'])

        return render_template("health goals.html", form=goals_form)

@app.route("/Dietary Preferences" , methods=["GET" , "POST"])
@flask_login.login_required
def dietary_preferences():
    preference = html_forms.dietary_preference()

    if request.method == "GET":
        return render_template("dietary_preferences.html", form=preference)
    elif request.method == "POST":
        diet_requirements = list(request.form.listvalues())
        print(diet_requirements[0])

        return render_template("dietary_preferences.html", form=preference)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("/")

@login_manager.unauthorized_handler
def unauthorized_handler():
    print("Redirect to Homepage")
    return redirect("/")


# pdf = Pdf("Testing")
# ai_handler = AI_Handler()
# person.info_stats_pdf_gen()

if __name__ == "__main__":
    app.run(debug=True)


