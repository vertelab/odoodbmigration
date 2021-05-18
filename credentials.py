import odoorpc

source_connection = odoorpc.ODOO(input('Source host: '))
print(source_connection.db.list())
source_connection.login(input('db: '), input('login: '), input('password: '))

target_connection = odoorpc.ODOO(input('Target host: '))
print(target_connection.db.list())
target_connection.login(input('db: '), input('login: '), input('password: '))


if input('\nAre you sure you want to save credentials? [y/N] > ').lower() == 'y':
    pass
else:
    exit(0)

# Save sessions to .odoorpcrc
source_connection.save('source_kastrup')
target_connection.save('target_kastrup')