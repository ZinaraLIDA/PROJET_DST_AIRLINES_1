from mysql.connector import connect

class SqlConnect:

    def __init__(self, c_mysql):
        self.c_mysql = c_mysql
        try:
            self.conn = connect(host=c_mysql["host"], port=c_mysql["port"], username=c_mysql["username"], password=c_mysql["password"], database=c_mysql["db_name"])
        except:
            self.conn = connect(host=c_mysql["host"], port=c_mysql["port"], username=c_mysql["username"], password=c_mysql["password"])

    def close(self):
        self.conn.close()

