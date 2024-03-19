from numpy import number
from pymongo.mongo_client import MongoClient
from config import MongoDBConfig
from uuid import uuid4
import time
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from app.firebase.firebase import FireBase
from sanic.response import json

assetsCate = ["Tiền mặt", "Tiền gửi ngân hàng", "Cho vay", "Đầu tư", "Bất động sản"]

debtCate = ["Tiền mặt", "Trả góp", "Thế chấp", "Thấu chi"]

day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
def get_previous_day(data):
    if data["day"] > 1:
        return {
            "day": data["day"] - 1,
            "month": data["month"],
            "year": data["year"]
        }
    else:
        if data["month"] > 1: 
            return {
                "day": day_in_month(data["month"] - 1),
                "month": data["month"] - 1,
                "year": data["year"]
            }
        else:
            return {
                "day": 31,
                "month": 12,
                "year": data["year"] - 1
            }


class MongoDB:
    def __init__(self, connection_url=None):
        uri = "mongodb+srv://doanthang2001:05092001Thang@fintrack01.bdf1t8u.mongodb.net"
        # Create a new client and connect to the server
        self.client = MongoClient(uri)

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        # Send a ping to confirm a successful connection
        self.db = self.client[MongoDBConfig.DATABASE]
        self.user_collection = self.db[MongoDBConfig.USER_COLLECTION]
        self.spending_collection = self.db[MongoDBConfig.SPENDING_COLLECTION]
        self.comment_collection = self.db[MongoDBConfig.COMMENT_COLLECTION]
        self.assets_collection = self.db[MongoDBConfig.ASSETS_COLLECTION]
        self.transactions_collection = self.db[MongoDBConfig.TRANSACTIONS_COLLECTION]
        # self.fb = FireBase()
        
    def create_user(self, username, password, name, birthday, job, university):
        data = self.user_collection.find_one({"username": username})
        if(data): 
            return "existed"
        else:
            uuid = str(uuid4())
            self.user_collection.insert_one({
                '_id': uuid,
                'username': username,
                'password': password,
                'name': name,
                'birthday': birthday,
                'job': job,
                'university': university,
            })
            return json({"status": "success", "data": self.user_collection.find_one({"username": username})})
    
    def get_user(self, username):
        data = self.user_collection.find_one({"username": username})
        return data
    
    def create_feedback(self, img_url, username, point, data, comment):
        uuid = str(uuid4())
        self.comment_collection.insert_one({
            '_id': uuid,
            'img_url': img_url,
            'username': username,
            'point': point,
            'data': data,
            'comment': comment
        })
        return "success"
    
# comment

    def count_comments(self):
        return self.comment_collection.count_documents({})
    
    def average_points_all_comments(self):
        try:
            cursor = self.comment_collection.find({})
            total_point = 0
            count = 0
            for document in cursor:
                total_point += int(document['point'])
                count += 1

            return total_point / count if count > 0 else 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return "false"  # If there's an error, return "false" (as per your code)


# assets
        
    def get_user_assets(self, username):
        data = self.assets_collection.find_one({"username": username})
        return data
    
    def get_user_assets_specific(self, username, day, month, year):
        try: 
            data = self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                return data
            else: 
                uuid = str(uuid4())
                previous_day = get_previous_day({"day": day, "month": month, "year": year})
                previous_day_data = self.assets_collection.find_one({"username": username, "day": previous_day["day"], 
                                                                     "month": previous_day["month"], "year": previous_day["year"]})
                if previous_day_data:
                    self.assets_collection.insert_one({
                        '_id': uuid,
                        'username': username,
                        "day": day, 
                        "month": month, 
                        "year": year,
                        "assets": previous_day_data["assets"],
                        "debt": previous_day_data["debt"],
                        "history": []
                    })

                    return self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
                    
                else: 
                    self.assets_collection.insert_one({
                        '_id': uuid,
                        'username': username,
                        "day": day, 
                        "month": month, 
                        "year": year,
                        "assets": [0, 0, 0, 0, 0],
                        "debt": [0, 0, 0, 0],
                        "history": []
                    })
                    return self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
                
                
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
        
    def get_user_assets_specific_month_year(self, username, month, year):
        try: 
            data = self.assets_collection.find({"username": username, "month": month, "year": year})
            if data:
                res = []
                for docs in data:
                    res.append(docs)
                return res
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
    
    def add_assets_transaction(self, username, day, month, year, name, category1, category2, money, hour, minute, second, _type):
        try: 
            data = self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                if(_type == 0) :
                    if category1 == "Tài sản":
                        data["assets"][assetsCate.index(category2)] += money
                    else:
                        data["debt"][assetsCate.index(category2)] += money
                else:
                    if category1 == "Tài sản":
                        data["assets"][assetsCate.index(category2)] -= money
                    else:
                        data["debt"][assetsCate.index(category2)] -= money
                
                print(data)

                data["history"].append({
                    "name": name,
                    "category1": category1,
                    "category2": category2,
                    "money": money,
                    "hour": hour,
                    "minute": minute,
                    "second": second,
                    "type": _type,

                })
                self.assets_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "assets": data["assets"], "debt": data["debt"], "history": data["history"] }})
            else: 
                assetsData = [0, 0, 0, 0, 0]
                debtData = [0, 0, 0, 0, 0]

                if(_type == 0) :
                    if category1 == "Tài sản":
                        assetsData[assetsCate.index(category2)] += money
                    else:
                        assetsData[debtCate.index(category2)] += money
                else:
                    if category1 == "Tài sản":
                        debtData[assetsCate.index(category2)] -= money
                    else:
                        debtData[debtCate.index(category2)] -= money

                uuid = str(uuid4())
                self.assets_collection.insert_one({
                    '_id': uuid,
                    'username': username,
                    "day": day, 
                    "month": month, 
                    "year": year,
                    "assets": assetsData,
                    "debt": debtData,
                    "history": [{
                        "name": name,
                        "category1": category1,
                        "category2": category2,
                        "money": money,
                        "hour": hour,
                        "minute": minute,
                        "second": second,
                        "type": _type,
                    }]
                }) 
            return self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
    
    def delete_assets_transaction (self, username, day, month, year, 
                            name, money, hour, minute, second):
        try: 
            data = self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                for i in range(len(data["history"]) - 1, -1, -1):
                    if (data["history"][i]["name"] == name and data["history"][i]["money"] == money and 
                    data["history"][i]["hour"] == hour and data["history"][i]["minute"] == minute and
                    data["history"][i]["second"] == second):
                        if(data["history"][i]["type"] == 0) :
                            if data["history"][i]["category1"] == "Tài sản":
                                data["assets"][assetsCate.index(data["history"][i]["category2"])] -= data["history"][i]["money"]
                            else:
                                data["debt"][debtCate.index(data["history"][i]["category2"])] -= data["history"][i]["money"]
                        else:
                            if data["history"][i]["category1"] == "Tài sản":
                                data["assets"][assetsCate.index(data["history"][i]["category2"])] += data["history"][i]["money"]
                            else:
                                data["debt"][debtCate.index(data["history"][i]["category2"])] += data["history"][i]["money"] 
                        data["history"].pop(i)

                self.assets_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "history": data["history"], "assets": data["assets"], "debt": data["debt"] }})
            else: 
                return None
            return self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
        
    def update_user_assets(self, username, day, month, year, assets, debt):
        try : 
            data = self.assets_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                self.assets_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "assets": assets, "debt": debt }})
            else: 
                uuid = str(uuid4())
                self.assets_collection.insert_one({
                    '_id': uuid,
                    'username': username,
                    "day": day, 
                    "month": month, 
                    "year": year,
                    "assets": assets,
                    "debt": debt,
                })
            return "success"    
        except Exception as e:
            print(f"An error occurred: {e}")
            return "false"  # If there's an error, return "false" (as per your code)
        
# transactions
    def get_user_transactions(self, username):
        data = self.transactions_collection.find_one({"username": username})
        return data
    
    def get_user_transactions_specific(self, username, day, month, year):
        try: 
            data = self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                return data
            else:
                uuid = str(uuid4())
                self.transactions_collection.insert_one({
                    '_id': uuid,
                    'username': username,
                    "day": day, 
                    "month": month, 
                    "year": year,
                    "history": []
                })
                return self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
    
    def get_user_transactions_specific_month_year(self, username, month, year):
        try: 
            data = self.transactions_collection.find({"username": username, "month": month, "year": year})
            if data:
                res = []
                for docs in data:
                    res.append(docs)
                return res
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)

    def add_transaction(self, username, day, month, year, name, category1, category2, money, hour, minute, second, _type, moneytype):
        try: 
            data = self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            if data:
                data["history"].append({
                    "name": name,
                    "category1": category1,
                    "category2": category2,
                    "money": money,
                    "hour": hour,
                    "minute": minute,
                    "second": second,
                    "type": _type,
                    "moneytype": moneytype
                })
                self.transactions_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "history": data["history"] }})
            else: 
                uuid = str(uuid4())
                self.transactions_collection.insert_one({
                    '_id': uuid,
                    'username': username,
                    "day": day, 
                    "month": month, 
                    "year": year,
                    "history": [{
                        "name": name,
                        "category1": category1,
                        "category2": category2,
                        "money": money,
                        "hour": hour,
                        "minute": minute,
                        "second": second,
                        "type": _type, 
                        "moneytype": moneytype
                    }]
                }) 
            return self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
        
    
    def update_transaction (self, username, day, month, year, 
                            name, category1, category2, money, 
                            hour, minute, second, _type, moneytype,
                            new_name, new_category1, new_category2, new_money,
                            new_hour, new_minute, new_second, new_type, new_moneytype):
        try: 
            data = self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            print(data)
            if data:
                for i in range(0, len(data["history"])):
                    if (data["history"][i]["name"] == name and data["history"][i]["category1"] == category1 and
                    data["history"][i]["category2"] == category2 and data["history"][i]["money"] == money and 
                    data["history"][i]["hour"] == hour and data["history"][i]["minute"] == minute and
                    data["history"][i]["second"] == second and data["history"][i]["type"] == _type and 
                    data["history"][i]["moneytype"] == moneytype):
                        
                        data["history"][i] = {
                            "name": new_name,
                            "category1": new_category1,
                            "category2": new_category2,
                            "money": new_money,
                            "hour": new_hour,
                            "minute": new_minute,
                            "second": new_second,
                            "type": new_type,
                            "moneytype": new_moneytype
                        }
                self.transactions_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "history": data["history"] }})
            else: 
                return None
            return self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
        
    def delete_transaction (self, username, day, month, year, 
                            name, category1, category2, money, 
                            hour, minute, second, _type, moneytype):
        try: 
            data = self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})
            print(data)
            if data:
                for i in range(len(data["history"]) - 1, -1, -1):
                    if (data["history"][i]["name"] == name and data["history"][i]["category1"] == category1 and
                    data["history"][i]["category2"] == category2 and data["history"][i]["money"] == money and 
                    data["history"][i]["hour"] == hour and data["history"][i]["minute"] == minute and
                    data["history"][i]["second"] == second and data["history"][i]["type"] == _type and
                    data["history"][i]["moneytype"] == moneytype):
                        
                        data["history"].pop(i)

                self.transactions_collection.update_one({"username": username, "day": day, "month": month, "year": year}
                                                  , {"$set": { "history": data["history"] }})
            else: 
                return None
            return self.transactions_collection.find_one({"username": username, "day": day, "month": month, "year": year})

        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # If there's an error, return "false" (as per your code)
        