
class DataBaseExecuter(): 
    def __init__(self, host_driver_connstr:str, database_system:str, user_collection:str, password:str, dbtype:str):
        self.host_driver_connstr = host_driver_connstr
        self.database_system = database_system
        self.user_collection = user_collection
        self.password = password
        self.dbtype = dbtype
        
    def __openconn(self):
        if self.dbtype == 'mysql':
            try:
                import mysql.connector
                self.conn = mysql.connector.connect(
                    host=self.host_driver_connstr,
                    database=self.database_system,
                    user=self.user_collection,
                    password=self.password,
                )
            except Exception as e:
                raise Exception(f"Errore di connessione: {e}")
        elif self.dbtype == 'db2':
            try:
                    import pyodbc
                    self.conn = pyodbc.connect(
                    driver=self.host_driver_connstr,  #'{iSeries Access ODBC Driver}',
                    system=self.database_system,
                    uid=self.user_collection,
                    pwd=self.password,
                )
            except Exception as e:
                raise Exception(f"Errore di connessione: {e}")
        elif self.dbtype == 'mongo':
            try:
                import pymongo
                client = pymongo.MongoClient(self.host_driver_connstr)
                db = client[self.database_system]
                self.conn = db[self.user_collection]
        
            except Exception as e:
                raise Exception(f"Errore di connessione: {e}")
        else:
            raise Exception("Il tipo di DB non è supportato da questa classe.")
        
    def __closeconn(self):
        self.conn.close()    

    def selectbyqry(self,qry):
        import pandas as pd
        self.__openconn()
        if self.dbtype == 'mongo':
            download_data = self.conn.find(qry)
            list_data = list(download_data)
            data = pd.DataFrame(list_data)
        else:
            data =  pd.read_sql(qry, self.conn)
            self.__closeconn()
        return data

    def executeqry(self,qry):
        self.__openconn()
        if self.dbtype == 'mongo':
            try:
                self.conn.insert_one(qry)
            except Exception as e:
                raise Exception(e)
        else:
            self.cursor = self.conn.cursor()
            try:
                self.cursor.execute(qry)
                self.conn.commit()
                self.__closeconn()
            except Exception as e:
                self.conn.rollback()
                self.__closeconn()
                raise Exception(e)
        
    def dfload(self, data, table_name: str, column_lst: list):
        column_str = ",".join(column_lst)
        load_str = f""" INSERT INTO {table_name} ({column_str}) values """
        for i,row in data.iterrows():
            string = "('" + "','".join(row) + "')"
            try:
                self.executeqry(load_str + string)
            except Exception as e:
                raise Exception(f"""Errore nel caricamento della riga {i}, {e}""")


    def dblog(self, procedura, log):
        import datetime as dt
        time_now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qry = f"""INSERT INTO log_procedure (procedura, dtm, messaggio) values ('{procedura}','{time_now}', '{log}')"""
        
        self.__openconn()
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(qry)
            self.conn.commit()
            self.__closeconn()
        except Exception as e:
            self.conn.rollback()
            self.__closeconn()
            raise Exception(e)

    def update_mg(self, filter, set):
        self.__openconn()
        try:
            self.conn.replace_one(filter, set, upsert=True)
        except Exception as e:
            raise Exception(e)