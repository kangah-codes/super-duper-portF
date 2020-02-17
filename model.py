__author__ = "Joshua Akangah"

import mysql.connector


def create_database():
	try:
		connection = mysql.connector.connect(user='akangah89')
		cursor = connection.cursor()

		cursor.execute("""
			CREATE DATABASE PORTFOLIO DEFAULT CHARACTER SET 'utf8'
		""")

	except mysql.connector.Error as err:
		return err

class Information():
	def __init__(self):
		try:
			self.connection = mysql.connector.connect(user='scott')
			self.cursor = self.connection.cursor()

			self.cursor.execute("""
				CREATE TABLE `site` ("
				" `about` text NOT NULL,"
				" `portfolio` text NOT NULL,"
				" `job_exp` text NOT NULL "
				" `category` text NOT NULL"
				" `contact` text DEFAULT '[]'"
				") ENGINE=InnoDB
			)
