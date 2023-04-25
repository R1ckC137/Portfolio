from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:889900aassddffgghhjj@localhost/portfolio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(600), nullable=False)
    description_1 = db.Column(db.Text, nullable=False)
    description_2 = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

    def __str__(self):
        return self.project_name


with app.test_request_context():
    db.create_all()
    all_projects = []
    portfolio = Portfolio.query.all()
    for project in portfolio:
        project_info = {
            'project_name': project.project_name,
            'intro': project.intro,
            'description_1': project.description_1,
            'description_2': project.description_2,
            'technologies': project.technologies,
            }
        all_projects.append(project_info)
        print(all_projects)


@app.route('/')
def index():
    global all_projects
    with app.test_request_context():
        db.create_all()
    return render_template('index.html', name='index', all_projects=all_projects)


@app.route('/project/<string:project_name>/<description_1>/<description_2>/<technologies>')
def project(project_name, description_1, description_2, technologies):
    global all_projects
    return render_template('project.html', all_projects=all_projects, project_name=project_name,
                           description_1=description_1, description_2=description_2, technologies=technologies)


@app.route('/add_project', methods=['POST', 'GET'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        intro = request.form['intro']
        description_1 = request.form['description_1']
        description_2 = request.form['description_2']
        technologies = request.form['technologies']

        add_project = Portfolio(project_name=project_name, intro=intro,
                                description_1=description_1, description_2=description_2, technologies=technologies)
        db.session.add(add_project)
        db.session.commit()

        return render_template('add_project.html')
    else:
        return render_template('add_project.html')


if __name__ == '__main__':
    app.run(debug=True)
