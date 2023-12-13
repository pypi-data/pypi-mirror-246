import psycopg2 as pg

def conxao_postgrees(host, database, user, password):
    try:
        conn = pg.connect(
            host = host, 
            database = database, 
            user = user, 
            password = password
        )
    except:
        print('WARNING: Conexão não estabelecida!')
        conn = '<none>'
    return conn