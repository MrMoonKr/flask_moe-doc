import zipfile
import datetime
import paginate
import telegram
import yaml

from flask import Flask, render_template, request, url_for, redirect, send_file, flash, jsonify
from paginate_sqlalchemy import SqlalchemyOrmWrapper
from sqlalchemy import asc, desc, func, or_
from formencode import htmlfill
from six import BytesIO

from flask_moe.database import db_session
from flask_moe.models import Source, BoardQna, BoardQnaReply

app = Flask(__name__)
app.config.update(SECRET_KEY='go$Thgy4@Tgha%*gfg48vV')

config = yaml.load(open("config.yml"))


def paginate_link_tag(item):
    """
    Create an A-HREF tag that points to another page usable in paginate.
    """
    a_tag = paginate.Page.default_link_tag(item)

    if item['type'] == 'current_page':
        return paginate.make_html_tag('li', paginate.make_html_tag('a', a_tag), **{"class": "active"})
    return paginate.make_html_tag("li", a_tag)


@app.route("/")
def index_page():
    current_path = "index"

    tpl_vars = dict(
        current_path=current_path
    )
    return render_template('index.html', **tpl_vars)


# @app.route("/environ")
# def environ():
#    return "<br>".join(["{key}:{value}".format(key=key, value=value) for key, value in request.environ.items()])


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


@app.route("/board/<board_section>")
def qna_list(board_section):
    current_page = request.args.get('page', 1)
    srch_key = request.args.get('srch_key', '')
    srch_value = request.args.get('srch_value', '')

    page_url = url_for("qna_list", board_section=board_section, srch_key=srch_key, srch_value=srch_value)
    page_url = str(page_url) + "&page=$page"

    record_cnt = db_session.query(func.count(BoardQna.id)).filter(BoardQna.section == board_section)
    if srch_key and srch_value:
        if srch_key == "all":
            record_cnt = record_cnt.filter(or_(BoardQna.title.contains(srch_value),
            BoardQna.user_name.contains(srch_value),
            BoardQna.content.contains(srch_value)))
        elif srch_key == "title":
            record_cnt = record_cnt.filter(BoardQna.title.contains(srch_value))
        elif srch_key == "author":
            record_cnt = record_cnt.filter(BoardQna.user_name.contains(srch_value))
        elif srch_key == "content":
            record_cnt = record_cnt.filter(BoardQna.content.contains(srch_value))
    record_cnt = record_cnt.first()

    records = db_session.query(BoardQna).filter(BoardQna.section == board_section)
    if srch_key and srch_value:
        if srch_key == "all":
            records = records.filter(or_(BoardQna.title.contains(srch_value),
            BoardQna.user_name.contains(srch_value),
            BoardQna.content.contains(srch_value)))
        elif srch_key == "title":
            records = records.filter(BoardQna.title.contains(srch_value))
        elif srch_key == "author":
            records = records.filter(BoardQna.user_name.contains(srch_value))
        elif srch_key == "content":
            records = records.filter(BoardQna.content.contains(srch_value))
    records = records.order_by(desc(BoardQna.create_date))

    items_per_page = 15
    virtual_article_no = record_cnt[0] - (current_page - 1) * items_per_page
    # https://okky.kr/article/407295

    paginator = paginate.Page(records, current_page, page_url=page_url, items_per_page=items_per_page,
                              wrapper_class=SqlalchemyOrmWrapper)

    tpl_vars = dict(
        current_path=board_section,
        paginator=paginator,
        paginate_link_tag=paginate_link_tag,
        page_url=page_url,
        virtual_article_no=virtual_article_no
    )

    return render_template('qna/qna.html', **tpl_vars)


@app.route("/board/<board_section>/<article_id>")
def qna_view(board_section, article_id):
    record = db_session.query(BoardQna).filter(BoardQna.section == board_section).filter(BoardQna.id == article_id).first()
    
    if record:
        db_session.commit()
    
        tpl_vars = dict(
            current_path=board_section,
            record=record
        )
    
        return render_template('qna/view.html', **tpl_vars)
    else:
        return redirect(url_for('qna_list', board_section=board_section))


@app.route("/board/<board_section>/<article_id>/hit", methods=["POST"])
def qna_hit_increment(board_section, article_id):
    record = db_session.query(BoardQna).filter(BoardQna.section == board_section).filter(BoardQna.id == article_id).first()
    record.hit += 1
    
    db_session.commit()
    
    return jsonify(dict(success=True))


@app.route("/board/<board_section>/<article_id>/modify")
def qna_modify_view(board_section, article_id):
    record = db_session.query(BoardQna).filter(BoardQna.section == board_section).filter(BoardQna.id == article_id).first()
    
    tpl_vars = dict(
        current_path=board_section,
        record=record
    )
    
    return render_template('qna/modify.html', **tpl_vars)


@app.route("/board/<board_section>/<article_id>/modify", methods=["POST"])
def qna_modify(board_section, article_id):
    req_json = request.get_json()

    ret_dict = dict(success=False)
    
    record = db_session.query(BoardQna).filter(BoardQna.section == board_section).filter(BoardQna.id == article_id).first()
    record.title = req_json.get('title')
    record.content = req_json.get('content')
    record.user_name = req_json.get('author')
    record.ip = request.environ['REMOTE_ADDR']
    
    if req_json.get("password") == record.password:
        #db_session.add(record)
        db_session.commit()

        ret_dict["success"] = True
    
        bot_message = "[{board_section}] 글이 수정되었습니다\n" \
        "Title: {title}\n" \
        "Date: {create_date}\n" \
        "link: {link}"

        bot = telegram.Bot(token=config['telegram_token'])

        try:
            bot.sendMessage(chat_id=config['telegram_search5'], text=bot_message.format(
                board_section=board_section,
                title=record.title,
                create_date=record.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                link="{}/board/{}/{}".format(get_host_url(), board_section, record.id)))
        except:
            pass
    
    return jsonify(ret_dict)


@app.route("/board/<board_section>/add")
def qna_add_view(board_section):

    tpl_vars = dict(
        current_path=board_section
    )

    return render_template('qna/write.html', **tpl_vars)


@app.route("/board/<board_section>/add", methods=["POST"])
def qna_add(board_section):
    req_json = request.get_json()
    
    record = BoardQna()
    record.section = board_section
    record.title = req_json.get('title')
    record.content = req_json.get('content')
    record.password = req_json.get('password')
    record.create_date = datetime.datetime.now()
    record.hit = 0
    record.user_name = req_json.get('author')
    record.ip = request.environ['REMOTE_ADDR']

    db_session.add(record)
    db_session.commit()

    bot_message = "[{board_section}] 새 글이 등록되었습니다\n" \
    "Title: {title}\n" \
    "Date: {create_date}\n" \
    "link: {link}"

    bot = telegram.Bot(token=config['telegram_token'])

    try:
        bot.sendMessage(chat_id=config['telegram_search5'], text=bot_message.format(
            board_section=board_section,
            title=record.title,
            create_date=record.create_date.strftime("%Y-%m-%d %H:%M:%S"),
            link="{}/board/{}/{}".format(get_host_url(), board_section, record.id)))
    except:
        pass
    
    return jsonify(dict(success=True))


@app.route("/board/<board_section>/<article_id>", methods=["POST"])
def qna_delete(board_section, article_id):
    record = db_session.query(BoardQna).filter(BoardQna.section == board_section).filter(BoardQna.id == article_id).first()

    ret_dict = dict(success=False)

    req_json = request.get_json()
    if req_json.get("password") == record.password:
        db_session.delete(record)

        ret_dict["success"] = True

        bot_message = "[{board_section}] 글이 삭제되었습니다\n" \
        "Title: {title}\n" \
        "Date: {create_date}\n" \
        "link: {link}"

        bot = telegram.Bot(token=config['telegram_token'])

        try:
            bot.sendMessage(chat_id=config['telegram_search5'], text=bot_message.format(
                board_section=board_section,
                title=record.title,
                create_date=record.create_date.strftime("%Y-%m-%d %H:%M:%S"),
                link="{}/board/{}/{}".format(get_host_url(), board_section, record.id)))
        except:
            pass

        db_session.commit()
    
    return jsonify(ret_dict)


@app.route("/source")
def source_list():
    current_path = "source"

    chapter1_records = db_session.query(Source).filter(
        Source.code_num.startswith('1-')).order_by(asc(Source.id))
    chapter2_records = db_session.query(Source).filter(
        Source.code_num.startswith('2-')).order_by(asc(Source.id))
    chapter3_records = db_session.query(Source).filter(
        Source.code_num.startswith('3-')).order_by(asc(Source.id))
    chapter4_records = db_session.query(Source).filter(
        Source.code_num.startswith('4-')).order_by(asc(Source.id))
    chapter5_records = db_session.query(Source).filter(
        Source.code_num.startswith('5-')).order_by(asc(Source.id))
    chapter6_records = db_session.query(Source).filter(
        Source.code_num.startswith('6-')).order_by(asc(Source.id))
    chapter7_records = db_session.query(Source).filter(
        Source.code_num.startswith('7-')).order_by(asc(Source.id))
    chapter8_records = db_session.query(Source).filter(
        Source.code_num.startswith('8-')).order_by(asc(Source.id))
    chapter9_records = db_session.query(Source).filter(
        Source.code_num.startswith('9-')).order_by(asc(Source.id))
    chapter10_records = db_session.query(Source).filter(
        Source.code_num.startswith('10-')).order_by(asc(Source.id))
    chapter11_records = db_session.query(Source).filter(
        Source.code_num.startswith('11-')).order_by(asc(Source.id))

    tpl_vars = dict(
        current_path=current_path,
        chapter1_records=chapter1_records,
        chapter2_records=chapter2_records,
        chapter3_records=chapter3_records,
        chapter4_records=chapter4_records,
        chapter5_records=chapter5_records,
        chapter6_records=chapter6_records,
        chapter7_records=chapter7_records,
        chapter8_records=chapter8_records,
        chapter9_records=chapter9_records,
        chapter10_records=chapter10_records,
        chapter11_records=chapter11_records
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
    attachment_filename = ''
    strIO = BytesIO()

    if id.isnumeric():
        record = db_session.query(Source).filter(Source.id == id).first()

        strIO = BytesIO()
        strIO.write(record.file_content.encode('utf-8'))
        strIO.seek(0)

        attachment_filename = "%s.py" % record.code_num
        if "." in record.code_num:
            attachment_filename = record.code_num
    else:
        strIO = BytesIO()
        zip_file = zipfile.ZipFile(strIO, 'w')

        records = db_session.query(Source)
        if id.startswith('chapter'):
            records = records.filter(Source.code_num.startswith('{0}-'.format(id[7:])))

        for record in records:
            file_cont = BytesIO()
            file_cont.write(record.file_content.encode('utf-8'))
            file_cont.seek(0)

            attachment_filename = "%s.py" % record.code_num
            if "." in record.code_num:
                attachment_filename = record.code_num

            zip_file.writestr(attachment_filename, file_cont.getvalue())

        zip_file.close()

        strIO.seek(0)

        if id == 'all':
            attachment_filename = 'sources.zip'
        else:
            attachment_filename = 'sources_{0}.zip'.format(id)

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


def get_host_url():
    current_host = request.environ["HTTP_HOST"]
    if len(request.environ.get("SERVER_PORT", "")) > 0:
        current_host = "{}:{}".format(current_host, request.environ["SERVER_PORT"])
    
    if request.environ.get("HTTPS", "") == "on":
        current_host = "https://{}".format(current_host)
    else:
        current_host = "http://{}".format(current_host)

    return current_host


def page_title():
    request_url = request.environ
    
    return dict(
        flask_web_qna="Flask 기반의 파이썬 웹 프로그래밍",
        vuejs_first_step="Vue.js 첫걸음"
    ).get(request_url['werkzeug.request'].view_args['board_section'])


def disqus_url():
    request_url = request.environ
    
    return dict(
        flask_web_qna="flask-based-python-web-programming.disqus.com",
        vuejs_first_step="vuejs-first-step.disqus.com"
    ).get(request_url['werkzeug.request'].view_args['board_section'])


@app.context_processor
def utility_processor():
    return dict(get_host_url=get_host_url, page_title=page_title, disqus_url=disqus_url)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.debug=True
    app.run()
