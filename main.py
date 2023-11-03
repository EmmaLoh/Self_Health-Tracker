import datetime as datetime
from fastapi import FastAPI
from decimal import Decimal
from pydantic import BaseModel, SecretStr,EmailStr,Field,validator
import sqlite3
from sqlite3 import Error
from flask import Flask, request

app = FastAPI()

# Define Data Model
class User(BaseModel):
 id: int
 name: str
 birthdate:datetime.date
 height:Decimal
 password:SecretStr
 email: EmailStr

class Healthmetrics(BaseModel):
 id: int
 timestamp:datetime.datetime
 bloodpressure:Decimal= Field(ge=0.01, decimal_places=2)
 weight:Decimal= Field(ge=0.01, decimal_places=2)
 

class Emotion(BaseModel):
 id: int
 img:str
 createdAt:datetime.datetime
 
#Create a Database Connection
def create_connection():
 connection = sqlite3.connect("Self-Health.db")
 return connection

def create_table():
 connection = create_connection()
 cursor = connection.cursor()
 create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL,
        birthdate TEXT NOT NULL,
        height NUMERIC NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """
 create_healthmetrics_table_query = """
    CREATE TABLE IF NOT EXISTS healthmetrics (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        timestamp TEXT NOT NULL,
        bloodpressure NUMERIC NOT NULL,
        weight INTEGER NOT NULL
    )
    """

 create_emotions_table_query = """
    CREATE TABLE IF NOT EXISTS emotions (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        img BLOB NOT NULL,
        createdAt TEXT NOT NULL
        
    )

    """
 
 cursor.execute(create_users_table_query)
 cursor.execute(create_healthmetrics_table_query)
 cursor.execute(create_emotions_table_query)

 connection.commit()
 connection.close()

create_table()


 



# Create operation
# user
@app.post("/api/v1/users/")
def create_user_endpoint(user: User):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)", 
                    (user.id, user.name, user.birthdate, str(user.height), user.email, user.password.get_secret_value()))
        conn.commit()
    return {"message": "User created successfully"}

@app.get("/api/v1/users/{user_id}")
def read_user_endpoint(user_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE id=?", (user_id,))
        user = cur.fetchone()
        if user is None:
            return {"error": "User not found"}
        else:
            return {"id": user[0], "name": user[1], "birthdate": user[2], "height": user[3], "email": user[4], "password": user[5]}

@app.put("/api/v1/users/{user_id}")
def update_user_endpoint(user_id: int, user: User):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE Users SET name=?, birthdate=?, height=?, email=?, password=? WHERE id=?", 
                    (user.name, user.birthdate, str(user.height), user.email, user.password.get_secret_value(), user_id))
        conn.commit()
    return {"message": "User updated successfully"}

@app.delete("/api/v1/users/{user_id}")
def delete_user_endpoint(user_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE id=?", (user_id,))
        conn.commit()
    return {"message": "User deleted successfully"}

# healthmetrics
@app.post("/api/v1/healthmetrics/")
def create_healthmetric_endpoint(healthmetric: Healthmetrics):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO healthmetrics VALUES (?, ?, ?, ?)", (healthmetric.id, healthmetric.timestamp, str(healthmetric.bloodpressure), str(healthmetric.weight)))
        conn.commit()
    return {"message": "Health metric created successfully"}

@app.get("/api/v1/healthmetrics/{healthmetric_id}")
def read_healthmetric_endpoint(healthmetric_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM healthmetrics WHERE id=?", (healthmetric_id,))
        healthmetric = cur.fetchone()
        if healthmetric is None:
            return {"error": "Health metric not found"}
        else:
            return {"id": healthmetric[0], "timestamp": healthmetric[1], "bloodpressure": healthmetric[2], "weight": healthmetric[3]}

@app.put("/api/v1/healthmetrics/{healthmetric_id}")
def update_healthmetric_endpoint(healthmetric_id: int, healthmetric: Healthmetrics):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE healthmetrics SET timestamp=?, bloodpressure=?, weight=? WHERE id=?", 
                    (healthmetric.timestamp, str(healthmetric.bloodpressure), str(healthmetric.weight), healthmetric_id))
        conn.commit()
    return {"message": "Health metric updated successfully"}

@app.delete("/api/v1/healthmetrics/{healthmetric_id}")
def delete_healthmetric_endpoint(healthmetric_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM healthmetrics WHERE id=?", (healthmetric_id,))
        conn.commit()
    return {"message": "Health metric deleted successfully"}
#emotion
@app.post("/api/v1/emotions/")
def create_emotion_endpoint(emotion: Emotion):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO emotions VALUES (?, ?, ?)", (emotion.id, emotion.img, emotion.createdAt))
        conn.commit()
    return {"message": "Emotion created successfully"}

@app.get("/api/v1/emotions/{emotion_id}")
def read_emotion_endpoint(emotion_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM emotions WHERE id=?", (emotion_id,))
        emotion = cur.fetchone()
        if emotion is None:
            return {"error": "Emotion not found"}
        else:
            return {"id": emotion[0], "img": emotion[1], "createdAt": emotion[2]}

@app.put("/api/v1/emotions/{emotion_id}")
def update_emotion_endpoint(emotion_id: int, emotion: Emotion):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE emotions SET img=?, createdAt=? WHERE id=?", 
                    (emotion.img, emotion.createdAt, emotion_id))
        conn.commit()
    return {"message": "Emotion updated successfully"}

@app.delete("/api/v1/emotions/{emotion_id}")
def delete_emotion_endpoint(emotion_id: int):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM emotions WHERE id=?", (emotion_id,))
        conn.commit()
    return {"message": "Emotion deleted successfully"}
