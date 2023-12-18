from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd


def df_iud(stmt, df_name: str, df_data):
    try:
        engine = create_engine('sqlite://')
        df_data.to_sql(df_name, engine)
        with engine.connect() as conn:
            result = conn.execute(text(stmt))
            conn.commit()
        df_data = pd.read_sql(
            f'select * from {df_name}', engine).drop(['index'], axis=1)
        with engine.connect() as conn:
            conn.execute(text(f'drop table {df_name}'))
            conn.commit()
        return df_data
    except:
        return 'error ...'


def df_select(stmt, df_name: str, df_data):
    try:
        engine = create_engine('sqlite://')
        df_data.to_sql(df_name, engine)
        with engine.connect() as conn:
            result = conn.execute(text(stmt))
        my_list = [item for item in result]
        try:
            df_data = pd.DataFrame(my_list).drop(['index'], axis=1)
        except:
            df_data = pd.DataFrame(my_list)
        with engine.connect() as conn:
            conn.execute(text(f'drop table {df_name}'))
            conn.commit()
        return df_data
    except:
        return 'error ...'
