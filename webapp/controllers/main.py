# -*- coding: utf-8 -*-
# @Author: XUEQUN
# @Date:   2017-03-17 11:16:27
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-09-28 10:10:40

from flask import (render_template,
                   current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   flash,
                   session,
                   make_response)
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
)
from webapp.forms import LoginForm, RegisterForm
from os import path
from webapp.models import User,db
from flask_login import login_user, logout_user
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import StringIO
import string,random


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir,'templates','main'),
    )

#生成验证码图片
#numbers = ''.join(map(str, range(10)))
numbers = string.digits+string.letters
chars = ''.join((numbers))


def create_validate_code(size=(120, 30),
                         chars=chars,
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(255, 0, 0),
                         font_size=18,
                         font_type="/usr/local/src/myproject/cdnadmin/webapp/static/temp/stkaiti.ttf",
                         length=4,
                         draw_points=True,
                         point_chance = 2):
    '''''
    size: 图片的大小，格式（宽，高），默认为(120, 30)
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，默认为 stkaiti.ttf
    length: 验证码字符个数
    draw_points: 是否画干扰点
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    '''

    width, height = size
    img = Image.new(mode, size, bg_color) # 创建图形
    draw = ImageDraw.Draw(img) # 创建画笔

    def get_chars():
        '''''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_points():
        '''''绘制干扰点'''
        chance = min(50, max(0, int(point_chance))) # 大小限制在[0, 50]

        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''''绘制验证码字符'''
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 4),
                    strs, font=font, fill=fg_color)

        return strs

    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    """
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
   """
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

    #image保存到内存中
    buf = StringIO.StringIO()
    img.save(buf,'JPEG',quality=70)

    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'

    return response,strs

@main_blueprint.route('/')
def index():
    return redirect(url_for('main.login'))

@main_blueprint.route('/login', methods=['GET', 'POST'])
#@oid.loginhandler
def login():
    form = LoginForm()
    print 'In form %s' %(form.verification_code.data)
    print 'In session %s' %(session.get('code'))
    #获取表单里面输入的数据
    form_code = form.verification_code.data
    #获取session中的数字
    session_code = session.get('code')
    #openid_form = OpenIDForm()

    # if openid_form.validate_on_submit():
    #     return oid.try_login(
    #         openid_form.openid.data,
    #         ask_for=['nickname', 'email'],
    #         ask_for_optional=['fullcmd

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )
        if form_code != session_code:
            form.verification_code.errors.append(u'验证码错误，请重新输入！')
        else:

        #flash("You have been logged in.", category="success")
            return redirect(url_for('cdn.home'))

    # openid_errors = oid.fetch_error()
    # if openid_errors:
    #     flash(openid_errors, category="danger")

    #return render_template('login.html', form=form, openid_form=openid_form)
    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )

    flash(u"成功退出!", category="success")
    return redirect(url_for('.login'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
#@oid.loginhandler
def register():
    form = RegisterForm()
    # openid_form = OpenIDForm()

    # if openid_form.validate_on_submit():
    #     return oid.try_login(
    #         openid_form.openid.data,
    #         ask_for=['nickname', 'email'],
    #         ask_for_optional=['fullname']
    #     )

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.email = form.email.data
        new_user.tel = form.tel.data
        new_user.status = 0
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash(u"用户创建成功，请登陆.", category="success")

        return redirect(url_for('.login'))

    # openid_errors = oid.fetch_error()
    # if openid_errors:
    #     flash(openid_errors, category="danger")

    #return render_template('register.html', form=form, openid_form=openid_form)
    return render_template('register.html', form=form)



@main_blueprint.route('/code/')
def get_code():
    #把strs发给前端,或者在后台使用session保存
    #返回图片和上面的文字
    response,strs = create_validate_code()
    #保存文字到session
    session['code'] = strs
    #image保存到内存中
    #buf = StringIO.StringIO()
    #code_img.save(buf,'JPEG',quality=70)

    #buf_str = buf.getvalue()
    #response = make_response(buf_str)
    #response.headers['Content-Type'] = 'image/jpeg'
    return response
