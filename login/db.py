import psycopg2
import os

def create_table():
# Connect to the database 
    conn = psycopg2.connect(database="flask_db",user=os.environ.get('USER'), 
                            password=os.environ.get('PASS'), host="localhost", port="5432") 

    # create a cursor 
    cur = conn.cursor() 

    # if you already have any table or not id doesnt matter this 
    # will create a products table for you. 
    cur.execute( 
        '''CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, name varchar(100), password varchar(128));''') 

    # commit the changes 
    conn.commit() 

    # close the cursor and connection 
    cur.close() 
    conn.close() 
    
def connect_db():
    conn = psycopg2.connect(database="flask_db", user=os.environ.get('USER'), 
                            password=os.environ.get('PASS'), host="localhost", port="5432") 
    cur = conn.cursor()
    return conn, cur

def close_db(conn, cur):
    conn.commit()
    
    cur.close()
    conn.close()