import pyodbc
import pandas as pd
import numpy as np 
import sqlalchemy
import logging 

class clientSql():
    def __init__(
        self,
        host:str,
        user:str,
        password:str,
        db_name:str,
        MODE:str='Windows' # other option is Ubuntu
        ) -> None:
        """MODE -> Windows | Ubuntu """

        logging.debug("Init MsSQL server instance")
        #credentials
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = db_name
        # default driver
        self.__driver = 'SQL Server'
        if MODE=='Ubuntu':
            # if we use thisdriver, remind install before :)
            self.__driver= 'ODBC Driver 17 for SQL Server'
        
        self.__conn_string= 'DRIVER={'+self.__driver+'};SERVER='+self.__host+';DATABASE='+self.__database+';ENCRYPT=yes;UID='+self.__user+';PWD='+ self.__password

    def get_engine(self):
        logging.debug(f"pyodbc: {self.__conn_string}")
        return pyodbc.connect(self.__conn_string)
    
    def append_data_from_df(
        self,
        df:pd.DataFrame,
        table_name:str,
        schema:str,
        column_name_datetime:str='Fecha',
        chunk_size:int = 20
        ):

        # if hasattr(self,'sql_server') == False:
        #     self.__init_sql()
        
        logging.info(f">> Append data into {schema}.{table_name}")

        df.to_sql(
            con = self.get_pandas_engine(),
            name = table_name,
            schema = schema,
            if_exists = 'append',
            chunksize = chunk_size,
            index = False,
            method = 'multi'
            )

        logging.info(f">> Delete duplicated values {schema}.{table_name}")
        self.delete_duplicate_values_sql(
            schema=schema,
            table_name=table_name,
            column_name=column_name_datetime
        )

    def delete_duplicate_values_sql(
        self,
        schema:str,
        table_name:str,
        column_name:str or list,
        ):

        # if hasattr(self,'sql_server') == False:
        #     self.__init_sql()

        cursor = self.get_engine()

        if isinstance(column_name,str):
            query = f"""
                WITH cte AS (
                    SELECT 
                        *, 
                        ROW_NUMBER() OVER (
                            PARTITION BY [{column_name}]
                            ORDER BY [{column_name}]
                        )  [row_num]
                    FROM [{schema}].[{table_name}])
                DELETE FROM cte
                WHERE row_num>1
            """
        elif isinstance(column_name,list):
            col_string = ','.join(['['+col+']' for col in column_name])
            query = f"""
                WITH cte AS (
                    SELECT 
                        *, 
                        ROW_NUMBER() OVER (
                            PARTITION BY {col_string}
                            ORDER BY {col_string}
                        )  [row_num]
                    FROM [{schema}].[{table_name}])
                DELETE FROM cte
                WHERE row_num>1
            """
        cursor.execute(query)
        cursor.commit()
        cursor.close() 

    def get_pandas_engine(self):
        constring = f"mssql+pyodbc://{self.__user}:{self.__password}@{self.__host}/{self.__database}?driver=SQL+Server"
        logging.debug(f'get pandas connection {constring}')
        dbEngine = sqlalchemy.create_engine(constring, connect_args={'connect_timeout': 10}, echo=False)
        return dbEngine

    def read_with_pandas(self,query,**kwargs):
        return pd.read_sql(query,self.get_pandas_engine(),**kwargs)

    def execute_query(
        self,query:str
        ):
        cursor = self.get_engine()
        cursor.execute(query)
        cursor.commit()
        cursor.close() 

if __name__ == '__main__':
    pass