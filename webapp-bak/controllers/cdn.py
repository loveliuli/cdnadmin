# -*- coding: utf-8 -*-
# @Author: liuli
# @Date:   2017-03-15 23:28:39
# @Last Modified by:   XUEQUN
# @Last Modified time: 2017-08-08 15:06:56
import os,time
from os import path
import datetime,json
from sqlalchemy import func
from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   abort,
                   flash,
                   request)
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from webapp.models import db,User,Project,Charge_info,Charge_statics,Domain
from webapp.forms import CommentForm, PostForm
from ..utils import wangsustatics,fastwebstatics
from ..utils.pro import project_http,project_https,fastweb

cdn_blueprint = Blueprint(
    'cdn',
    __name__,
    template_folder=path.join(path.pardir,'templates','cdn'),
    url_prefix="/cdn"
    )


'''
处理时间不为json格式的问题
'''
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

'''
自定义过滤器
'''
def dateformat(value, format="%Y-%m"):
    return value.strftime(format)


#download_type分为http和https两种
#download_domian分为project_http.domain和project_https.domain两种
#fastweb只有http一种类型，而wangsu有http和https两种类型
def insert_traffic_data(cname,year,month,download_type=None,download_domain=None):
    if cname =='fastweb':
        os.chdir('/usr/local/src/myproject/cdnadmin/webapp/utils')
        _rt_statics,total_money = fastwebstatics.get_statics_result(year,month)
        print _rt_statics,total_money
    elif cname == 'wangsu' and download_type=='http':
        _rt_statics = wangsustatics.get_traffic_result(myflag=download_type,mydomain=project_http.domain,year=year,month=month)
    elif  cname == 'wangsu' and download_type=='https':
        _rt_statics = wangsustatics.get_traffic_result(myflag=download_type,mydomain=project_https.domain,year=year,month=month)
    for val in _rt_statics:
        new_comment = Charge_statics()
        new_comment.charge_date = datetime.datetime.now().strptime(val[0],"%Y-%m")
        new_comment.charge_cname = val[1]
        new_comment.charge_type = val[2]
        new_comment.charge_project = val[3]
        new_comment.charge_area = val[4]
        new_comment.charge_traff = val[5]
        new_comment.charge_total = val[6]
        new_comment.charge_percent = val[7]

        db.session.add(new_comment)
        db.session.commit()

def commit_date(domain_cname):
    new_domain = Domain()
    new_domain.cname = domain_cname
    new_domain.status = 1
    new_domain.purpose = ''
    new_domain.project_id = project_id
    new_domain.domain_name = v
    new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
    new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)

    db.session.add(new_domain)
    db.session.commit()

def insert_domain(domain_cname):
    if domain_cname == 'fastweb':
        fastweb_dic = {'jx1':'剑一','jx3':'剑三','jxsj':'剑世','yy':'月影','fkxd':'反恐行动'}
        for k in fastweb.project:
            if k == 'all':continue
            project_id = Project.query.filter_by(project_name=fastweb_dic[k]).first().id
            for v in fastweb.project[k]:
                new_domain = Domain()
                new_domain.cname = '快网'
                new_domain.status = 1
                new_domain.purpose = '快网-HTTP下载加速'
                new_domain.project_id = project_id
                new_domain.domain_name = v
                new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
                new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)

                db.session.add(new_domain)
                db.session.commit()
    elif domain_cname == 'wangsu_http':
        for k in project_http.domain:
            if k == 'all':continue
            project_id = Project.query.filter_by(project_name=k).first().id
            for v in project_http.domain[k]:
                new_domain = Domain()
                new_domain.cname = '网宿'
                new_domain.status = 1
                new_domain.purpose = '网宿-HTTP下载加速'
                new_domain.project_id = project_id
                new_domain.domain_name = v
                new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
                new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)

                db.session.add(new_domain)
                db.session.commit()
    elif domain_cname == 'wangsu_https':
        for k in project_https.domain:
            if k == 'all':continue
            project_id = Project.query.filter_by(project_name=k).first().id
            for v in project_https.domain[k]:
                new_domain = Domain()
                new_domain.cname = '网宿'
                new_domain.status = 1
                new_domain.purpose = '网宿-HTTPS下载加速'
                new_domain.project_id = project_id
                new_domain.domain_name = v
                new_domain.end_date = datetime.datetime.now()+datetime.timedelta(1000)
                new_domain.start_date = datetime.datetime.now()-datetime.timedelta(1500)

                db.session.add(new_domain)
                db.session.commit()

def get_current_user():
    try:
        cur_user = current_user.username
    except Exception as e:
        flash(u"请先登录!")
        return  redirect(url_for('main.login'))
    else:
        user = User.query.filter_by(username=cur_user).one()
        return user

    #price=Charge_info.query.filter_by(nick_name='cn').filter_by(charge_cname='网宿').filter_by(charge_type='下载加速').all()[0].charge_price
    #return prices

@cdn_blueprint.route('/')
def home():
    cur_user = get_current_user()
    distinct_cname_list = db.session.query(func.distinct(Charge_statics.charge_cname)).all()
    charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).group_by(Charge_statics.charge_project).all()
    fa_list = ["fa fa-eye fa-5x","fa fa-shopping-cart fa-5x","fa fa-comments fa-5x","fa fa-users fa-5x","fa fa-bug fa-5x","fa fa-calendar fa-5x","fa fa-cloud-upload fa-5x","fa fa-cloud-download fa-5x"]
    fa_color = ["card-image red","card-image orange","card-image blue","card-image"]
    return render_template('dashboardtype.html',login_user=cur_user.username,charge_statics=charge_statics,fa_list=fa_list,fa_color=fa_color)

@cdn_blueprint.route('/logout/')
def logout():
    return  redirect(url_for('main.logout'))

@cdn_blueprint.route('/custom/')
def custom():
    cur_user = get_current_user()
    #insert_traffic_data('wangsu',2017,7,download_type='http',download_domain=project_http.domain)
    #insert_domain('fastweb')
    return render_template('custom.html',login_user=cur_user.username,price='successed!')


@cdn_blueprint.route('/dashboard/')
def dashboard():
    cur_user = get_current_user()
    project_legend_fastweb,status_data_fastweb_5=Charge_statics.get_charge_statics(charge_date='2017-05-01 00:00:00',charge_cname='快网')
    project_legend_fastweb,status_data_fastweb_6=Charge_statics.get_charge_statics(charge_date='2017-06-01 00:00:00',charge_cname='快网')
    project_legend_wangsu,status_data_wangsu_5,project_legend_client_wangsu,status_data_wangsu_client_5,project_legend_phone_wangsu,status_data_wangsu_phone_5=Charge_statics.get_charge_statics(charge_date='2017-05-01 00:00:00',charge_cname='网宿')
    project_legend_wangsu,status_data_wangsu_6,project_legend_client_wangsu,status_data_wangsu_client_6,project_legend_phone_wangsu,status_data_wangsu_phone_6=Charge_statics.get_charge_statics(charge_date='2017-06-01 00:00:00',charge_cname='网宿')

    return render_template('dashboard.html',login_user=cur_user.username,
        project_legend_wangsu=json.dumps(project_legend_wangsu),
        status_data_wangsu_5=json.dumps(status_data_wangsu_5),status_data_wangsu_6=json.dumps(status_data_wangsu_6),
        project_client_wangsu=json.dumps(project_legend_client_wangsu),
        status_data_wangsu_client_5=json.dumps(status_data_wangsu_client_5),status_data_wangsu_client_6=json.dumps(status_data_wangsu_client_6),
        project_legend_phone_wangsu=json.dumps(project_legend_phone_wangsu),
        status_data_wangsu_phone_5=json.dumps(status_data_wangsu_phone_5),status_data_wangsu_phone_6=json.dumps(status_data_wangsu_phone_6),
        project_legend_fastweb=json.dumps(project_legend_fastweb),
        status_data_fastweb_5=json.dumps(status_data_fastweb_5),status_data_fastweb_6=json.dumps(status_data_fastweb_6)

        )

@cdn_blueprint.route('/dashboard/index/<string:gametype>/', methods=('GET', 'POST'))
def dashboardshowtype(gametype):
    cur_user = get_current_user()
    client_game = ['剑一','剑二','封神一','剑三','剑世','月影','反恐行动','猎魔','蜂鸟','春秋','麻辣江湖','封神三','格斗灌篮王']
    other = ['数据中心','tako','公共']
    distinct_cname_list = db.session.query(func.distinct(Charge_statics.charge_cname)).all()
    charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).group_by(Charge_statics.charge_project).all()
    charge_statics_client_game = []
    charge_statics_phone_game = []
    charge_statics_other_game = []
    for item in charge_statics:
        if item[1] in client_game and item[1] not in other:
            charge_statics_client_game.append(item)
        elif item[1] in other:
            charge_statics_other_game.append(item)
        else:
            charge_statics_phone_game.append(item)
    print charge_statics_phone_game,charge_statics_client_game
    fa_list = ["fa fa-eye fa-5x","fa fa-shopping-cart fa-5x","fa fa-comments fa-5x","fa fa-users fa-5x","fa fa-bug fa-5x","fa fa-calendar fa-5x","fa fa-cloud-upload fa-5x","fa fa-cloud-download fa-5x"]
    fa_color = ["card-image red","card-image orange","card-image blue","card-image"]
    if gametype == 'client':
        return render_template('dashboardtype.html',login_user=cur_user.username,charge_statics=charge_statics_client_game,fa_list=fa_list,fa_color=fa_color)
    elif gametype == 'phone':
        return render_template('dashboardtype.html',login_user=cur_user.username,charge_statics=charge_statics_phone_game,fa_list=fa_list,fa_color=fa_color)
    else:
        return render_template('dashboardtype.html',login_user=cur_user.username,charge_statics=charge_statics_other_game,fa_list=fa_list,fa_color=fa_color)

@cdn_blueprint.route('/dashboard/<string:project>/', methods=('GET', 'POST'))
def dashboardshowproject(project):
    cur_user = get_current_user()
    charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_cname.label('charge_cname'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).filter_by(charge_project=project).group_by(Charge_statics.charge_cname,Charge_statics.charge_date).all()
    legend_list = []
    xaxis_list = []
    #{'cname1':[(date1,data1),(date2,data2)],'cname2':[(date1,data1),(date2,data2)]}
    data_dic = {}
    rt_dic = {}
    data_list = []

    for s in charge_statics:
        if s.charge_cname in legend_list:continue
        legend_list.append(s.charge_cname)
    for s in charge_statics:
        if s.charge_date.strftime('%Y-%m') in xaxis_list:continue
        xaxis_list.append(s.charge_date.strftime('%Y-%m'))

    for rr in legend_list:
        for rt in charge_statics:
            if rr == rt.charge_cname:
                print rt[3],type(rt[3])
                data_list.append((rt[0].strftime('%Y-%m'),round(rt[3],3)))
        data_dic[rr]=data_list
        data_list = []

    for cname,value in data_dic.items():
        rt_dic[cname]=[x[1] for x in value]
    print rt_dic
    color_list = ['rgb(0,136,212)','rgb(219,50,51)']
    return render_template('dashboardshowproject.html',
        login_user=cur_user.username,
        charge_statics=charge_statics,
        legend_list=json.dumps(data_dic.keys()),
        xaxis_list=json.dumps(xaxis_list),
        rt_dic=rt_dic,
        color_list=color_list
        )


@cdn_blueprint.route('/tables/')
def tables():
    cur_user = get_current_user()
    #price = get_price()
    charge_statics = Charge_statics.query.all()
    return render_template('table.html',login_user=cur_user.username,price=charge_statics)
    #os.chdir('/usr/local/src/myproject/cdnadmin/webapp/utils')
    #with open('fastwebstaticsresult.txt') as f:
    #    rt=f.readlines()
    #    _rt_statics,total_money = eval(rt[0])
    #return render_template('table.html',login_user=cur_user.username,statics=_rt_statics)

@cdn_blueprint.route('/tablestotal/')
def tablestotal():
    cur_user = get_current_user()
    rt_list = []
    distinct_date_list = db.session.query(func.distinct(Charge_statics.charge_date)).all()
    distinct_cname_list = db.session.query(func.distinct(Charge_statics.charge_cname)).all()
    for d in distinct_date_list:
        for c in distinct_cname_list:
            charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_cname.label('charge_cname'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).filter_by(charge_date=d[0]).filter_by(charge_cname=c[0]).group_by(Charge_statics.charge_project).all()
            rt_list.extend(charge_statics)
    return render_template('tabletotal.html',login_user=cur_user.username,prices=rt_list)

@cdn_blueprint.route('/tablestotalgroup/')
def tablestotalgroup():
    project = request.args.get('myproject','')
    mydate =  request.args.get('mydate','')
    mycname = request.args.get('mycname','')
    mytype = request.args.get('mytype','')
    cur_user = get_current_user()
    rt_list = []
    distinct_date_list = db.session.query(func.distinct(Charge_statics.charge_date)).all()
    distinct_cname_list = db.session.query(func.distinct(Charge_statics.charge_cname)).all()
    charge_statics = db.session.query(Charge_statics.charge_date.label('charge_date'),Charge_statics.charge_cname.label('charge_cname'),Charge_statics.charge_type.label('charge_type'),Charge_statics.charge_project.label('charge_project'),func.sum(Charge_statics.charge_total)).filter_by(charge_date=mydate).filter_by(charge_cname=mycname).filter_by(charge_project=project).group_by(Charge_statics.charge_type).all()
    rt_list = [rt for rt in charge_statics if rt[0] is not None]
    return render_template('tabletotalgroup.html',login_user=cur_user.username,prices=rt_list)

@cdn_blueprint.route('/tablestatics/',methods=['GET'])
def tablestatics():
    cur_user = get_current_user()
    project = request.args.get('myproject','')
    mydate =  request.args.get('mydate','')
    mycname = request.args.get('mycname','')
    mytype = request.args.get('mytype','')
    rt_area = []
    rt_result = []
    domain_list = []


    #print project,mydate
    #print project,mydate,mycname,mytype
    rt = Charge_statics.query.filter_by(charge_project=project).filter_by(charge_date=mydate).filter_by(charge_cname=mycname).filter_by(charge_type=mytype).all()
    pro =Project.query.filter_by(project_name=project).all()
    #print rt,pro
    for x in pro:
        for y in x.domains:
            if y.cname == str(mycname):
                domain_list.append(y.domain_name)
    #print project,domain_list

    for z in rt:
        rt_total = {}
        rt_area.append(z.charge_area)
        rt_total['value']=z.charge_total
        rt_total['name']=z.charge_area
        rt_result.append(rt_total)
    #print rt_area,rt_result
    return render_template('tablestatics.html',login_user=cur_user.username,rt_area=json.dumps(rt_area),rt_result=json.dumps(rt_result),rt_cname=mycname,rt_project=project,rt_date=mydate,rt_domains=domain_list)

@cdn_blueprint.route('/domainadmin/')
def domainadmin():
    domain_status = {0:"已停用",1:"使用中"}
    project = Project.query.all()
    cur_user = get_current_user()
    domains = Domain.query.all()
    #print domains
    return render_template('domainadmin.html',login_user=cur_user.username,domains=domains,domain_status=domain_status,project=project)

'''
创建域名信息
'''
@cdn_blueprint.route('/domain/create/',methods=['POST','GET'])                               #将url path=/users/的get请求交由users函数处理
def create_domain():
    domain_status = [(0,"已停用"),(1,"使用中")]
    cdn_names = [("网宿","网宿"),("快网","快网")]
    projects = []
    pros = Project.query.all()
    for pro in pros:
        projects.append((pro.id,pro.project_name))
    return render_template('domain_create.html',domain_status=domain_status,projects=projects,cdn_names=cdn_names)


def check_domain(cname,domain):
    check_domain_isexists = Domain.query.filter_by(domain_name=domain).filter_by(cname=cname).all()
    if len(check_domain_isexists)==0:
        return (True,u'添加项目成功!')
    else:
        return (False,u'项目已经存在!')

'''
新增域名信息
'''
@cdn_blueprint.route('/domain/add/',methods=['POST','GET'])                               #将url path=/users/的get请求交由users函数处理
def add_domain():
    cname = request.form.get('cdn_name','')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status_id','')
    purpose = request.form.get('purpose')
    domain = request.form.get('domain')
    project_id = request.form.get('project_id')
    _is_ok, _error = check_domain(cname,domain)
    if not start_date:
        start_date = datetime.datetime.now()
    if not end_date:
        end_date = datetime.datetime.now()
    if _is_ok:
        new_project = Domain()
        new_project.cname = cname
        new_project.start_date = start_date
        new_project.end_date = end_date
        new_project.status = status
        new_project.purpose = purpose
        new_project.domain_name = domain
        new_project.project_id = project_id
        db.session.add(new_project)
        db.session.commit()
    return json.dumps({'is_ok' : _is_ok, 'errors' : _error, 'success' : '添加成功'})


'''
删除资产信息
'''

@cdn_blueprint.route('/domain/delete/', methods=['GET'])
def delete_domain():
    pid = request.args.get('id')
    domain = Domain.query.filter_by(id=pid).first()
    #print domain
    db.session.delete(domain)
    db.session.commit()
    flash('删除域名成功!',category='success')
    return redirect(url_for('cdn.domainadmin'))

'''
更新域名信息
'''
@cdn_blueprint.route('/domain/update/',methods=['POST','GET'])                               #将url path=/users/的get请求交由users函数处理
def update_domain():
    domain_status = [(0,"已停用"),(1,"使用中")]
    cdn_names = [("网宿","网宿"),("快网","快网")]
    projects = []
    pros = Project.query.all()
    for pro in pros:
        projects.append((pro.id,pro.project_name))
    return render_template('domain_update.html',domain_status=domain_status,projects=projects,cdn_names=cdn_names)

'''
接受前端js提交过来的id，回显整条数据信息
'''
@cdn_blueprint.route('/getdomaininfo/<id>')
def get_domain_by_id(id):
    _rt = {}
    domain= Domain.query.filter_by(id=id).first()
    if domain:
        _rt['id'] = domain.id
        _rt['cname'] = domain.cname
        _rt['start_date'] = domain.start_date
        _rt['end_date'] = domain.end_date
        _rt['status'] = domain.status
        _rt['purpose'] = domain.purpose
        _rt['project_id'] = domain.project_id
        _rt['domain_name'] = domain.domain_name
        return json.dumps(_rt,cls=ComplexEncoder)
    else:
        pass


'''
检查修改后的域名是否已经存在于数据库中，且id不为当前id。即域名重复
1、修改后的域名在数据库存在，且id不一致，提示域名不能重复
2、修改后的域名在数据库存在，id一致，没问题
3、修改后的域名在数据库不存在，没问题
4、同一个域名可能既在网宿使用，也可能在快网使用(比如 反恐网宿在用，快网备用状态，切换时修改CNAME就行)
'''
def get_current_domain_id(cname,domain):
    check_domain_isexists = Domain.query.filter_by(domain_name=domain).filter_by(cname=cname).first()
    #domain_id = check_domain_isexists.id
    try:
        #如果根据修改后的域名查不到记录
        check_domain_isexists.id
    except AttributeError:
        return (True,u'修改域名成功!')
        #如果根据修改后的域名查到了记录，则后续进行判断是否是同一个记录。不同记录有问题
    else:
        domain_id = check_domain_isexists.id
        return (True,domain_id)

'''
修改域名信息
'''
@cdn_blueprint.route('/domain/modify/',methods=['POST','GET'])
def modify_domain():
    #print request.form
    pid =  request.form.get('id','')
    cname = request.form.get('cdn_name','')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status_id','')
    purpose = request.form.get('purpose')
    domain = request.form.get('domain')
    project_id = request.form.get('project_id')
    rt_status,cur_id = get_current_domain_id(cname,domain)
    #print pid
    #print rt_status,cur_id
    if cur_id == '修改域名成功!':
         _is_ok,_error = (True,u'修改域名成功!')
    else:
        if cur_id == int(pid):
            _is_ok,_error =  (True,u'修改域名成功!')
        else:
            _is_ok,_error =  (False,u'域名已经存在!')
    if not start_date:
        start_date = datetime.datetime.now()
    if not end_date:
        end_date = datetime.datetime.now()
    #print _is_ok,_error
    if _is_ok:
        new_project = Domain.query.filter_by(id=pid).update(
            {
            "cname":cname,
            "start_date":start_date,
            "end_date":end_date,
            "status":status,
            "purpose":purpose,
            "domain_name":domain,
            "project_id":project_id
            }
        )
        db.session.commit()
    return json.dumps({'is_ok' : _is_ok, 'errors' : _error, 'success' : '修改成功'})

@cdn_blueprint.route('/projectamdin/')
def projectadmin():
    cur_user = get_current_user()
    projects = Project.query.all()
    return render_template('projectadmin.html',login_user=cur_user.username,projects=projects)

@cdn_blueprint.route('/priceinfo/')
def priceinfo():
    cur_user = get_current_user()
    prices = Charge_info.query.all()
    return render_template('priceinfo.html',login_user=cur_user.username,prices=prices)

def check_projectname(projectname):
    if len(projectname)<30:
        return (True,u'添加项目成功!')
'''
新建项目
'''
@cdn_blueprint.route('/project/add/', methods=['POST'])          #将url path=/user/add的post请求交由add_user处理
def add_project():
    projectname = request.form.get('projectname', '')
       #检查用户信息
    _is_ok, _error = check_projectname(projectname)

    if _is_ok:
        new_project = Project()
        new_project.project_name = projectname
        db.session.add(new_project)
        db.session.commit()
    return json.dumps({'is_ok':_is_ok, "error":_error})

'''
修改项目
'''
@cdn_blueprint.route('/project/update/', methods=['POST'])          #将url path=/user/add的post请求交由add_user处理
def update_project():
    projectid = request.form.get('id', '')
    #获取表单上的项目名称projectname
    projectname = request.form.get('projectname','')
    pro = Project.query.filter_by(id=projectid).one()
    #从数据库查询原始项目名称new_projectname
    new_projectname = pro.project_name
    check_projectname_isexists = Project.query.filter_by(project_name=projectname).all()
    #如果查询当前填入的项目名称存在数据库当中，且修改了项目名称，则提示项目名称已经存在。
    if check_projectname_isexists and not projectname == new_projectname :
        return json.dumps({'is_ok':False, "error":'修改的项目名已存在，操作失败!'})
    if projectname == new_projectname:
        return json.dumps({'is_ok':False, "error":'项目名称没有变化!'})
    else:
        Project.query.filter_by(id=projectid).update({'project_name':projectname})
        db.session.commit()
        return json.dumps({'is_ok':True, "error":'修改成功!'})

@cdn_blueprint.route('/project/delete/', methods=['GET'])
def delete_project():
    pid = request.args.get('id')
    pro = Project.query.filter_by(id=pid).first()
    #print pro
    db.session.delete(pro)
    db.session.commit()
    flash('删除项目成功!',category='success')
    return redirect(url_for('cdn.projectadmin'))


@cdn_blueprint.route('/userinfo/')
def userinfo():
    cur_user = get_current_user()
    project_list = []
    print cur_user.username
    status_dic = {1:'使用中',0:'已停用'}
    user = User.query.filter_by(username=cur_user.username).first()
    for x in user.projects.all():
        project_list.append(x.project_name)
    return render_template('userinfo.html',login_user=cur_user.username,user=user,project_list=project_list,status_dic=status_dic)

@cdn_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)

    permission = Permission(UserNeed(post.user.id))
    print permission.can()

    # We want admins to be able to edit any post
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('.post', post_id=post.id))

        form.text.data = post.text

        return render_template('edit.html', form=form, post=post)

    abort(403)
if __name__ == '__main__':
    print get_price()
