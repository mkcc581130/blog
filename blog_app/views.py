# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.template import Context
from models import UserForm, ArticleForm, CommentForm, ReplyForm, ImgUploadForm
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
import pytz
import datetime
# Create your views here.


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
    if id:
        art = []
        readtotal = 0
        comtotal = 0
        month = ('一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二')
        c4 = ArticleForm.objects.filter(userid=id)
        for i in c4:
            readtotal = readtotal + i.artread
            comtotal = comtotal + i.artcom
        if artid:
            com = []
            c5 = ArticleForm.objects.get(id=artid)
            c6 = CommentForm.objects.filter(artid=artid)
            c7 = ReplyForm.objects.filter(artid=artid)
            c5.artread = c5.artread + 1
            c5.save()
            for j in c6:
                q = UserForm.objects.get(id=j.userid)
                w = ReplyForm.objects.filter(replyfirst=j.id)
                sec = []
                if w:
                    for k in w:
                        wq = UserForm.objects.get(id=k.userid)
                        sec.append({
                            'id': k.id,
                            'name': wq.username,
                            'comuserid': str(k.userid).encode("utf8"),
                            'logo': wq.userlogo,
                            'secondcom': k.commentcontent,
                            'comtime': commonday(k.commenttime),
                        })
                com.append({
                    'id': j.id,
                    'name': q.username,
                    'comuserid': str(j.userid).encode("utf8"),
                    'logo': q.userlogo,
                    'firstcom': j.commentcontent,
                    'comtime': commonday(j.commenttime),
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
                'ownerid': str(id).encode("utf8"),
                'artid': str(artid).encode("utf8"),
                'com': com,
            })
            if 'username' in request.session:
                c0 = UserForm.objects.get(username=request.session['username'])
                if c0.password == request.session['password']:
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
                        'ownerid': str(id).encode("utf8"),
                        'userid': str(c0.id).encode("utf8"),
                        'artid': str(artid).encode("utf8"),
                        'com': com,
                        'comtotal': comtotal,
                    })
        else:
            for i in c4:
                art.append({
                    'y': i.artlastedittime.strftime('%Y'),
                    'm': month[int(i.artlastedittime.strftime('%m')) - 1],
                    'd': i.artlastedittime.strftime('%d'),
                    'title': i.arttitle,
                    'content': i.artabstract,
                    'artid': str(i.id).encode("utf8"),
                    'read': i.artread,
                    'com': i.artcom,
                })
            c = Context({
                'autologin': False,
                'arttotal': len(c4),
                'readtotal': readtotal,
                'userid': '10000',
                'art': art,
                'webuser': UserForm.objects.get(id=id).username,
                'ownerid': str(id),
                'artid': str(artid).encode("utf8"),
                'comtotal': comtotal,

            })
            if 'username' in request.session:
                c0 = UserForm.objects.get(username=request.session['username'])
                if c0.password == request.session['password']:
                    c = Context({
                        'autologin': True,
                        'username': c0.username,
                        'userid': str(c0.id).encode("utf8"),
                        'userlogo': c0.userlogo,
                        'email': c0.email,
                        'intr': c0.intr,
                        'arttotal': len(c4),
                        'readtotal': readtotal,
                        'art': art,
                        'webuser': UserForm.objects.get(id=id).username,
                        'owner': str(c0.id) == str(id),
                        'ownerid': str(id).encode("utf8"),
                        'artid': artid,
                        'comtotal': comtotal,
                    })
    else:
        if method == 'web':
            c12 = ArticleForm.objects.filter(classify=0)
            tt = 'web前端'
            ti = 'web'
        elif method == 'linux':
            c12 = ArticleForm.objects.filter(classify=1)
            tt = 'linux'
            ti = 'linux'
        elif method == 'python':
            c12 = ArticleForm.objects.filter(classify=2)
            tt = 'python'
            ti = 'python'
        elif method == 'other':
            c12 = ArticleForm.objects.filter(classify=3)
            tt = '其他'
            ti = 'qita'
        else:
            c12 = ArticleForm.objects.all()
            tt = '全部文章'
            ti = 'quanbu'
        artall = []
        for i in c12:
            a = UserForm.objects.get(id=i.userid)
            classify = ['web前端', 'linux', 'python', '其他']
            artall.append({
                'un': a.username,
                'ul': a.userlogo,
                'ui': a.id,
                'title': i.arttitle,
                'time': commonday(i.artlastedittime),
                'r': i.artread,
                'a': i.artabstract,
                'c': classify[i.classify],
                'aid': i.id,
            })

        c = Context({
            'artall': artall,
            'tt': tt,
            'ti': ti,
        })
        if 'username' in request.session:
            c0 = UserForm.objects.get(username=request.session['username'])
            if c0.password == request.session['password']:
                c = Context({
                    'artall': artall,
                    'tt': tt,
                    'ti': ti,
                    'autologin': True,
                    'username': c0.username,
                    'userid': str(c0.id).encode("utf8"),
                    'userlogo': c0.userlogo,
                    'email': c0.email,
                    'intr': c0.intr,
                })
    if request.method == "POST":
        if method == 'login':
            # form = LoginForm(request.POST)
            # if form.is_valid():
            #     user = form.cleaned_data['username']
            #     password = form.cleaned_data['password']
            user = request.POST['username']
            password = request.POST['password']
            if UserForm.objects.filter(username=user):
                c1 = UserForm.objects.get(username=user)
            elif UserForm.objects.filter(email=user):
                c1 = UserForm.objects.get(email=user)
            else:
                c1 = ''
                return JsonResponse({'r': False, 'passresult': True})
            if c1:
                if c1.password == password:
                    request.session['username'] = c1.username
                    request.session['password'] = c1.password
                    try:
                        request.POST['checkbox']
                    except:
                        request.session.set_expiry(0)
                    c1.lastlogintime = datetime.datetime.now()
                    c1.lastloginIP = request.META['REMOTE_ADDR']
                    c1.save()
                    return JsonResponse({'r': True, 'passresult': True, 'userid': c1.id})
                else:
                    return JsonResponse({'r': True, 'passresult': False})
        if method == 'reg':
            if 'remail' in request.POST:
                if UserForm.objects.filter(email=request.POST['remail']):
                    return JsonResponse({'r': False, })
                else:
                    return JsonResponse({'r': True, })
            else:
                ip = request.META['REMOTE_ADDR']
                nowtime = datetime.datetime.now()
                c1 = UserForm(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'], createIP=ip, createtime=nowtime, lastlogintime=nowtime, lastloginIP=ip)
                c1.save()
                request.session['username'] = request.POST['username']
                request.session['password'] = request.POST['password']
                return JsonResponse({'r': True, })
        if method == 'logout':
            del request.session['username']
            del request.session['password']
            return JsonResponse({'r': True, })
        if method == 'comment':
            c2 = UserForm.objects.get(username=request.session['username'])
            c3 = ArticleForm.objects.get(id=artid)
            c3.artcom = c3.artcom + 1
            c3.save()
            if request.POST['dataid']:
                ReplyForm(userid=c2.id, artid=artid, commenttime=datetime.datetime.now(),
                                  commentcontent=request.POST['comcon'],replyfirst=int(request.POST['dataid'])).save()
            else:
                CommentForm(userid=c2.id, artid=artid, commenttime=datetime.datetime.now (),
                                  commentcontent=request.POST['comcon']).save()
            return JsonResponse({'r': True, })
        if method == 'delcom':
            if request.POST['com'] == 'first':
                CommentForm.objects.get(id=int(request.POST['dataid'])).delete()
                a1 = ArticleForm.objects.get(id=artid)
                b1 = ReplyForm.objects.filter(replyfirst=int(request.POST['dataid']))
                if b1:
                    a1.artcom = a1.artcom - 1 - len(b1)
                    b1.delete()
                    a1.save()
                else:
                    a1.artcom = a1.artcom - 1
                    a1.save()

                return JsonResponse({'r': True, })
            elif request.POST['com'] == 'second':
                ReplyForm.objects.get(id=int(request.POST['dataid'])).delete()
                a1 = ArticleForm.objects.get(id=artid)
                a1.artcom = a1.artcom - 1
                a1.save()
                return JsonResponse({'r': True, })
        if method == 'change':
            c2 = UserForm.objects.get(username=request.session['username'])
            if 'cemail' in request.POST:
                if UserForm.objects.filter(email=request.POST['cemail']):
                    return JsonResponse({'r': False, })
                else:
                    return JsonResponse({'r': True, })
            elif 'cpass' in request.POST:
                if request.POST['cpass'] == c2.password:
                    return JsonResponse({'r': True, })
                else:
                    return JsonResponse({'r': False, })
            else:
                if request.POST['email']:
                    c2.email = request.POST['email']
                    c2.save()
                if request.POST['password']:
                    request.session['password'] = request.POST['password']
                    c2.password = request.POST['password']
                    c2.save()
                if request.POST['intr']:
                    c2.intr = request.POST['intr']
                    c2.save()
                if'userlogo' in request.FILES:
                    c2.userlogo = request.FILES['userlogo']
                    c2.save()
                return redirect('index', c2.id, '')
        if method == 'edit':
            if 'artid' in request.POST:
                c10 = ArticleForm.objects.get(id=int(request.POST['artid']))
                return JsonResponse({
                    't': c10.arttitle,
                    'c': c10.artcontent,
                    'k': c10.artkeyword,
                    'a': c10.artabstract,
                    'cl': c10.classify,
                    'r': True
                })
            else:
                c2 = UserForm.objects.get(username=request.session['username'])
                if request.POST['id'] != '0':
                    c10 = ArticleForm.objects.get(id=int(request.POST['id']))
                    c10.arttitle = request.POST['title']
                    c10.artkeyword = request.POST['key']
                    c10.artcontent = request.POST['content']
                    c10.artabstract = request.POST['ab']
                    c10.classify = int(request.POST['c'])
                    c10.artlastedittime = datetime.datetime.now()
                    c10.save()
                    return JsonResponse({'r': True, })
                else:
                    now = datetime.datetime.now()
                    ArticleForm(userid=c2.id,arttitle=request.POST['title'],artkeyword=request.POST['key'],
                                artcontent=request.POST['content'],artcreatetime=now,artlastedittime=now,
                                artabstract=request.POST['ab'],classify=int(request.POST['c'])).save()
                    return JsonResponse({'r': True, })
        if method == 'artdel':
            artdelid = int(request.POST['artid'])
            c13 = ArticleForm.objects.get(id=artdelid)
            ui = str(c13.userid)
            c13.delete()
            CommentForm.objects.filter(artid=artdelid).delete()
            ReplyForm.objects.filter(artid=artdelid).delete()
            return JsonResponse({'r': True, 'ui': ui})
        if method == 'upload':
            c11 = ImgUploadForm(img=request.FILES[0]).save()
            return HttpResponse (c11.img)
    return render(request, url + '.html', c)


@ensure_csrf_cookie
def index(request, id, method):
    return demo('index', request, id, '', method)


@ensure_csrf_cookie
def all_articles(request, method):
    return demo('all_articles', request, '', '', method)


@ensure_csrf_cookie
def article(request, id, artid, method):
    return demo('article', request, id, artid, method)
