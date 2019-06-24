from flask import Flask, render_template
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


@app.route('/main')
def main():
    repo = Repository()
    structure = dict()
    for cid in range(int(repo.conn.get("cid").decode("utf-8"))):
        print(cid)
        name = repo.get_name_by_cid(cid)
        parent_id, parent_name = repo.get_parent(cid)
        while parent_id != "-1":
            print(parent_id, parent_name)
            name = parent_name + " > " + name
            parent_id, parent_name = repo.get_parent(parent_id)
        structure[cid] = name
    sorted_structure = sorted(structure.items(), key=operator.itemgetter(1))
    return render_template("main.html", menu=sorted_structure)


if __name__ == "__main__":
    app.run()
