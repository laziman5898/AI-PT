import mysql.connector


class DB_Handler:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user="root",
                password='root',
                database="clients",
            )
        except mysql.connector.Error as E:
            print(E)
        else:
            self.cursor = self.connection.cursor()

    def login_fetch_all(self):
        select_all_query = "SELECT * FROM clients_login"
        if self.connection.is_connected():
            self.cursor.execute(select_all_query)
            result = self.cursor.fetchall()
            desc = self.cursor.description
            col_names = [col[0] for col in desc]
            data = [dict(zip(col_names, row)) for row in result]

            return data
        else:
            print("DB is not connected")

    def macro_data_exists(self, id):
        query = f"SELECT * FROM macro_breakdown where clients_login_id = '{id}' "
        self.cursor.execute(query)
        response = self.cursor.fetchall()

        if not response:
            return False
        else:
            return True

    def update_info(self, id ,info):

        add_query = f"UPDATE clients_info " \
                    f"SET height_in_cm = '{info['height']}' , weight_in_kg = '{info['weight']}', gender = '{info['gender']}', age = '{info['age']}', bmi = '{info['BMI']}', bmi_classifier = '{info['BMI_classifier']}'" \
                    f"WHERE clients_login_ID = {id};"

        self.cursor.execute(add_query)
        self.connection.commit()
        print("Row Added Successfully")

    def update_info_macro_calc(self, id ,info):

        update_clients_info_query = f"UPDATE clients_info " \
                    f"SET BMR = '{info['BMR']}' , goal = '{info['goal']}', lifestyle = '{info['lifestyle']}', kcal_goal = '{info['Kcal Goal']}'" \
                    f"WHERE clients_login_ID = {id};"

        self.cursor.execute(update_clients_info_query)
        self.connection.commit()

        if self.macro_data_exists(id):
            update_macro_breakdown_query = f"UPDATE macro_breakdown " \
                                        f"SET proten_intake = {info['kcal_breakdown']['proteins'][0]}, carb_intake = {info['kcal_breakdown']['carbohydrates'][0]}, fat_intake = {info['kcal_breakdown']['fats'][0]}, protien_kcal={info['kcal_breakdown']['proteins'][1]} , carb_kcal={info['kcal_breakdown']['carbohydrates'][1]}, fat_kcal={info['kcal_breakdown']['fats'][1]} " \
                                        f"WHERE clients_login_ID = {id}"

            self.cursor.execute(update_macro_breakdown_query)
            self.connection.commit()

            print("Row  Successfully")
        else:
            update_macro_breakdown_query =  f"INSERT INTO macro_breakdown(clients_login_ID , proten_intake, carb_intake , fat_intake, protien_kcal,carb_kcal,fat_kcal)" \
                                            f"VALUES('{id}','{info['kcal_breakdown']['proteins'][0]}','{info['kcal_breakdown']['carbohydrates'][0]}',{info['kcal_breakdown']['fats'][0]},'{info['kcal_breakdown']['proteins'][1]}','{info['kcal_breakdown']['carbohydrates'][1]}',{info['kcal_breakdown']['fats'][1]})"
            self.cursor.execute(update_macro_breakdown_query)
            self.connection.commit()

        print("Row Added")

    def info_add_id_and_name(self, data):
        add_info_query = f"INSERT INTO clients_info(clients_login_ID, name, spoonacular_username,spoonacular_password,spoonacular_hash)" \
                         f"VALUES('{data['ID']}','{data['name']}', '{data['spoonacular_username']}', '{data['spoonacular_password']}','{data['spoonacular_hash']}')"
        self.cursor.execute(add_info_query)
        self.connection.commit()
        print("Row Added Successfully")

    def get_user(self, data):
        query = f"SELECT * FROM clients_login where Username = '{data['username']}'"
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

    def info_check_exist(self, id):
        self.cursor.execute(f"SELECT * FROM clients_info where id = '{id}'")
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def login_check_exist(self, name):
        self.cursor.execute(f"SELECT * FROM clients_info where id = '{name}'")
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True

    def register_user(self, data):
        query = "INSERT INTO clients_login(Username,`First Name`,`Last Name`,`Email`,`Password`)" \
                f" VALUES('{data['username']}','{data['first_name']}','{data['last_name']}','{data['email']}','{data['password']}')"
        self.cursor.execute(query)
        self.connection.commit()
        print("Successfully Added to login")

    def login_db_check(self, email, password):
        self.cursor.execute(f"SELECT * FROM clients_login where Email =  '{email}'")
        result = self.cursor.fetchall()
        if not result:
            print("Email does not exist")
            return False , "Error"
        else:
            if password == (result[0][5]):
                print("correct password")
                return True, result[0]
            else:
                print("Incorrect Password")
                return False , "Error"
    def get_user_info(self, id):
        query = f"SELECT * FROM clients_info where clients_login_ID = {id}"
        self.cursor.execute(query)
        response = self.cursor.fetchall()

        desc = self.cursor.description
        col_names = [col[0] for col in desc]
        data = [dict(zip(col_names, row)) for row in response]
        return data


