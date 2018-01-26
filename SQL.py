import sqlite3 as lite
import sys

file_name='c:\\Python26\\Scores.db'

conn = lite.connect(file_name)
cursor = conn.cursor()
cursor.execute('''DROP TABLE USERS''')
cursor.execute('''DROP TABLE USER''')
# #cursor.execute('''CREATE TABLE users (id INT PRIMARY KEY, NAME TEXT NOT NULL, DATE CHAR) ''')
# cursor.execute('''INSERT INTO users(id, name, date) VALUES(?,?,?)''',(5,'alen', '26/1/2017'))
# conn.commit()
# cursor.execute('''SELECT id,name,date FROM users''')
# all_rows = cursor.fetchall()
# for row in all_rows:
#     print row[0],
#     print row[1],
#     print row[2],
#     print
# conn.close()
#
# try:
#     conn = lite.connect(file_name)
# except lite.Error, e:
#     print "Error %s:" % file_name
#     sys.exit(1)
# try:
#     create_str='''CREATE TABLE USERS (
#             ID INT PRIMARY KEY
#             NAME TEXT NOT NULL,
#             DATE CHAR(9) NOT NULL,
#             TIME CHAR(8) NOT NULL,
#             PLAYER INT NOT NULL,
#             COMPUTER INT NOT NULL
#             )'''
#     conn.execute(create_str)
#     conn.commit()
#     print "Table created successfully"
#
# except lite.Error, e:
#     print "Error create table %s:" % file_name
#     sys.exit(1)
#
# finally:
#     if conn:
#         print "Opened database successfully"
#         cursor = conn.cursor()
#         # name = raw_input()
#         date="1/26/2017"
#         time="7:18 PM"
#         # player=int(raw_input())
#         # computer=int(raw_input())
#         # try:
#         #     cursor.execute('''INSERT INTO USERS(name, date, time, player, computer) VALUES(?,?,?,?,?)''',(name, date, time, player, computer))
#         # except lite.OperationalError:
#         #     cursor.execute('''UPDATE USERS SET player=? WHERE name = ?''',(0,name))
#         # conn.commit()
#
#         cursor.execute('''SELECT name,date,time,player,computer FROM USERS''')
#         all_rows = cursor.fetchall()
#         for row in all_rows:
#             print('{0} : {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))
#
#         name = 'amint'
#         cursor.execute('''SELECT date,time,player FROM USERS WHERE name=?''', (name,))
#         user = cursor.fetchone()
#         print user
#         user = cursor.fetchone() # retrieves the next row
#         print user
#         print
#         #Delete user
#         print 'Enter name: '
#         name = raw_input()
#         cursor.execute('''DELETE FROM USERS WHERE name = ? ''', (name,))
#         conn.commit()