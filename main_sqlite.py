from utils.sqlite_utils import SQLiteDB

def main():
    try:
        # Create the sqlite engine
        sqlite_db = SQLiteDB(database='/Users/marcosmorenoblanco/Documents/bicing/bicingv2.db')

        # Create table in db
        sqlite_db.create_table(table_name='bicing')

        # start job
        sqlite_db.start_job(url='http://api.citybik.es/v2/networks/bicing?fields=stations', 
                            start_date = '2022-03-22 10:40:00',
                            end_date= '2022-03-22 10:50:00')

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
