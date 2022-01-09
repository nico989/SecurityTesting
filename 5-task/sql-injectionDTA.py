import sys
import os
import sqlite3

conn = None
try:
    conn = sqlite3.connect('users.db')
except Exception:
    print("Can't connect to the database")
    sys.exit(-1)

print("Welcome to this vulnerable database reader")
print("You have to login first")

print("Insert your user-id")
user_id = input() # Source1
# makeTainted("user_id")

print("Insert your password")
password = input() # Source2
# makeTainted("password")

retrieve_user = "SELECT * FROM credentials WHERE user_id = '" + user_id + "' and password = '" + password + "';"
# makeCondTainted("retrieve_user", ["user_id", "password"])

# if (isTainted("retrieve_user") && isSQLInjectionAttack(retrieve_user)):
#       sys.exit(-1)
cursor = conn.execute(retrieve_user) # Sink1
# makeCondTainted("cursor", ["retrieve_user"])

entries = cursor.fetchall()
# makeCondTainted("entries", ["cursor"])
if len(entries) > 0: 
    print("\n===Logged-in=====")
    retrieve_user = "SELECT * FROM accounts WHERE user_id = '" + user_id + "';"
    # makeCondTainted("retrieve_user", ["user_id"])
    
    # if (isTainted("retrieve_user") && isSQLInjectionAttack(retrieve_user)):
    #       sys.exit(-1)
    cursor = conn.execute(retrieve_user) # Sink2
    # makeCondTainted("cursor", ["retrieve_user"])
    entries = cursor.fetchall()
    # makeCondTainted("entries", ["cursor"])
    for entry in entries:
        # makeCondTainted("entry", ["entries"])
        user_id, first_name, last_name, phone = entry
        # makeCondTainted("user_id", "first_name", "last_name", "phone", ["entry"])
        print()
        # if (isTainted("user_id") && isXSSAttack(user_id)):
        #       sys.exit(-1)
        print("Here is {} data:".format(user_id)) # Sink3
        print("user-id=", user_id) # Sink3
        print("first_name=", first_name) 
        print("last_name=", last_name) 
        print("phone", phone) 
else:
    # makeUntainted("entries")
    print("Wrong credentials")