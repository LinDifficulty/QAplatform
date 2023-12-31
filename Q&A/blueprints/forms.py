import wtforms
from wtforms.validators import Email,Length,EqualTo, InputRequired
from models import UserModel
from redis import Redis
from exts import db

xtredis = Redis(host='127.0.0.1', port=6379)
# From验证前端的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误!")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名验证错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致！")])

    #自定义验证
    #1.邮箱是否已经注册
    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")

    #2.验证码是否正确
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = xtredis.get(email)
        if not captcha_model:
            print(captcha_model)
            raise wtforms.ValidationError(message="邮箱或验证码错误!")
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1, max=100, message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要写入问题id！")])


class DeleteAnswerForm(wtforms.Form):
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要写入问题id！")])
    answer_id = wtforms.IntegerField(validators=[InputRequired(message="必须要写入答案id！")])


class PersonalUserForm(wtforms.Form):
    user_id = wtforms.IntegerField()