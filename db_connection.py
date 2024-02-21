import mysql.connector

class DB_Handler:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host= 'localhost',
                user="root",
                password= 'root',
                database= "clients",
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
            return result
        else:
            print("DB is not connected")

    def info_add(self,info):
        add_info_query = f"INSERT INTO clients_info(name,height_in_cm,weight_in_kg,gender,age,bmi,bmi_classifier,lifestyle,goal,bmr,kcal_goal)" \
                         f"VALUES('{info['name']}','{info['height']}','{info['weight']}','{info['gender']}','{info['age']}','{info['BMI']}','{info['BMI_classifier']}','{info['lifestyle']}','{info['goal']}','{info['BMR']}','{info['Kcal Goal']}')"

        if self.connection.is_connected():
            if self.info_check_exist(info['name']):
                try:
                    self.cursor.execute(add_info_query)
                except (mysql.Error, mysql.Warning) as e:
                    print(e)
                else:
                    self.connection.commit()
                    print("Row Added Successfully")
                    self.cursor.close()
            else:
                print("User Already Exists")
        else:
            print("DB is not connected")

    def info_check_exist(self, name):
        self.cursor.execute(f"SELECT * FROM clients_info where id = '{name}'")
        result = self.cursor.fetchall()
        if not result:
            return False
        else:
            return True







