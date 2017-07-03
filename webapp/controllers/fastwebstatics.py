#!usr/bin/env python
#coding=utf-8

import urllib2
import json
import calendar
import datetime
from pro import fastweb
import math
import sys
import commands

#获取Token公共类
class   GetToken:
    appid = 'aa83fdce98223b149506246190d0a5'
    appsecret = '268b100b8b'
    grant_type = 'client_credentials'

    def __init__(self ,appid,appsecret,grant_type = 'client_credentials'):
        self.appid = appid
        self.appsecret = appsecret
        self.grant_type = grant_type

#获取JSON格式token
    def getAccessTokenByJson(self):
        url = 'https://cdncs-api.fastweb.com.cn/oauth/access_token.json'
        data = {
            "grant_type": self.grant_type,
            "appid": self.appid,
            "appsecret": self.appsecret
        }
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
            res = response.read()
        except:
            res = ''
        return  res

#此接口用于按区间查询流量带宽，按一日为一个时间点统计数据
    def get_Range_Traffic(self,url,domains,token,start_date,end_date,data_format,show_ts=1,show_ap=1):
        self.domains = domains
        self.token = token
        self.start_date = start_date
        self.end_date = end_date
        self.data_format = data_format
        self.show_ts = show_ts
        self.show_ap = show_ap
        url = 'https://cdncs-api.fastweb.com.cn/report/get_range_traffic.json'

        data = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "show_ts": self.show_ts,
            "show_ap": self.show_ap,
            "domains": self.domains,
            "data_format":self.data_format,
            "access_token": self.token
            }

        data  = json.dumps(data)
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
            res = response.read()
        except:
            res = ''
        return res

#此接口用于按某天查询流量带宽， 按5分钟为一个时间点统计数据
    def get_Day_Traffic(self,day,domains,token,show_ts='false',show_ap='false',data_format='false'):
        self.day = day
        self.domains = domains
        self.token = token
        self.show_ts = show_ts
        self.show_ap = show_ap
        self.data_format = data_format
        url = 'https://cdncs-api.fastweb.com.cn/report/get_day_traffic.json'
        data = {
            "date": self.day,
            "domains": self.domains,
            "data_format": self.data_format,
            "show_ts": self.show_ts,
            "show_ap": self.show_ap,
            "access_token": self.token,
            }
        data  = json.dumps(data)
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
            res = response.read()
        except:
            res = ''
        return res

    #获取每月的每天，并返回列表。默认为当年当月。
    def get_every_day_of_month(self,year=None,month=None):
        count = 1
        date_list = []

        if year:
            year = int(year)
        else:
            year = datetime.date.today().year

        if month:
            month = int(month)
        else:
            month = datetime.date.today().month

        firstDayWeekDay, monthrange = calendar.monthrange(year, month)
        firstDay = datetime.datetime(year=year, month=month, day=1).strftime('%Y-%m-%d')
        while count<=monthrange:
            next_day = datetime.datetime(year=year, month=month, day=count).strftime('%Y-%m-%d')
            date_list.append(next_day)
            count += 1
        return date_list


#获取token，#因为每天获取TOKEN有次数限制，建议把下面的TOKEN保存起来，以供多个接口共同使用。
def get_token():
    ins  = GetToken('aa83fdce98223b149506246190d0a5','268b100b8b','client_credentials')
    res_json = ins.getAccessTokenByJson()
    #rt = res_json.decode("utf-8")
    rt = json.loads(res_json)
    if rt.get('info') == u'操作成功':
        return rt
    elif rt.get('info') == u'token已过期':
        print 'token已过期,再次生产token，并入库保存，确保token为最新，且每次从数据库中查询'
    elif rt.get('info') == u'未找到此用户':
        print '认证失败，请确认用户名和密码正确'
    else:
        return res_json.decode("utf-8")

#获取每个项目的流量，并写入到以项目命名的文件
def get_traffic_project(project,year,month):
    ins  = GetToken('aa83fdce98223b149506246190d0a5','268b100b8b','client_credentials')
    domains = ','.join(fastweb.project.get(project))
    token = "9aa9e4aebde165d7b83c784edde1d50d721729b1d76816532a72cfef3a41392f70238d6f6320767d823281c116e2c00961eac716760857fa2bbfb8952245243e"

    #try 运行函数，如果token异常报错，则再次生产token，并保存入库，每次从库中查询token
    #one_day_of_data = ins.get_Day_Traffic(day='2017-05-01',domains=domains,token=token,show_ts='false',show_ap='false',data_format='false')
    #获取每月的所有天数，格式为:['2017-05-01','2017-05-02'......'2017-05-31']
    every_day_of_month = ins.get_every_day_of_month(year,month)
    #获取每月所有天数的数据列表
    data_list_of_month = []

    status,rt = commands.getstatusoutput("ls %s"  %project)
    if not status:
        pass
    else:
        for day in every_day_of_month:
            try:
                cur_day_data = ins.get_Day_Traffic(day=day,domains=domains,token=token,show_ts='false',show_ap='false',data_format='false')
            except AttributeError as e:
                print e
            cur_day_data = json.loads(cur_day_data)
            data_list_of_month.append(cur_day_data.get('result').get('data_list'))
        with open(project,'w+') as f:
            f.write(json.dumps(data_list_of_month))

#获取所有带宽，并按95式计费算出计费带宽和峰值带宽
def get_result_project(project):
    rt = []
    try:
        with open(project) as f:
            for x in f.readlines():
                b=list(eval(x))
                for z in range(len(b)):
                    for y in  b[z]:
                        rt.append(y.get('bandwidth'))
    except IOError:
        print '文件不存在!'
        sys.exit()


    rt = sorted(rt,reverse=True)
    #for index,item in enumerate(rt):
    #    print index,item
    #print '峰值带宽为:%s' %rt[0]
    del_num = int(math.ceil(len(rt)*0.05))
    for i in range(1,del_num):
        rt.pop(0)
    return rt[0]
def get_statics_result():
    pj = {
    'jx1':'剑一',
    'jx3':'剑三',
    'jxsj':'剑世',
    'yy':'月影',
    'fkxd':'反恐行动',
    'all':'所有'}
    year = 2017
    month = 05
    peak = 0.0
    total = 0.0
    total_money = 0.0

    #print get_token()
    for p in fastweb.project:
        if p =='all':continue
        get_traffic_project(p,year,month)
        peak += float(get_result_project(p))
    for poo in fastweb.project:
        if poo == 'all':total=get_result_project(poo)
    #print '总计费带宽为:%s' %peak
    #print '实际计费带宽为:%s' %total
    #print '*'*60
    statics = []
    for po  in fastweb.project:
        if po == 'all':continue
        #print "%s项目在%s年-%s月的CDN计费情况" %(pj[po],year,month)
        get_traffic_project(p,year,month)
        #print '计费带宽为:%sMbps' %(get_result_project(po))
        #print '所占比例为:%.2f%%' %(get_result_project(po)/peak*100)
        #print '实际费用分摊带宽为:%.2f,费用为:%.2f元' %(get_result_project(po)/peak*total,get_result_project(po)/peak*total*16)
        total_money+=get_result_project(po)/peak*total*16
        #print '*'*60
        _rt = ('%s-%s' %(year,month),u'快网',u'下载加速',pj[po],u'中国大陆','%.2f' %(get_result_project(po)/peak*total),'%.2f' %(get_result_project(po)/peak*total*16),'%.2f%%' %(get_result_project(po)/peak*100))
        statics.append(_rt)
    return (statics,total_money)
if __name__ == '__main__':
    print get_statics_result()

