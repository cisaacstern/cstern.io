import os
import json
import io

import markdown
from flask import Flask, render_template, request
from jinja2 import Environment

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

    in_project = next((p for p in projects if p['name'] == title), None)

    if in_project is None:
        return render_template('404.html'), 404
    else:
        selected = in_project
        
    if 'description' not in selected:
        cwd = "static/projects"
        projdir = (cwd, selected['name'])

        md = open_static('%s/%s/reflection.md' % projdir)

        selected['description'] = markdown.markdown(md, 
                                    extensions=[
                                        'codehilite', 
                                        'pymdownx.superfences', 
                                        'pymdownx.arithmatex'
                                        ],
                                    extension_configs = {
                                        'pymdownx.arithmatex' : {
                                            'generic' : 'True'
                                        }
                                    }
                                )

    name = selected['name']
    last_commit = data['badge']['base'] + name + data['badge']['lg_tail']
    
    return render_template('project.html', project=selected, last_commit=last_commit)

@app.route('/goals')
def goals():
    
    return render_template('goals.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/resume')
def resume():
    data = get_static_json("static/cv/cv.json")
    items = data['items']

    return render_template('cv.html', items=items)

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

def render_markdown_template(md_template, context):
    env = Environment()
    template = env.from_string(md_template)
    rendered_md = template.render(context=context)
    return rendered_md

def open_static(path):
    return io.open(get_static_file(path), "r", encoding="utf-8").read()