# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.template import Context
from models import UserForm, ArticleForm, CommentForm, ReplyForm
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password, check_password
import pytz
import datetime
# Create your views here.


# 改变时间样式
def commonday(date):
    tz = pytz.timezone(pytz.country_timezones('cn')[0])
    nowtime = datetime.datetime.now(tz)
    n = (nowtime-date).days
    if n == 0:
        s = (nowtime - date).seconds
        if s < 60:
            return str(s) + '秒前'
        elif s < 3600:
            return str(s/60) + '分钟前'
        else:
            return str(s/3600) + '小时前'
    elif n == 1:
        return '昨天 ' + date.strftime('%H:%M')
    elif n == 2:
        return '前天 ' + date.strftime('%H:%M')
    else:
        return date.strftime('%m') + '-' + date.strftime('%d')


def demo(url, request, id, artid, method):
    c = Context({})
    # 设置模板变量
    if id:  # 判断是不是全部文章页
        art = []
        readtotal = 0
        comtotal = 0
        month = ('一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二')
        c4 = ArticleForm.objects.filter(userid=id).values_list('id','arttitle','artabstract','artread','artcom','artlastedittime')
        for i in c4:
            readtotal = readtotal + i[3]
            comtotal = comtotal + i[4]
        if artid:  # 判断是不是详细文章页
            com = []
            c5 = ArticleForm.objects.only('artread', 'artlastedittime', 'arttitle', 'artcontent', 'artkeyword').get(id=artid)
            c6 = CommentForm.objects.filter(artid=artid).values_list('id', 'userid', 'commentcontent', 'commenttime')
            c7 = ReplyForm.objects.only('id').filter(artid=artid)
            c5.artread = c5.artread + 1
            c5.save()
            for j in c6:
                q = UserForm.objects.only('username', 'userlogo').get(id=j[1])
                w = ReplyForm.objects.filter(replyfirst=j[0]).values_list('id', 'userid', 'commentcontent', 'commenttime')
                sec = []
                if w:
                    for k in w:
                        wq = UserForm.objects.only('username', 'userlogo').get(id=k[1])
                        sec.append({
                            'id': k[0],
                            'name': wq.username,
                            'comuserid': str(k[1]),
                            'logo': wq.userlogo,
                            'secondcom': k[2],
                            'comtime': commonday(k[3]),
                        })
                com.append({
                    'id': j[0],
                    'name': q.username,
                    'comuserid': str(j[1]),
                    'logo': q.userlogo,
                    'firstcom': j[2],
                    'comtime': commonday(j[3]),
                    'second': sec,
                })
            artc = {
                'y': c5.artlastedittime.strftime('%Y'),
                'm': month[int(c5.artlastedittime.strftime('%m')) - 1],
                'd': c5.artlastedittime.strftime('%d'),
                'title': c5.arttitle,
                'content': c5.artcontent,
                'key': c5.artkeyword,
                'read': c5.artread,
                'artcom': len(c6)+len(c7),
            }
            c = Context({
                'autologin': False,
                'arttotal': len(c4),
                'readtotal': readtotal,
                'comtotal': comtotal,
                'userid': '10000',
                'art': artc,
                'webuser': UserForm.objects.get(id=id).username,
                'ownerid': str(id),
                'artid': str(artid),
                'com': com,
            })
            if 'username' in request.session:  # 判断session里是否有用户信息
                c0 = UserForm.objects.only('id', 'username', 'password', 'userlogo', 'email', 'intr').get(username=request.session['username'])
                if request.session['password'] == c0.password:   # 判断密码是否正确
                    c = Context({
                        'autologin': True,
                        'username': c0.username,
                        'userlogo': c0.userlogo,
                        'email': c0.email,
                        'intr': c0.intr,
                        'arttotal': len(c4),
                        'readtotal': readtotal,
                        'art': artc,
                        'webuser': UserForm.objects.get(id=id).username,
                        'owner': str(c0.id) == str(id),
                        'ownerid': str(id),
                        'userid': str(c0.id),
                        'artid': str(artid),
                        'com': com,
                        'comtotal': comtotal,
                    })
        else:
            for i in c4:
                art.append({
                    'y': i[5].strftime('%Y'),
                    'm': month[int(i[5].strftime('%m')) - 1],
                    'd': i[5].strftime('%d'),
                    'title': i[1],
                    'content': i[2],
                    'artid': str(i[0]),
                    'read': i[3],
                    'com': i[4],
                })
            c = Context({
                'autologin': False,
                'arttotal': len(c4),
                'readtotal': readtotal,
                'userid': '10000',
                'art': art,
                'webuser': UserForm.objects.get(id=id).username,
                'ownerid': str(id),
                'artid': str(artid),
                'comtotal': comtotal,

            })
            if 'username' in request.session:  # 判断session里是否有用户信息
                c0 = UserForm.objects.only('id', 'username', 'password', 'userlogo', 'email', 'intr').get(username=request.session['username'])
                if request.session['password'] == c0.password:   # 判断密码是否正确
                    c = Context({
                        'autologin': True,
                        'username': c0.username,
                        'userid': str(c0.id),
                        'userlogo': c0.userlogo,
                        'email': c0.email,
                        'intr': c0.intr,
                        'arttotal': len(c4),
                        'readtotal': readtotal,
                        'art': art,
                        'webuser': UserForm.objects.get(id=id).username,
                        'owner': str(c0.id) == str(id),
                        'ownerid': str(id),
                        'artid': artid,
                        'comtotal': comtotal,
                    })
    else:
        # 各个分类的文章列表页
        if method == 'web':
            c12 = ArticleForm.objects.filter(classify=0).values_list('id', 'userid', 'arttitle', 'artabstract', 'artread', 'artlastedittime', 'classify')
            tt = 'web前端'
            ti = 'web'
        elif method == 'linux':
            c12 = ArticleForm.objects.filter(classify=1).values_list('id', 'userid', 'arttitle', 'artabstract', 'artread', 'artlastedittime', 'classify')
            tt = 'linux'
            ti = 'linux'
        elif method == 'python':
            c12 = ArticleForm.objects.filter(classify=2).values_list('id', 'userid', 'arttitle', 'artabstract', 'artread', 'artlastedittime', 'classify')
            tt = 'python'
            ti = 'python'
        elif method == 'other':
            c12 = ArticleForm.objects.filter(classify=3).values_list('id', 'userid', 'arttitle', 'artabstract', 'artread', 'artlastedittime', 'classify')
            tt = '其他'
            ti = 'qita'
        else:
            c12 = ArticleForm.objects.all().values_list('id', 'userid', 'arttitle', 'artabstract', 'artread', 'artlastedittime', 'classify')
            tt = '全部文章'
            ti = 'quanbu'
        artall = []
        for i in c12:
            a = UserForm.objects.only('id', 'username', 'userlogo').get(id=i[1])
            classify = ['web前端', 'linux', 'python', '其他']
            artall.append({
                'un': a.username,
                'ul': a.userlogo,
                'ui': a.id,
                'title': i[2],
                'time': commonday(i[5]),
                'r': i[4],
                'a': i[3],
                'c': classify[i[6]],
                'aid': i[0],
            })

        c = Context({
            'artall': artall,
            'tt': tt,
            'ti': ti,
        })
        if 'username' in request.session:  # 判断session里是否有用户信息
            c0 = UserForm.objects.only('id', 'username', 'password', 'userlogo', 'email', 'intr').get(username=request.session['username'])
            if request.session['password'] == c0.password:   # 判断密码是否正确
                c = Context({
                    'artall': artall,
                    'tt': tt,
                    'ti': ti,
                    'autologin': True,
                    'username': c0.username,
                    'userid': str(c0.id),
                    'userlogo': c0.userlogo,
                    'email': c0.email,
                    'intr': c0.intr,
                })
    #判断请求
    if request.method == "POST":  # 判断上传方式是否为POST
        if method == 'login':   # 登录处理
            user = request.POST['username']
            password = request.POST['password']
            if UserForm.objects.filter(username=user):
                c1 = UserForm.objects.only('id', 'username', 'password', 'lastlogintime', 'lastloginIP').get(username=user)
            elif UserForm.objects.filter(email=user):
                c1 = UserForm.objects.only('id', 'username', 'password', 'lastlogintime', 'lastloginIP').get(email=user)
            else:
                c1 = ''
                return JsonResponse({'r': False, 'passresult': True})
            if c1:
                if check_password(password, c1.password):   # 判断密码是否正确
                    request.session['username'] = c1.username
                    request.session['password'] = c1.password
                    try:   # 判断7天自动登录是否选中
                        request.POST['checkbox']
                    except:
                        request.session.set_expiry(0)
                    c1.lastlogintime = datetime.datetime.now()
                    c1.lastloginIP = request.META['REMOTE_ADDR']
                    c1.save()
                    return JsonResponse({'r': True, 'passresult': True, 'userid': c1.id})
                else:
                    return JsonResponse({'r': True, 'passresult': False})
        if method == 'reg':   # 注册处理
            if 'remail' in request.POST:   # 验证邮箱是否存在
                if UserForm.objects.filter(email=request.POST['remail']):
                    return JsonResponse({'r': False, })
                else:
                    return JsonResponse({'r': True, })
            else:
                ip = request.META['REMOTE_ADDR']
                nowtime = datetime.datetime.now()
                password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
                c1 = UserForm(username=request.POST['username'], password=password, email=request.POST['email'], createIP=ip, createtime=nowtime, lastlogintime=nowtime, lastloginIP=ip)
                c1.save()
                request.session['username'] = request.POST['username']
                request.session['password'] = password
                return JsonResponse({'r': True, })
        if method == 'logout':   # 登出处理
            del request.session['username']
            del request.session['password']
            return JsonResponse({'r': True, })
        if method == 'comment':   # 评论处理
            c2 = UserForm.objects.only('id').get(username=request.session['username'])
            c3 = ArticleForm.objects.only('artcom').get(id=artid)
            c3.artcom = c3.artcom + 1
            c3.save()
            if request.POST['dataid']:
                ReplyForm(userid=c2.id, artid=artid, commenttime=datetime.datetime.now(),
                                  commentcontent=request.POST['comcon'],replyfirst=int(request.POST['dataid'])).save()
            else:
                CommentForm(userid=c2.id, artid=artid, commenttime=datetime.datetime.now (),
                                  commentcontent=request.POST['comcon']).save()
            return JsonResponse({'r': True, })
        if method == 'delcom':   # 删除评论处理
            if request.POST['com'] == 'first':   # 删除评论及全部回复
                CommentForm.objects.only('id').get(id=int(request.POST['dataid'])).delete()
                a1 = ArticleForm.objects.only('artcom').get(id=artid)
                b1 = ReplyForm.objects.only('id').filter(replyfirst=int(request.POST['dataid']))
                if b1:
                    a1.artcom = a1.artcom - 1 - len(b1)
                    b1.delete()
                    a1.save()
                else:
                    a1.artcom = a1.artcom - 1
                    a1.save()

                return JsonResponse({'r': True, })
            elif request.POST['com'] == 'second':   # 删除回复
                ReplyForm.objects.only('id').get(id=int(request.POST['dataid'])).delete()
                a1 = ArticleForm.only('artcom').objects.get(id=artid)
                a1.artcom = a1.artcom - 1
                a1.save()
                return JsonResponse({'r': True, })
        if method == 'change':   # 修改用户信息处理
            username = request.session['username']
            if 'cemail' in request.POST:   # 验证邮箱是否存在
                if UserForm.objects.filter(email=request.POST['cemail']):
                    return JsonResponse({'r': False, })
                else:
                    return JsonResponse({'r': True, })
            elif 'cpass' in request.POST:   # 验证原密码是否输入正确
                c2 = UserForm.objects.only('password').get(username=username)
                if check_password(request.POST['cpass'], c2.password):
                    return JsonResponse({'r': True, })
                else:
                    return JsonResponse({'r': False, })
            else:
                if request.POST['email']:   # 修改邮箱
                    c2 = UserForm.objects.only('id', 'email').get(username=username)
                    c2.email = request.POST['email']
                    c2.save()
                if request.POST['password']:   # 修改密码
                    c2 = UserForm.objects.only('id', 'password').get(username=username)
                    pa = make_password(request.POST['password'], None, 'pbkdf2_sha256')
                    request.session['password'] = pa
                    c2.password = pa
                    c2.save()
                if request.POST['intr']:   # 修改简介
                    c2 = UserForm.objects.only('id', 'intr').get(username=username)
                    c2.intr = request.POST['intr']
                    c2.save()
                if'userlogo' in request.FILES:   # 修改头像
                    c2 = UserForm.objects.only('id', 'userlogo').get(username=username)
                    c2.userlogo = request.FILES['userlogo']
                    c2.save()
                return redirect('index', c2.id, '')
        if method == 'edit':   # 编辑文章处理
            if 'artid' in request.POST:   # 读取文章
                c10 = ArticleForm.objects.only('arttitle', 'artcontent','artkeyword', 'artabstract', 'classify').get(id=int(request.POST['artid']))
                return JsonResponse({
                    't': c10.arttitle,
                    'c': c10.artcontent,
                    'k': c10.artkeyword,
                    'a': c10.artabstract,
                    'cl': c10.classify,
                    'r': True
                })
            else:   # 编辑修改文章
                c2 = UserForm.objects.get(username=request.session['username'])
                if request.POST['id'] != '0':
                    c10 = ArticleForm.objects.only('arttitle', 'artcontent','artkeyword', 'artabstract',
                                                   'classify', 'artlastedittime').get(id=int(request.POST['id']))
                    c10.arttitle = request.POST['title']
                    c10.artkeyword = request.POST['key']
                    c10.artcontent = request.POST['content']
                    c10.artabstract = request.POST['ab']
                    c10.classify = int(request.POST['c'])
                    c10.artlastedittime = datetime.datetime.now()
                    c10.save()
                    return JsonResponse({'r': True, })
                else:  # 写新文章
                    now = datetime.datetime.now()
                    ArticleForm(userid=c2.id, arttitle=request.POST['title'], artkeyword=request.POST['key'],
                                artcontent=request.POST['content'], artcreatetime=now, artlastedittime=now,
                                artabstract=request.POST['ab'], classify=int(request.POST['c'])).save()
                    return JsonResponse({'r': True, })
        if method == 'artdel':   # 删除文章处理
            artdelid = int(request.POST['artid'])
            c13 = ArticleForm.objects.only('userid').get(id=artdelid)
            ui = str(c13.userid)
            c13.delete()
            CommentForm.objects.only('id').filter(artid=artdelid).delete()
            ReplyForm.objects.only('id').filter(artid=artdelid).delete()
            return JsonResponse({'r': True, 'ui': ui})
    return render(request, url + '.html', c)


@ensure_csrf_cookie
def index(request, id, method):   # 个人博客页
    return demo('index', request, id, '', method)


@ensure_csrf_cookie
def all_articles(request, method):   # 全部文章页
    return demo('all_articles', request, '', '', method)


@ensure_csrf_cookie
def article(request, id, artid, method):   # 文章内容页
    return demo('article', request, id, artid, method)
