import os
import json
import io

from flask import Flask, render_template, request
import markdown

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")
    projects = data['projects']
    projects.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        projects = [p for p in projects if tag.lower() in [tag.lower() for tag in p['tags']]]

    badgebase = data['badge']['base']
    badgetail = data['badge']['sm_tail']

    return render_template('projects.html', projects=projects, tag=tag, 
                            badgebase=badgebase, badgetail=badgetail)

@app.route('/projects/<title>')
def project(title):
    data = get_static_json("static/projects/projects.json")
    projects = data['projects']

    in_project = next((p for p in projects if p['link'] == title), None)

    if in_project is None:
        return render_template('404.html'), 404
    else:
        selected = in_project
        
    # load html if the json file doesn't contain a description
    if 'description' not in selected:
        path = "projects"

        md = io.open(get_static_file(
            'static/%s/%s/%s.md' % (path, selected['link'], selected['link'])), "r", encoding="utf-8").read()

        selected['description'] = markdown.markdown(md, 
                                    extensions=['codehilite', 'pymdownx.superfences', 
                                                'pymdownx.arithmatex']
                                )

    name = selected['name']
    last_commit = data['badge']['base'] + name + data['badge']['lg_tail']
    
    return render_template('project.html', project=selected, last_commit=last_commit)

@app.route('/goals')
def goals():
    data = get_static_json("static/giftgoals/giftgoals.json")['giftgoals']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('giftgoals.html', giftgoals=data, tag=tag)

def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)

def get_static_json(path):
    return json.load(open(get_static_file(path)))

def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0

