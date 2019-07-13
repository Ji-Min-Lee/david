import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import logging
import operator

from repository import Repository

app = Flask(__name__)

app.config['LOGGING_LEVEL'] = logging.DEBUG
app.config['LOGGING_FORMAT'] = '%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d]'
app.config['LOGGING_LOCATION'] = '../'
app.config['LOGGING_FILENAME'] = 'blog4me.log'
app.config['LOGGING_MAX_BYTES'] = 100000
app.config['LOGGING_BACKUP_COUNT'] = 1000


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/main', methods=['GET'])
def main():
    repo = Repository()
    structure = dict()
    page = dict()
    for cid in range(int(repo.conn.get("cid").decode("utf-8"))):
        name = repo.get_name_by_cid(cid)
        parent_id, parent_name = repo.get_parent(cid)
        while parent_id != "-1":
            name = parent_name + " > " + name
            parent_id, parent_name = repo.get_parent(parent_id)
        structure[cid] = name
        md_path = repo.get_page(cid)
        page[cid] = md_path
    sorted_structure = sorted(structure.items(), key=operator.itemgetter(1))
    if request.method == 'GET' and request.args.get('title') is not None:
        title = request.args.get('title')
        md_path = request.args.get('md_path')
        cid = request.args.get('cid')
        if md_path is not None and md_path != "None":
            md_path += ".html"
            return render_template("main.html", title=title, menu=sorted_structure, page=page, md=md_path, cid=cid)
        else:
            return render_template("main.html", title=title, menu=sorted_structure, page=page, cid=cid)
    return render_template("main.html", title="Home", menu=sorted_structure, page=page)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['md-file']
        path = "./templates/md/" + secure_filename(f.filename)
        f.save(path)
        cid = request.args.get('cid')
        repo = Repository()
        repo.add_page(cid=cid, md_path=secure_filename(f.filename).replace(".md", ""))
        html_filename = secure_filename(f.filename).replace(".md", ".html")
        os.system(f"pandoc {path} -f markdown -t html -s -o ./templates/{html_filename}")
        return f.filename
    return "Not Allowed Error", 405


if __name__ == "__main__":
    app.run()
