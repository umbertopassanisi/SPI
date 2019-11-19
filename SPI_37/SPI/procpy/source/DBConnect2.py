import sys
import cx_Oracle

env = 'prod'

connectionString = 'spi/wadkn23_@'

if env == 'dev':
    connectionString+='IN1UECFD'
elif env == 'test':
    connectionString+='IN1UECFT'
elif env == 'prod':
    connectionString+='IN1UECFA'
else:
    print('unknown database')
    sys.exit()
    
def connect():
    token = cx_Oracle.Connection(connectionString)
    return token

def close(token):
    token.close()

def commit(token):
    token.commit()

def commitAndClose(token):
    token.commit()
    token.close()

