import psycopg2

class User:
    def __init__(self,username):
        self.username = username
        self.auth = False
        self.active = False

    def authenticate(self,password):
        con = psycopg2.connect(port="5432", host="localhost", user="alyson", password="123456",
                               dbname="alfredsDB")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM public.\"Users\" WHERE \"Name\"='"+self.username+"'")
        result = cursor.fetchone()
        print(result)
        if result[1]==password:
            self.auth = True
        else:
            self.auth = False

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username