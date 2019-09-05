import pymongo
from czScrapy.config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def get_from_mongo(where):
    rt = db[MONGO_TABLE].find(where)

    if rt:
        return list(rt)

    return None


def save_to_mongo(a_set):
    if db[MONGO_TABLE].insert_one(a_set):
        # print('save to mongo successfully', a_set)
        return True
    return False


def upsert_to_mongo(where, a_set):
    if db[MONGO_TABLE].update_one(where, {'$set': a_set}, upsert=True):
        # print('upsert to mongo successfully', a_set)
        return True
    return False


def check_id_mongo(a_set):
    r = db[MONGO_TABLE].find_one({'id': a_set.get('id')})
    if r:
        return True
    r = db[MONGO_TABLE].find_one({'title': a_set.get('title')})
    if r:
        return True
    return False


def check_dup_record(a_set):
    if db[MONGO_TABLE].find_one({'$and': [
        {'title': a_set.get('title')},
            {'source': {'$ne': a_set.get('source')}}]}):
        return True
    else:
        return False


def save_mongo_to_csv(tbname, filename):
    d = db[MONGO_TABLE].find_one({}, {'_id': False})
    print(d)


if __name__ == "__main__":
    # print(check_id_mongo({'id': '10247'}))
    # print(save_to_mongo({'id': 1, 'name': 'asdfa'}))
    # print(upsert_to_mongo({'id': 1}, {'name': 'aaa', 'age': 22}))
    # print(list(get_from_mongo(
    #     {'id': '26abf388-1f73-4aff-8055-8ea0bf6d5f21'})))

    # print(check_dup_record(
    #     {'title': '2018年（第四期）嘉兴市本级公共资金竞争性存放项目', 'source': '嘉兴市公共资源交'}))

    a = {'id': '10247'}
    # b = check_id_mongo(a)
    b = get_from_mongo(a)
    print(b)
