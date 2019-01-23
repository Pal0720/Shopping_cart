import datetime
import psycopg2

db = psycopg2.connect(host='localhost',user='postgres', password ='**********', dbname ='shopping_cart')
mycursor = db.cursor()

#signup customer (not included in the program)

print("########################")
print("Welcome to the Appin Supermarket")
print("########################")

#Login as admin or customer

while(True):
    username = input("Enter your username : ")
    password = input("Enter your password : ")

    try:
        mycursor.execute("SELECT * FROM users WHERE user_name={} and password={}".format(username, password))
        user_result = mycursor.fetchone()
        print(f"Welcome : {username}. You login as {user_result[3]}")
        break
    except Exception as arg:
        print("Wrong username or password.. Please try again..! : ", arg)



# create for Admin
if user_result[3] == 'admin':
    choice = input("Hello Admin, What do you want to do today : \n1)Add products \n2)See Customer data : \nChoice : ")

    if choice == '1':
        input_category = input("Enter the category of the product you want to add : ")
        name =  input("Enter the name of the product you want to add : ")
        price =  input("Enter the price of the product : ")
        stock =  input("Enter the stock quantity of the product : ")
        description = input("Enter some description about the product : ")

        mycursor.execute("SELECT * FROM categories WHERE cat_name = {}".format(input_category))
        check_category = mycursor.fetchone()
        if check_category is None:
            mycursor.execute("INSERT INTO categories(cat_name) VALUE {}".format(input_category))
            db.commit()
        # need another query to get the category_id, if a new one is added.
        mycursor.execute("SELECT * FROM categories WHERE cat_name = {}".format(input_category))
        category_result = mycursor.fetchone()
        mycursor.execute("INSERT INTO products(product_name,price,stock,description,category) VALUES ({}, {}, {}, {}, {})".format(name, price, stock, description,category_result[0]))
        db.commit()

    elif choice == '2':
        customer_choice = input("Do you want to see \n1)all customer data or \n2)particular customer : \nChoice : ")
        if customer_choice == '1':
            mycursor.execute("SELECT * FROM user_history")
            result = mycursor.fetchall()
            for i in result:
                print(i)
        elif customer_choice == '2':
            user_choice = input("Enter the username to check for details : ")
            try :
                mycursor.execute("SELECT user_id FROM users WHERE user_name = {}".format(user_choice))
                user_result = mycursor.fetchone()
                mycursor.execute("SELECT * FROM user_history WHERE user_id = {}".format(user_result[0]))
                result = mycursor.fetchall()
                for i in result:
                    print(i)
            except Exception as arg:
                print("No such user : ", arg)
        else:
            print("oops, please select a valid choice..")
    else:
        print("oops, please select a valid choice or login as customer!!")


elif user_result[3]== 'customer':
# For customers:
    choice = input("What do you want to do today : \n1)Buy a product \n2)See your shopping history \nChoice : ")

    if choice == '1':

        #first select from a list of categories
        mycursor.execute("SELECT cat_name FROM categories")
        result = mycursor.fetchall()
        print("Choose from available categories : ")
        for i in result:
            print(i[0])
        cat_choice = input("Enter name of category you want to choose : ")
        mycursor.execute("SELECT cat_id from categories where cat_name ={}".format(cat_choice))
        selected_id = mycursor.fetchone()


        mycursor.execute("SELECT product_name FROM products WHERE category = {} ".format(selected_id))
        product_results = mycursor.fetchall()

        print("These are the available products in this category : ")
        for i in product_results :
            print(i)

        prod_choice = input("What do you want to buy(Enter product name) : ")
        mycursor.execute("SELECT prod_id, product_name, price, stock, description FROM products WHERE product_name = {}".format(prod_choice))
        productt = mycursor.fetchall()
        print("Product details :", productt)

        cart_choice = input("Do you want to add this to cart? Enter [y/n]: ")
        if cart_choice == 'y' or 'Y':
            quantity = input("How many of these do you want : ")
            if quantity>productt[3]:
                print("OOPS...! Available quantity is only {}".format(productt[3]))
            else:
                # change the stock of that product in the products table
                mycursor.execute("UPDATE TABLE products SET stock = {} WHERE product_id = {}".format(((productt[3] - quantity),productt[0])))

                #Insert shopping data for the particular user into user_history table
                mycursor.execute("INSERT INTO user_history(product, user_id, quantity, total_price, date) VALUES({},{},{},{},{})".format(productt[0],user_result[0],quantity,(productt[2]*quantity), str(datetime.datetime.now())))
                db.commit()
                #print success message
                print(f"Congrats, You have bought it! {productt[1]} will reach you soon. Total price is {productt[2]*quantity}")
                print("Thankyou for shopping with us")

    elif choice == '2':
        history_result = mycursor.execute("SELECT * FROM user_history WHERE user_id = {}".format(user_result[0]))
        for i in history_result:
            print(i)
    else:
        print("Oops choice not availbale, please select from available choices!!")
