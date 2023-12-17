from flask import Flask, render_template, request, redirect, url_for 
import psycopg2 

app = Flask(__name__) 

# Connect to the database 
conn = psycopg2.connect(database="flask_db", user="casper", 
						password="", host="localhost", port="5432") 

# create a cursor 
cur = conn.cursor() 

# if you already have any table or not id doesnt matter this 
# will create a products table for you. 
cur.execute( 
	'''CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY, name varchar(100), price float);''') 

# commit the changes 
conn.commit() 

# close the cursor and connection 
cur.close() 
conn.close() 


@app.route('/') 
def index(): 
	# Connect to the database 
	conn = psycopg2.connect(database="flask_db", 
							user="casper", 
							password="", 
							host="localhost", port="5432") 

	# create a cursor 
	cur = conn.cursor() 

	# Select all products from the table 
	cur.execute('''SELECT * FROM products''') 

	# Fetch the data 
	data = cur.fetchall()

	# close the cursor and connection 
	cur.close() 
	conn.close() 

	return data


@app.route('/create', methods=['POST']) 
def create(): 
    req = request.get_json()
    conn = psycopg2.connect(database="flask_db", user="casper", password="", host="localhost", port="5432") 

    cur = conn.cursor() 
    
	# Get the data from the request 
    name = req['name'] 
    price = req['price'] 

	# Insert the data into the table 
    cur.execute('''INSERT INTO products (name, price) VALUES (%s, %s)''', (name, price)) 

    
	# commit the changes 
    conn.commit() 

	# close the cursor and connection 
    cur.close() 
    conn.close() 

    return {
        "name": name,
        "price": price
    }


@app.route('/update', methods=['PUT']) 
def update(): 
    req=request.get_json()
    conn = psycopg2.connect(database="flask_db", 
							user="casper", 
							password="", 
							host="localhost", port="5432") 

    cur = conn.cursor() 
    """
    Way-1:
        to update the price of a product
        eg: 
        {
            "name": "Apple",
            "price": 2.99
        }
    
    Way-2:
        to update the name of a product
        eg: 
        {
            "oldName": "Apple",
            "newName": "Apple2"
        }
    
    Way-3:
        to update the name and price of a product
        eg: 
        {
            "oldName": "Apple",
            "newName": "Apple2",
            "price": 2.99
        }
    """
    try:
        name = req['name'] 
        price = req['price'] 
        
        cur.execute('''UPDATE products SET price=%s WHERE name=%s''', (price, name))
        conn.commit() 
        return {
            "name": name,
            "price": price
        }
        
    except:
        oldName = req['oldName']
        newName = req['newName']
        try:
            price = req['price']
            cur.execute('''UPDATE products SET name=%s, price=%s WHERE name=%s''', (newName, price, oldName))
            conn.commit() 
            return {
                "name": newName,
                "price": price
            }
        except:
            cur.execute('''UPDATE products SET name=%s WHERE name=%s''', (newName, oldName))
            conn.commit() 
            return {
                "name": newName
            }
	
    


@app.route('/delete', methods=['DELETE']) 
def delete(): 
    req = request.get_json()
    conn = psycopg2.connect (database="flask_db", user="casper", host="localhost", port="5432") 
    cur = conn.cursor() 

	# Get the data from the form 
    name = req['name'] 

	# Delete the data from the table 
    cur.execute('''DELETE FROM products WHERE name=%s''', (name,)) 

	# commit the changes 
    conn.commit() 

	# close the cursor and connection 
    cur.close() 
    conn.close() 

    return {
        "deleted name": name
    }


if __name__ == '__main__': 
	app.run(debug=True) 
