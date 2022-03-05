from pymongo import MongoClient
from sqlite3 import connect
import pymysql
import settings

from settings import HOST, DATABASE, USER, PASSWORD

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]

def get_or_create_user(effective_user, phone=None):
    user = db.blogers.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'user_name': effective_user.username,
            'phone': phone,
            'personal_rate': 5,
            'links':[],
            'guest_ip': []
        }
        db.blogers.insert_one(user)
    return user


def how_many_links(user_id):
    user = db.blogers.find_one({'user_id': user_id})
    quanity_of_links = len(user['links'])
    return quanity_of_links


def add_link(user_id, link, website):
    link_id = how_many_links(user_id)
    db.blogers.update_one({'user_id': user_id},
                          {'$push': 
                              {'links':{
                                    'link_id': link_id,
                                    'website': website,
                                    'short_link': link,
                                    'guests': []
                                    }
                               }
                              }
                          )
    return link_id


def guest_quanity(user_id):
    user = db.blogers.find_one({'user_id': user_id})
    total_guests = len(user['guest_ip'])
    return total_guests


def add_ip_adress(user_id, ip):
    db.blogers.update_one({'user_id': user_id},
                          {'$addToSet': {'guest_ip': ip}})

 
def get_user_rate(user_id):
    user = db.blogers.find_one({'user_id': user_id})
    rate = user['personal_rate']
    return rate


def get_date_from_sql():
    try:
        connection = pymysql.connect(
            host = HOST,
            port = 3306,
            user = USER,
            password = PASSWORD,
            database = DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )
        print('succesfully connected ...')
        print('#'*20)

        try:
            with connection.cursor() as cursor:
                create_table_query = "SELECT * FROM users" 
                cursor.execute(create_table_query)
                result = cursor.fetchall()
                return result

        finally:
            connection.close()

    except Exception as ex:
        print('Connection failed')
        print(ex)