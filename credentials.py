import odoorpc
import time

while(True):
    try:
        odoo = odoorpc.ODOO(input('Host name: '), port=input('Port (8069): '))
        time.sleep(1)
    except:
        print('Connect to host, FAIL')
    else:
        try:
            print(odoo.db.list())
        except:
            print('List databases, FAIL')
        try:
            odoo.login(input('Db: '), input('User: '), input('Password: '))
        except:
            print('Login failed')
        else:
            print(odoo.env)
            try:
                odoo.save(input('Save as (source/target): '))
            except:
                print('Save credentials, FAIL')
    finally:
        if input('Start over? (y/N)').lower() != 'y':
            break
        