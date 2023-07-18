from flask import Blueprint, request, render_template, redirect, url_for, g
from .forms import QuestionForm, AnswerForm, DeleteAnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

bp = Blueprint("qa",__name__,url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html",questions=questions)


@bp.route("/qa/public", methods = ["GET", "POST"])
@login_required
def public_question():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return render_template("detail.html",question=question)
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html",question=question)


@bp.route("/answer/public", methods = ["GET", "POST"])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        print(f"{answer}已入库,信息为：{answer.content}")
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    else:
        print("数据验证失败")
        return redirect(url_for('qa.qa_detail', qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)

@bp.route("/answer/public/delete_question", methods = ["GET", "POST"])
def delete_question():
    form = AnswerForm(request.form)
    question_id = form.question_id.data
    question = QuestionModel.query.get(question_id)
    answers = AnswerModel.query.filter(AnswerModel.question_id == question_id).all()
    for answer in answers:
        db.session.delete(answer)
    db.session.delete(question)
    db.session.commit()
    return redirect("/")

@bp.route("/answer/public/delete_answer", methods = ["GET", "POST"])
def delete_answer():
    form = DeleteAnswerForm(request.form)
    answer_id = form.answer_id.data
    question_id = form.question_id.data
    answer = AnswerModel.query.get(answer_id)
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('qa.qa_detail', qa_id=question_id))

# todo:问题修改功能