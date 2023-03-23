# from sqlalchemy import create_engine
# import pandas as pd

# user = "root"
# senha = "1234"
# nome_banco = "edufinance_financeiro"
# host = "localhost"

# conn = f'mysql+mysqlconnector://{user}:{senha}@{host}/{nome_banco}?auth_plugin=mysql_native_password'.format(username=user,
#                                                                         password= senha, 
#                                                                         hostname=host, 
#                                                                         database=nome_banco)
                                                                        
                                                                                                                             
                                                                                                                            
                                                                                                                       
# engine = create_engine(conn)

# price_weg = pd.DataFrame({"empresas": "Weg", "cotacao": 20.54}, index = [0])

# price_weg.to_sql('price', engine, index=False, if_exists='append')



# print(price_weg)

# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
from sqlalchemy import create_engine
import pandas as pd

# DEFINE THE DATABASE CREDENTIALS
user = "root"
password = "1234"
database = "edufinance_financeiro"
host = "localhost"
port = 3306


def get_connection():
    return create_engine(
        url=f"mysql+pymysql://{user}:{password}@{host}:{3}/{4}".format(
            user, password, host, port, database
        )
    )

def append_in_mysql():
    price_weg = pd.DataFrame({"empresas": "Petrobras", "cotacao": 19.54}, index = [0])

    price_weg.to_sql('price', engine, index=False, if_exists='append')



    print(price_weg)


try:

    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
    engine = get_connection()
    print(f"Connection to the {host} for user {user} created successfully.")
    append_in_mysql()
except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)
