__author__ = 'Joshua Akangah'

import sqlite3
import datetime
from config import *
import json
from werkzeug.security import generate_password_hash, check_password_hash


"""
json.dumps(list) --> string of lists

json.loads(str(list)) --> list of strings
"""

class SiteModel:
	def default(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()
			self.cursor.execute(f"INSERT INTO SITE (TRY) VALUES ('True')")
			self.cursor.execute(f"""INSERT INTO AUTH (USR, PWD) VALUES ('akangah', "{generate_password_hash('ilovekwame1')}")""")

		except sqlite3.OperationalError as e:
			print(e)

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def __init__(self, name="site.db"):
		self.name = name
		self.connection = sqlite3.connect(self.name)
		self.cursor = self.connection.cursor()

		try:
			self.cursor.execute(
				"""
					CREATE TABLE SITE
					(
						TRY TEXT,
						ABOUT TEXT DEFAULT 'NOT UPLOADED',
						PORTFOLIO TEXT DEFAULT '[]',
						JOB_EXP TEXT DEFAULT '[]',
						CATEGORY TEXT DEFAULT '["All"]',
						CONTACT TEXT DEFAULT '[]',
						SHS_EDUCATION TEXT DEFAULT '["NULL", "NULL", "NULL"]',
						UNI_EDUCATION TEXT DEFAULT '["NULL", "NULL", "NULL"]',
						THEME TEXT DEFAULT 'None',
						SKILLS TEXT DEFAULT '[]',
						PUBLICATIONS TEXT DEFAULT '[]'
					)
				"""
			)

			self.cursor.execute(
				"""
					CREATE TABLE AUTH
					(
						USR TEXT,
						PWD TEXT
					)
				"""
			)

		except sqlite3.OperationalError as e:
			pass

		finally:
			self.connection.commit()
			try:
				self.connection = sqlite3.connect(self.name)
				self.cursor = self.connection.cursor()
				self.cursor.execute("SELECT TRY FROM SITE")

				try:
					if self.cursor.fetchone()[0] == 'True':
						pass
				except TypeError:
					self.default()

			except sqlite3.OperationalError as e:
				return e
			if self.connection:
				self.connection.close()

	def add_about(self, text):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute(f"UPDATE SITE SET ABOUT='{text}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def add_portfolio_cat(self, text):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT CATEGORY FROM SITE")
			exist_cat = json.loads(self.cursor.fetchone()[0])
			if text in exist_cat:
				return False
			exist_cat.append(text.replace(" ", "_"))
			self.cursor.execute(f"UPDATE SITE SET CATEGORY='{json.dumps(exist_cat)}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def add_portfolio(self, name, client, cat, desc, completed, save_name):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute(
				f"""
					SELECT CATEGORY FROM SITE
				"""
			)

			exist_cat = json.loads(self.cursor.fetchone()[0])
			for i in exist_cat:
				exist_cat[exist_cat.index(i)] = i.replace("_", " ")

			self.cursor.execute("SELECT PORTFOLIO FROM SITE")

			exist_it = json.loads(self.cursor.fetchone()[0])
			if cat in exist_cat:
				exist_it.append([name, desc, cat, client, completed, save_name])
				self.cursor.execute(f"UPDATE SITE SET PORTFOLIO='{json.dumps(exist_it)}'")
				return True
			return None

		except sqlite3.OperationalError as e:
			return e

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def add_skill(self, skill, icon):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT SKILLS FROM SITE")
			exist_skill = json.loads(self.cursor.fetchone()[0])
			exist_skill.append([skill, icon])
			self.cursor.execute(f"UPDATE SITE SET SKILLS='{json.dumps(exist_skill)}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def retrieve_skill(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT SKILLS FROM SITE")

			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def add_publication(self, name, date, filename):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT PUBLICATIONS FROM SITE")
			exist_publication = json.loads(self.cursor.fetchone()[0])
			exist_publication.append([name, date, filename])
			self.cursor.execute(f"UPDATE SITE SET PUBLICATIONS='{json.dumps(exist_publication)}")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()


	def retrieve_publication(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT PUBLICATIONS FROM SITE")

			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()


	def add_job_exp(self, post, place, start, end, desc):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			items = [post, place, start, end, desc]

			self.cursor.execute("SELECT JOB_EXP FROM SITE")
			exist_job = json.loads(self.cursor.fetchone()[0])
			exist_job.append([post, place, start, end, desc])

			self.cursor.execute(f"UPDATE SITE SET JOB_EXP='{json.dumps(exist_job)}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def add_contact(self, contact):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT CONTACT FROM SITE")
			exist_contact = json.loads(self.cursor.fetchone()[0])

			exist_contact.append(contact)

			self.cursor.execute(f"UPDATE SITE SET CONTACT='{json.dumps(exist_contact)}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def retrieve_about(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT ABOUT FROM SITE")

			return self.cursor.fetchone()[0]

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			if self.connection:
				self.connection.close()

	def retrieve_portfolio_cat(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT CATEGORY FROM SITE")
			items = []

			for _ in json.loads(self.cursor.fetchall()[0][0]):
				items.append(_.replace("_", " "))
			return items

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def retrieve_project(self, name):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT PORTFOLIO FROM SITE")
			items = []

			for _ in json.loads(self.cursor.fetchall()[0][0]):
				if name == _[0].replace(" ", "_"):
					items.append(_)
			return items

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def retrieve_portfolio(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT PORTFOLIO FROM SITE")

			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()


	def retrieve_job_exp(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT JOB_EXP FROM SITE")
			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def retrieve_contact(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute("SELECT CONTACT FROM SITE")

			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def add_education(self, start, end, course, typeof):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			if typeof == 'shs':
				self.cursor.execute(f"UPDATE SITE SET SHS_EDUCATION='{json.dumps([start, end, course])}'")

			else:
				self.cursor.execute(f"UPDATE SITE SET UNI_EDUCATION='{json.dumps([start, end, course])}'")


		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def retrieve_education(self, typeof):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			if typeof == 'shs':
				self.cursor.execute("SELECT SHS_EDUCATION FROM SITE")
				return json.loads(self.cursor.fetchone()[0])
			self.cursor.execute("SELECT UNI_EDUCATION FROM SITE")
			return json.loads(self.cursor.fetchone()[0])

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()

	def change_theme(self, val):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute(f"UPDATE SITE SET THEME='{val}'")

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			self.connection.commit()
			if self.connection:
				self.connection.close()

	def check_theme(self):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()

			self.cursor.execute(f"SELECT THEME FROM SITE")
			return self.cursor.fetchall()[0]

		except sqlite3.OperationalError as e:
			return e

		else:
			return True

		finally:
			if self.connection:
				self.connection.close()

	def validate_login(self, usr, pwd):
		try:
			self.connection = sqlite3.connect(self.name)
			self.cursor = self.connection.cursor()
			items = []

			self.cursor.execute(f"SELECT * FROM AUTH")
			items.append(self.cursor.fetchone())
			if usr == items[0][0] and check_password_hash(items[0][1], pwd):
				return True
			return False

		except sqlite3.OperationalError as e:
			return e

		finally:
			if self.connection:
				self.connection.close()


	def __repr__(self):
		return f"""
		Site Database Model\n
		About {self.retrieve_about}\n
		Portfolio Categories {self.retrieve_portfolio_cat}\n
		Work {self.retrieve_portfolio}\n

		"""
# print(db.add_about("My name is Joshua Akangah. I love girls very much. I am single tho..."))
#print(db.add_portfolio_cat("Mobile App Development"))
#print(db.add_job_exp("STEM Volunteer", "ELiTE", "Jul 15", "May 19", "Worked on muyltiple projects and did this and that"))

#print(db.add_contact("0550120124"))

# print(db.add_educ('2019', '2344', 'Science', 'uni'))
# print(db.retrieve_educ())
#a = SiteModel()
# print(a.change_theme('on'))

class Admin:
	def __init__(self, usr, pwd, validated):
		self.username = usr
		self.pwd = pwd
		if validated:
			self.is_authenticated = True
			self.is_active = True
		else:
			self.is_authenticated = False
			self.is_active = False

	def get_id(self):
		return str(self.username)

def retrieve_auth():
	try:
		connection = sqlite3.connect('site.db')
		cursor = connection.cursor()

		cursor.execute("SELECT USR, PWD FROM AUTH")

		return cursor.fetchall()

	except sqlite3.OperationalError as e:
		return e

	finally:
		if connection:
			connection.close()
