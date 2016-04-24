from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index_page():
    current_path = "index"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('index.html', **tpl_vars)


@app.route("/windows")
def env_windows():
    current_path = "windows"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('windows.html', **tpl_vars)


@app.route("/jenkins/github")
def jenkins_github():
    current_path = "jenkins.github"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('jenkins/github.html', **tpl_vars)


@app.route("/jenkins/bitbucket")
def jenkins_bitbucket():
    current_path = "jenkins.bitbucket"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('jenkins/bitbucket.html', **tpl_vars)


@app.route("/jenkins/polling/manual")
def jenkins_polling_manual():
    current_path = "jenkins.polling.manual"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('jenkins/polling/manual.html', **tpl_vars)


@app.route("/jenkins/polling/auto")
def jenkins_polling_auto():
    current_path = "jenkins.polling.auto"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('jenkins/polling/auto.html', **tpl_vars)


@app.route("/jenkins/deploy")
def jenkins_deploy():
    current_path = "jenkins.deploy"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('jenkins/deploy.html', **tpl_vars)


@app.route("/qna")
def qna_list():
    current_path = "qna"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('qna/list.html', **tpl_vars)


@app.route("/qna/add")
def qna_add_get():
    current_path = "qna"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('qna/add.html', **tpl_vars)


@app.route("/qna/add", methods=["POST"])
def qna_add_post():
    return ""


@app.route("/qna/<seq>")
def qna_view():
    current_path = "qna"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('qna/view.html', **tpl_vars)


@app.route("/qna/<seq>/modify")
def qna_modify_get():
    current_path = "qna"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('qna/modify.html', **tpl_vars)


@app.route("/qna/<seq>/modify", methods=["POST"])
def qna_modify_post():
    return ""


@app.route("/qna/<seq>/delete")
def qna_delete_get():
    current_path = "qna"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('qna/delete.html', **tpl_vars)


@app.route("/qna/<seq>/delete", methods=["POST"])
def qna_delete_post():
    return ""


@app.route("/source")
def source_list():
    current_path = "source"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('sources.html', **tpl_vars)

if __name__ == "__main__":
    app.run()