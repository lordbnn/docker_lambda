"""
This is a boilerplate pipeline 'read_write_csv'
generated using Kedro 0.18.2
"""
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pandas as pd
import psycopg2
import psycopg2.extras as extras



#s3 credentials
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

bucket_name =  "d2b-internal-assessment-bucket"
Prefix='orders_data/'
suffix = 'analytics_export/'
res = s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix=Prefix)

host = 'localhost' 
user = 'postgres'
pw = 'postgres'
db = 'postgres'
port = '5432'

table = 'public.orders'


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:

        connection = psycopg2.connect(
            database=db,
            user=user,
            password=pw,
            host=host,
            port=port
        )
        
        print("PostgreSql Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection




def read_and_convert_csv_to_dataframe(df_name,csv_path):


    obj = s3.get_object(Bucket= bucket_name, Key= Prefix+csv_path)
    df_name = pd.read_csv(obj['Body']) 
    df_name = pd.DataFrame(df_name)

    return df_name 



def load_df_to_postgres(conn, df, table):

    tuples = [list(row) for row in df.itertuples(index=False)]


    cols = ','.join(list(df.columns))
    
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)                   
    cursor = conn.cursor()
    
    try:
        extras.execute_values(cursor, query, tuples)
        #cursor.execute(query)
        conn.commit()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    except psycopg2.InterfaceError:
        pass
    print("load to postgresql successful")
    cursor.close()





def handler(event,context):
    connection = create_server_connection(host, user, pw)
    orders = read_and_convert_csv_to_dataframe('orders','orders.csv')
    load_df_to_postgres(connection, orders, table)

