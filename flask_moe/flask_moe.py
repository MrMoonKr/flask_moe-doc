from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template('index.html', page="home")

@app.route("/windows")
def env_windows():
    return render_template('windows.html')

@app.route("/jenkins/github")
def jenkins_github():
    return render_template('jenkins/github.html')

@app.route("/jenkins/bitbucket")
def jenkins_bitbucket():
    return render_template('jenkins/bitbucket.html')

@app.route("/jenkins/polling/manual")
def jenkins_polling_manual():
    return render_template('jenkins/polling/manual.html')

@app.route("/jenkins/polling/auto")
def jenkins_polling_auto():
    return render_template('jenkins/polling/auto.html')

@app.route("/jenkins/deploy")
def jenkins_deploy():
    return render_template('jenkins/deploy.html')

@app.route("/qna")
def qna_list():
    return render_template('qna/list.html')

@app.route("/qna/add")
def qna_add_get():
    return render_template('qna/add.html')

@app.route("/qna/add", methods=["POST"])
def qna_add_post():
    return ""

@app.route("/qna/<seq>")
def qna_view():
    return render_template('qna/view.html')

@app.route("/qna/<seq>/modify")
def qna_modify_get():
    return render_template('qna/modify.html')

@app.route("/qna/<seq>/modify", methods=["POST"])
def qna_modify_post():
    return ""

@app.route("/qna/<seq>/delete")
def qna_delete_get():
    return render_template('qna/delete.html')

@app.route("/qna/<seq>/delete", methods=["POST"])
def qna_delete_post():
    return ""

@app.route("/source")
def source_list():
    return render_template('sources.html')