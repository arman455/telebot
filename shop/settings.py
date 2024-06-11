import pymongo
data = {
    "bot" : {
        "tg_token" : "6184907566:AAFYnK8CaR6vsQMdgkCO6Ou80yq4WkWsYsg",
        "bot_name" : "Scripy Techno Shop",
        "phone_number" : "+380683585475",
        "email" : "scripytechno@gmail.com",
        "address" : "Вулиця Квітнева 45Б" 
    },

    "db" : {
        "mongo_token" : "mongodb+srv://Logika_ivan_petrov:IbPS6hMS8sZGg50s@logikacluster.bdorooz.mongodb.net/test",
        "mongo_db" : "Scripy_Techno_Shop",
        "mongo_col_users" : "Users",
        "mongo_col_products" : "Products",
    }

}

my_client = pymongo.MongoClient(data["db"]["mongo_token"])
my_db = my_client[data["db"]["mongo_db"]]
my_col_u = my_db[data["db"]["mongo_col_users"]]
my_col_p = my_db[data["db"]["mongo_col_products"]]


oleg_user = my_col_u.find_one({
    "tg_id":441550313
})

oleg_user["basket"].update({
    '2': 3
})

my_col_u.update_one({"tg_id":441550313}, {"$set" : oleg_user})