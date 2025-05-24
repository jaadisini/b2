from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://dizaubot:dizaubot@cluster0.ise8rzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["antigcast_db"]

# Koleksi
bots_col = db["bots"]
groups_col = db["groups"]
blacklist_trigger_col = db["blacklist_triggers"]
whitelist_col = db["whitelist"]
blacklist_user_col = db["blacklist_users"]

# Fungsi helper
def get_group_status(chat_id: int) -> bool:
    g = groups_col.find_one({"chat_id": chat_id})
    return g["status"] if g else False

def set_group_status(chat_id: int, status: bool):
    groups_col.update_one({"chat_id": chat_id}, {"$set": {"status": status}}, upsert=True)

def add_whitelist(user_id: int):
    whitelist_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

def remove_whitelist(user_id: int):
    whitelist_col.delete_one({"user_id": user_id})

def list_whitelist():
    return [w["user_id"] for w in whitelist_col.find()]

def add_blacklist_user(user_id: int):
    blacklist_user_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

def remove_blacklist_user(user_id: int):
    blacklist_user_col.delete_one({"user_id": user_id})

def list_blacklist_user():
    return [u["user_id"] for u in blacklist_user_col.find()]

def add_blacklist_trigger(trigger: str):
    blacklist_trigger_col.update_one({"trigger": trigger}, {"$set": {"trigger": trigger}}, upsert=True)

def remove_blacklist_trigger(trigger: str):
    blacklist_trigger_col.delete_one({"trigger": trigger})

def list_blacklist_trigger():
    return [t["trigger"] for t in blacklist_trigger_col.find()]

def get_all_bots():
    return list(bots_col.find())

def add_bot(token: str, bot_id: int, username: str):
    bots_col.update_one(
        {"bot_id": bot_id},
        {"$set": {"bot_token": token, "bot_id": bot_id, "bot_username": username}},
        upsert=True,
    )
