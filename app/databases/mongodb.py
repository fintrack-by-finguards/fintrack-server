from numpy import number
from pymongo.mongo_client import MongoClient
from config import MongoDBConfig
from uuid import uuid4
import time
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from app.firebase.firebase import FireBase


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
        # self.fb = FireBase()

    # def create_user(self):
        
    def create_user(self, username, password, name):
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
            })
            return "success"
    
    def get_user(self, username):
        data = self.user_collection.find_one({"username": username})
        return data
    

    # def find_nonce_link(self, link):
    #     nonce = self.links_collection.count_documents({
    #         "url": link
    #     })
    #     return nonce

    # def get_all_customed_link(self, link):
    #     data = self.links_collection.find(
    #         {'url': link},  {'link': 1, 'nonce': 1, 'views': 1, '_id': 0})
    #     return data

    # def get_origin_url(self, link):
    #     data = self.links_collection.find_one(
    #         {'link': link}, {'url': 1, 'nonce': 1, 'views': 1, '_id': 0})
    #     self.links_collection.update_one(
    #         {'link': link}, {"$set": {"views": data["views"] + 1}})
    #     del data['views']
    #     return data

    # def views_count(self):
    #     res = {}
    #     data = self.links_collection.distinct("url")
    #     current_time_stamp = int(time.time())
    #     for url in data:
    #         views = list(self.links_collection.aggregate([{"$match": {"url": url}}, {
    #                      "$group": {"_id": "$url", "totalViews": {"$sum": "$views"}}}]))
    #         res[url] = views[0]['totalViews']
    #     for key, value in res.items():
    #         number_of_documents = self.urls_collection.count_documents({
    #                                                                    "url": key})
    #         if number_of_documents == 0:
    #             n_links = self.links_collection.count_documents({"url": key})
    #             uuid = str(uuid4())
    #             self.urls_collection.insert_one({
    #                 '_id': uuid,
    #                 'url': key,
    #                 'n_links': n_links,
    #                 'view_logs': {
    #                     str(current_time_stamp): value,
    #                 },
    #                 'last_update_at': current_time_stamp,
    #             })
    #         else:
    #             self.urls_collection.update_one({"url": key}, {"$set": {"view_logs.{}".format(
    #                 str(current_time_stamp)): value, "last_update_at": current_time_stamp}})
    #         _id = self.urls_collection.find_one({"url": key}, {'_id': 1})
    #         self.insert_image(key, str(_id['_id']))

    # def get_views_log(self, url):
    #     data = self.urls_collection.find_one(
    #         {"url": url}, {'view_logs': 1, '_id': 0})
    #     return data

    # def insert_image(self, url, _id):
    #     data = self.get_views_log(url)

    #     X = [datetime.fromtimestamp(int(view_log[0]))
    #          for view_log in data['view_logs'].items()]
    #     Y = [view_log[1] for view_log in data['view_logs'].items()]

    #     color = "red"
    #     if Y[0] <= Y[-1]:
    #         color = "green"

    #     plt.plot_date(X, Y, linestyle='solid', color=color)
    #     plt.gcf().autofmt_xdate()
    #     date_format = mpl_dates.DateFormatter('%Y-%m-%d %H:%M:%S')
    #     plt.gca().xaxis.set_major_formatter(date_format)
    #     plt.title("View logs of {}".format(url))
    #     plt.xlabel("Date")
    #     plt.ylabel("Views")
    #     plt.tight_layout()
    #     plt.savefig('app/databases/images/{}.png'.format(_id))
    #     plt.clf()

    #     public_url = self.fb.add_image('{}.png'.format(_id))

    #     self.view_logs_collection.update_one({"url": url}, {"$set": {"link": public_url}}, upsert=True)