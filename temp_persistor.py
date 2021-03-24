import json
import os
import sys
import pika
import mysql.connector
from datetime import datetime


def connect():
    global mydb, mycursor
    print("Connecting...")
    mydb = mysql.connector.connect(
        host="db",
        user="root",
        #  passwd="R3v0lv3r!",
        database="brew_project"
    )
    mycursor = mydb.cursor()


def disconnect():
    print("Disconnecting...")
    mycursor.close()
    mydb.close()


def create_session(session_name):
    connect()
    print("Creating Session...")

    print(session_name)
    query = "INSERT INTO session (session_name) VALUES ('{}')".format(session_name)
    mycursor.execute(query)
    mydb.commit()
    query = "SELECT session_id FROM session WHERE session_name = '{}'".format(session_name)
    mycursor.execute(query)
    row = mycursor.fetchone()
    session_id = row[0]
    print("Created Session: {}, ID: {}".format(session_name, session_id))
    disconnect()
    return session_id


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.queue_declare(queue='temps')
channel.queue_bind(queue='temps', exchange='temps')

on_off = False

# for debugging
# on_off = True
# sessionID = create_session('default2')
# connect()

for method_frame, properties, body in channel.consume('temps'):
    print('This is the body {}' .format(body))
    message_type = properties.headers.get('type')
    if message_type == 'command':
        if sessionID != 0:
            on_off = body == 'true'
            if on_off:
                connect()
            else:
                disconnect()
        else:
            print("Unable to start session with out Session ID")
    elif message_type == "create":

        sessionID = create_session(json.loads(body))
    else:
        if on_off:
            tempList = json.loads(body)
            sql = "INSERT INTO temps (session_id, temp_created, temp_hlt, temp_mlt, temp_bk) " \
                  "VALUES ({}, {}, {0:.3f}, {0:.3f}, {0:.3f}) "\
                  .format(sessionID, datetime.now(), tempList[0], tempList[1], tempList[2])
            mycursor.execute(sql)
            mydb.commit()
            print("Persisted : {}".format(sessionID, datetime.now(), tempList[0], tempList[1], tempList[2]))
    channel.basic_ack(method_frame.delivery_tag)

# channel.close()
# connection.close()
