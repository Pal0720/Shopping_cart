import datetime
import psycopg2

db = psycopg2.connect(host='localhost',user='postgres', password ='Mozart&bach3', dbname ='shopping_cart')
mycursor = db.cursor()

username = input("Enter your username : ")
password = input("Enter your password : ")

mycursor.execute("SELECT * FROM users WHERE user_name = %s and password = %s", (username, password))
user_result = mycursor.fetchone()
print(f"Welcome : {username}. You login as {user_result[3]}")