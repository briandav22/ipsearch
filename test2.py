import psycopg2
import ipaddress
import csv
class DB_handler:
    ## Handles the database connection
    def __init__(self,db_name,user,password,scrut_ip):
        self.db_name = db_name
        self.db_user = user
        self.db_password = password
        self.db_host = scrut_ip

    #method used to insert into DB

    def open_connection(self):
        self.conn = psycopg2.connect("dbname={} user={} password={} host={}".format(self.db_name,self.db_user,self.db_password,self.db_host))
        self.cur = self.conn.cursor()
        return self.cur

    def execute_query(self, query):
        self.cur.execute(query)
        try:
            record = [r[0] for r in self.cur.fetchall()]
            
        except:
            record = 'nothing_returned'
        self.conn.commit()
        return(record)

    def close_connection(self):
        self.cur.close()
        self.conn.close()
        print('disconnected from DB')


    def test_connection(self):

        try:
            self.conn = psycopg2.connect("dbname={} user={} password={} host={}".format(self.db_name,self.db_user,self.db_password,self.db_host))
            print('Connection has been Succesful')
            return True
        except psycopg2.Error as err:
            print("Error: ", err)
            return False
        
        self.conn.close()


class Host_searcher():
    def __init__(self):
        return

    def search_host(self, host_ip):
        return("select * from plixer.hosts_index where host_id = inet_a2b('{}')".format(host_ip))


    def all_hosts(self):
        return("select * from plixer.hosts_index")

    def create_table(self,table):
        return("CREATE TABLE {} (ip VARCHAR(50))".format(table))


    def copy_csv(self,table,path):
        return("copy {}(ip) from '{}' DELIMITER ',' CSV HEADER".format(table,path))


    def inner_join(self,table):
        return("SELECT inet_b2a(host_id),ip FROM plixer.hosts_index INNER JOIN {} ON ip = inet_b2a(host_id);".format(table))

    def inner_joins(self,table):
        return("SELECT inet_b2a(host_id) , inet_b2a(exporter_id),* FROM plixer.hosts_index INNER JOIN {} ON ip = inet_b2a(host_id);".format(table))
        


db_handler = DB_handler('plixer','root','admin','127.0.0.1')
path_to_csv = '/home/plixer/scrutinizer/files/ipsearch/sunburst/allips.csv'


host_search = Host_searcher()
db_handler.open_connection()


create_table_query = host_search.create_table('sunburst')



inner_join = host_search.inner_joins('sunburst')


try:
    db_handler.execute_query(create_table_query)
    copy_csv = host_search.copy_csv('sunburst',path_to_csv)
except:
    db_handler.close_connection()

    pass

db_handler.open_connection()

db_handler.execute_query(copy_csv)

results = db_handler.execute_query(inner_join)

print(results)
