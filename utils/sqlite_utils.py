import sqlite3
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd

class SQLiteDB:
    def __init__(self, database):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name):
        print(f"Creating table")
        self.cursor.execute('''create table ''' + table_name + '''
        (id text,
        name text,
        empty_slots integer, 
        ebikes integer,
        normal_bikes integer,
        free_bikes integer,
        latitude integer,
        longitude integer,
        timestamp text
        )''')

    def fetch_data(self, url):
        r = requests.get(url)
        data = r.json()
        # cursor = connection.cursor()
        for station in data['network']['stations']:
            self.cursor.execute("Insert into bicing values (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (station['id'], station['name'], station['empty_slots'], station['extra']['ebikes'], station['extra']['normal_bikes'],
            station['free_bikes'], station['latitude'], station['longitude'], station['timestamp']))
            self.conn.commit()

    def start_job(self, url, start_date, end_date):
        self.sched = BlockingScheduler()
        self.sched.add_job(self.fetch_data, 'interval', minutes=5, start_date=start_date, end_date=end_date, args=[url])
        self.sched.start()

    def execute_query(self, query):
        return self.conn.execute(query)

    def retrieve_as_df(self, query):
        exec = self.execute_query(query)
        cols = [column[0] for column in exec.description]
        return pd.DataFrame.from_records(data = exec.fetchall(), columns = cols)
