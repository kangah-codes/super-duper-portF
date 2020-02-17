from flask import Flask, render_template, url_for, request, redirect, flash
from flask_session import Session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import *
from config import *
import os

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = '/home/akangah89/mysite/static/img/uploads'
app.secret_key = 'cobby'

db = SiteModel()

session = gen_session()

login = LoginManager(app)
login.init_app(app)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'lmao'


@login.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return Admin(retrieve_auth()[0][0], retrieve_auth()[0][1], True)

@app.login_manager.unauthorized_handler
def unauth_handler():
	return redirect('/portal')


@app.route('/', methods=['GET', 'POST'])
def index():
	data = {
		"about": db.retrieve_about().split('.'),
		"category": db.retrieve_portfolio_cat(),
		"experience": db.retrieve_job_exp(),
		"contact": db.retrieve_contact(),
		"portfolio": db.retrieve_portfolio(),
		"shs": db.retrieve_education('shs'),
		"uni": db.retrieve_education('uni'),
		"theme": db.check_theme(),
		"skills": db.retrieve_skill(),
		"session": session

	}

	return render_template('index.html', **data)

@app.route('/portal', methods=['GET', 'POST'])
def portal():
	global session
	session = gen_session()
	data = {
		"session": session,

	}
	if request.method == 'POST':
		if db.validate_login(request.form.get('usr'), request.form.get('pwd')):
			user = Admin(request.form.get('usr'), request.form.get('pwd'), db.validate_login(request.form.get('usr'), request.form.get('pwd')))
			user.is_authenticated = True
			login_user(user, remember=True)
			return redirect(f'/home/{session}')
		data['msg'] = 'error'
		return render_template('login.html', **data)

	return render_template('login.html', **data)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/portal')

@app.route('/home/<session>', methods=['GET', 'POST'])
@login_required
def home(session):
	data = {
		"about": db.retrieve_about().split('.'),
		"category": db.retrieve_portfolio_cat(),
		"experience": db.retrieve_job_exp(),
		"contact": db.retrieve_contact(),
		"portfolio": db.retrieve_portfolio(),
		"session": session,
		"theme": db.check_theme()
	}

	if request.method == 'POST':
		state = request.form.get('check')
		print(state)
		db.change_theme(state)

	return render_template('home.html', **data)

@app.route('/portal/about/<session>', methods=['GET', 'POST'])
@login_required
def about(session):
	data = {
		"session": session,
	}

	if request.method == 'POST':
		about = request.form.get('about')
		if db.add_about(about):
			data['msg'] = 'success'
			return render_template('about.html', **data)
		data['msg'] = 'error'
		return render_template('about.html', **data)
	return render_template('about.html', **data)

@app.route('/portal/add_portfolio/<session>', methods=['GET', 'POST'])
@login_required
def add_portfolio(session):
	data = {
		"session": session,
		"exist": db.retrieve_portfolio_cat(),
	}

	if request.method == 'POST':
		name = request.form.get('name')
		completed = request.form.get('completed')
		client = request.form.get('client')
		category = request.form.get('category')
		desc = request.form.get('desc')
		img = request.files['img']
		save_name = gen_upload_id()

		if db.add_portfolio(name, client, category.replace("_"," "), desc, completed, save_name):
			img.save(os.path.join(app.config['IMAGE_UPLOADS'], f'{save_name}.png'))
			data['msg'] = 'success'
			return render_template('add_portfolio.html', **data)
		data['msg'] = 'error'
		return render_template('add_portfolio.html', **data)

	return render_template('add_portfolio.html', **data)

@app.route('/portal/add_experience/<session>', methods=['GET', 'POST'])
@login_required
def add_experience(session):
	data = {
		"session": session,
	}

	if request.method == 'POST':
		post = request.form.get('post')
		company = request.form.get('company')
		start = request.form.get('start')
		end = request.form.get('end')
		desc = request.form.get('desc')

		if db.add_job_exp(post, company, start, end, desc):
			data['msg'] = 'success'
			return render_template('add_experience.html', **data)
		data['msg'] = 'error'
		return render_template('add_experience.html', **data)

	return render_template('add_experience.html', **data)

@app.route('/portal/add_contact/<session>', methods=['GET', 'POST'])
@login_required
def add_contact(session):
	data = {
		"session": session,
	}

	if request.method == 'POST':
		contact = request.form.get('contact')

		if db.add_contact(contact):
			data['msg'] = 'success'
			return render_template('add_contact.html', **data)
		data['msg'] = 'error'
		return render_template('add_contact.html', **data)

	return render_template('add_contact.html', **data)

@app.route('/portal/add_education/<session>', methods=['GET', 'POST'])
@login_required
def add_education(session):
	data = {
		"session": session,
	}

	if request.method == 'POST':
		start = request.form.get('start')
		end = request.form.get('end')
		course = request.form.get('course')

		if request.form.get('level') == 'SHS':
			if db.add_education(start, end, course, 'shs'):
				data['msg'] = 'success'
				return render_template('add_education.html', **data)
			data['msg'] = 'error'
			return render_template('add_education.html', **data)
		if db.add_education(start, end, course, 'uni'):
			data['msg'] = 'success'
			return render_template('add_education.html', **data)
		data['msg'] = 'error'
		return render_template('add_education.html', **data)



	return render_template('add_education.html', **data)

@app.route('/portfolio/<project>/<session>')
@login_required
def project(project, session):
	data = {
		"session": session,
		"proj": db.retrieve_project(project),
		"theme": db.check_theme()
	}

	return render_template('portfolio.html', **data)

@app.route('/portal/add_portfolio_cat/<session>', methods=['GET', 'POST'])
@login_required
def add_portfolio_cat(session):
	data = {
		"session": session,
		"exist": db.retrieve_portfolio_cat()
	}

	if request.method == 'POST':
		cat = request.form.get('name')

		if db.add_portfolio_cat(cat):
			data['msg'] = 'success'
			return redirect(f'/portal/add_portfolio_cat/{session}')
		elif db.add_portfolio_cat(cat) == False:
			data['msg'] = 'exist'
			return render_template('add_portfolio_cat.html', **data)
		data['msg'] = 'error'
		return render_template('add_portfolio_cat.html', **data)

	return render_template('add_portfolio_cat.html', **data)

@app.route('/portal/add_resume/<session>', methods=['GET', 'POST'])
@login_required
def add_resume(session):
	data = {
		"session":session
	}

	if request.method == 'POST':
		resume = request.files['res']

		resume.save(os.path.join(app.config['IMAGE_UPLOADS'], 'resume.pdf'))

		flash("Saved resume")
		return redirect(f'/portal/add_resume/{session}')
	return render_template('add_resume.html', **data)

@app.route('/portal/add_skill/<session>', methods=['GET', 'POST'])
@login_required
def add_skill(session):
	data = {
		"session": session
	}

	if request.method == 'POST':
		skill = request.form.get("skill")
		icon = request.form.get("icon")

		if db.add_skill(skill, icon):
			data['msg'] = 'success'
			return render_template('add_skill.html', **data)
		data['msg'] = 'error'
		return render_template('add_skill.html', **data)

	return render_template('add_skill.html', **data)

if __name__ == '__main__':
	app.run(debug=True)