import utils
import random
import string
import volcengine.viking_db as vkdb

if __name__ == '__main__':
    vikingdb_service = utils.get_vikingdb_service()
    collection = vikingdb_service.get_collection("test_coll_for_sdk")

    datas = []
    for i in range(100):
        data = vkdb.Data(
            id="1",
            fields={
                "f_id": str(i+1),
                "f_string": "doc"+str(i / 10),
                "f_int64": random.randint(1, 100),
                "f_text": "this is " + ''.join(random.choice(string.ascii_letters[:10]) for _ in range(50)),
            }
        )
        datas.append(data)
    collection.upsert_data(datas)
