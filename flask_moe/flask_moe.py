from flask import Flask, render_template, request, url_for, redirect, send_file, flash
from flask_moe.database import db_session
from flask_moe.models import Source
import flask_moe.lib
from io import StringIO
from formencode import htmlfill
from six import BytesIO
from sqlalchemy import asc

app = Flask(__name__)
app.config.update(SECRET_KEY='go$Thgy4@Tgha%*gfg48vV')


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

    records = db_session.query(Source).order_by(asc(Source.id))

    tpl_vars = dict(
        current_path=current_path,
        records=records
    )

    return render_template('sources.html', **tpl_vars)


@app.route("/source/write")
def source_write_get():
    current_path = "source"

    tpl_vars = dict(
        current_path=current_path
    )

    return render_template('sources/write.html', **tpl_vars)


@app.route("/source/write", methods=["POST"])
def source_write_post():
    record = None

    if not request.form.get('id', ''):
        record = Source(
            request.form.get('code_num', ''),
            request.form.get('description', ''),
            request.form.get('file_content', '').replace(chr(160), chr(32))
        )
        db_session.add(record)
    else:
        record = db_session.query(Source).filter(
            Source.id == request.form.get('id', '')
        ).first()
        record.code_num = request.form.get('code_num', '')
        record.description = request.form.get('description', '')
        record.file_content = request.form.get('file_content', '').replace(chr(160), chr(32))

    db_session.commit()

    flash('{}가 저장되었습니다'.format(record.code_num))

    return redirect(url_for('source_write_get'))


@app.route("/source/<id>/download")
def source_download(id):
    record = db_session.query(Source).filter(Source.id == id).first()

    strIO = BytesIO()
    strIO.write(record.file_content.encode('utf-8'))
    strIO.seek(0)

    attachment_filename = "%s.py" % record.code_num
    if "." in record.code_num:
        attachment_filename = record.code_num

    return send_file(strIO, as_attachment=True,
                     attachment_filename=attachment_filename)


@app.route("/source/<code_num>")
def source_view(code_num):
    record = db_session.query(Source).filter(Source.code_num == code_num).first()

    current_path = "source"

    tpl_vars = dict(
        current_path=current_path
    )

    tmpl = render_template('sources/write.html', **tpl_vars)
    return htmlfill.render(tmpl, record.to_dict())


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    print(app.url_map)
    app.debug=True
    app.run()