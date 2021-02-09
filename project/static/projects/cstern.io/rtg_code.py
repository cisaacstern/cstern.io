@app.route('/projects/<title>')
def project(title):
    data = get_static_json("static/projects/projects.json")
    projects = data['projects']
    ...
    return render_template('project.html', project=selected, last_commit=last_commit)
