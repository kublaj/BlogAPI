import datetime
from api.data import users

from api import db

def create(username):
    user_id = users.get_user_id(username)
    expires = datetime.datetime.now() + datetime.timedelta(hours=2)
    cursor = db.cursor()
    cursor.execute('INSERT INTO Sessions (user_id, expires) VALUES (%s, %s);', (user_id, expires))
    db.commit()
    cursor.execute('SELECT LAST_INSERT_ID();')
    session_id = cursor.fetchone()[0]
    cursor.close()
    return session_id

def get(session_id):
    cursor = db.cursor()
    cursor.execute('SELECT user_id, expires, expired FROM Sessions WHERE id=%s;', (session_id,))
    session_information = {}
    result = cursor.fetchone()
    cursor.close()
    if result:
        session_information = {
            'user_id': result[0],
            'expires': result[1],
            'expired': result[2],
        }

        #if expired = False, check if the 'expires' time has passed the current time,
        #and if that's the case, change to expired = True
        if not session_information['expired']:
            current_datetime = datetime.datetime.now()
            if current_datetime > session_information['expires']:
                session_information['expired'] = True
    #There's no information about this session in the database.
    else:
        session_information = None
    return session_information
