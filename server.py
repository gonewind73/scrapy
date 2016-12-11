'''
Created on 2016年4月10日

@author: heguofeng
'''
from flask import Flask,url_for, redirect,request,session,Response,json

from flask import render_template, flash
#from forms import LoginForm
from cloud189Disk import OAuth2, vDiskClient
import urllib
import urllib.parse
import gevent
from numpy import random
from flask_sse import sse
import redis 
import datetime 
from rooms import room,rooms

from safebox import safebook,record

'''
1\ safebox。com
2\ 输入保险箱密码,submit
3\ get 189 authority
4\ get file and decode
5\ show
6\ add-delete-modify-save
'''

app = Flask(__name__)
app.config.from_object('config')

app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

red = redis.StrictRedis(host='localhost', port=6379, db=6)  

sbook=safebook("")

myRooms=rooms(100)
messages=[]

def event_stream(room):  
    '''  
    pubsub = red.pubsub()    
    pubsub.subscribe(room)    
    # TODO: handle client disconnection.    
    for message in pubsub.listen():    
        print( message)    
        yield 'data: %s\n\n' % message['data']   '''
    while(True):
        print("run here!")
        message=myRooms.getmessage(room)
        if(len(message)>0):
            yield 'data: %s\n\n' % message  
           

@app.route('/send')
def send_message():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"

@app.route('/189')
def cloud189Disk():
    qs = request.args
    session["secret"]=qs["secret"]
    
    AppSecret="93c6a3491a5e1d93af0e44b470798148"
    AppId="600102343"
    oauth2=OAuth2(AppId,AppSecret,"http://127.0.0.1/189Callback")
    url_params = urllib.parse.urlencode(oauth2.authorize("token"))
    print(url_params)
    url=oauth2.AUTHORIZE_URL+"?"+url_params
    return  redirect(url)


def event():
    while True:
        yield 'data: ' + json.dumps(random.rand(1).tolist()) + '\n\n'
        gevent.sleep(2)


@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/189Callback')
def Callback189():
    qs = request.url
    print(qs)
    return '''  
    <script language="javascript">

    function replacearg(url){
    arg=url.replace("#","?");
    arg=arg.replace("189Callback","189Callback2")
    return arg;
    } 
    
    
    </script>
    
    <body>
   
    <script>
    
        document.write(replacearg(document.location.href));

        // 以下方式定时跳转  
        setTimeout("javascript:location.href='"+replacearg(document.location.href)+"'", 10);   
    </script> 
    </body>
    '''

@app.route('/189Callback2')
def Callback1892():
    qs = request.args
    print(qs)
    session["accessToken"]=qs["accessToken"]
    print(session)
    
    vdc=vDiskClient()
    vdc.setAccessToken(session["accessToken"])
    sbook=safebook(session["secret"])
    
    data=vdc.getFiletoData("safedata.dat")
    sbook.loadFromEncrptedBytes(data)
    print(sbook.len())
    #session["sbook"]=sbook
    records=[]
    for i in range(0,sbook.len()):
        record=sbook.get(i)
        records.append(record.getdict())
    print(records)
        
    return render_template("list.html",
        title = '密码箱',
        records = records)

@app.route('/action')
def action():
    qs = request.args
    print(qs)
    #session["accessToken"]=qs["accessToken"]
    print(session)
    
    vdc=vDiskClient()
    vdc.setAccessToken(session["accessToken"])
    sbook=safebook(session["secret"])
    
    data=vdc.getFiletoData("safedata.dat")
    sbook.loadFromEncrptedBytes(data)
    #sbook=session["sbook"]
    if qs["action"]=="增加" :
        myrecord=(sbook.getid(),"","","","","")
        re=record()
        re.set(myrecord)
        sbook.append(re)
        print(sbook.len())
        encdata=sbook.saveToEncryptByte()
        vdc.putFileFromData("safedata.dat", encdata)
    if qs["action"]=="修改":
        r=sbook.getbyid(qs["rid"])
        myrecord=(r.rid,r.tag,r.uri,r.username,r.password,r.ref)
    if qs["action"]=="删除":
        r=sbook.deletebyid(qs["rid"])
        encdata=sbook.saveToEncryptByte()
        vdc.putFileFromData("safedata.dat", encdata)
        
        records=[]
        for i in range(0,sbook.len()):
            myrecord=sbook.get(i)
            records.append(myrecord.getdict())
        print(records)
            
        return render_template("list.html",
            title = '密码箱',
            records = records) 
    
    
    print(myrecord)
        
    recorddic={"rid":myrecord[0],
                "tag":myrecord[1],
                "uri":myrecord[2],
                "username":myrecord[3],
                "password":myrecord[4],
                "ref":myrecord[5]}
    
    print(recorddic)
        
    return render_template("record.html",
        title = '密码箱',
        record= recorddic,
        action=qs["action"])

@app.route('/save')
def save():
    qs = request.args
    print(qs)
    #session["accessToken"]=qs["accessToken"]
    print(session)
    
    vdc=vDiskClient()
    vdc.setAccessToken(session["accessToken"])
    sbook=safebook(session["secret"])
    
    data=vdc.getFiletoData("safedata.dat")
    sbook.loadFromEncrptedBytes(data)
    #sbook=session["sbook"]
    re=record()
    re.set((qs["rid"],qs["tag"],qs["uri"],qs["username"],qs["password"],qs["ref"]))
    sbook.setbyid(qs["rid"], re)
    encdata=sbook.saveToEncryptByte()
    vdc.putFileFromData("safedata.dat", encdata)
        
    records=[]
    for i in range(0,sbook.len()):
        myrecord=sbook.get(i)
        records.append(myrecord.getdict())
    print(records)
        
    return render_template("list.html",
        title = '密码箱',
        records = records) 
        

    
@app.route('/safebox')
def index():
    user = { 'nickname': 'heguofeng' } # fake user
    qs = request.url
    print(qs)

    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = '主页',
        user = user,
        posts = posts)
    
@app.route('/list')
def list():
    user = { 'nickname': 'heguofeng' } # fake user
    qs = request.url
    print(qs)

    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("list.html",
        title = '主页',
        user = user,
        posts = posts)
'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
    #form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
'''


            
        
@app.route('/login', methods=['GET', 'POST'])    
def loginchannel():    
    if request.method == 'POST':    
        print(request.form)
        session['user'] = request.form['user']  
        session['room'] = request.form['room']

        print(session)
        myRooms.subscribe(roomid=session['room'],user=session['user'])
        return redirect('/')    
    return '<form action="/login" method="post">user: <input type=text name="user">room: <input type="text" name="room"><input type="submit" value="Submit"></form>'    
 
@app.route('/post', methods=['POST'])    
def post():    
    message = request.form['message']    
    user = session.get('user', 'anonymous')    
    room= session.get('room', 'chat') 
    print(room) 
    now = datetime.datetime.now().replace(microsecond=0).time()    
    #red.publish(room, u'[%s] %s: %s' % (now.isoformat(), user, message))  
    r=myRooms.getroom(room)
    print(r)
    r.publish(message)
    #print(myRooms.getmessage(room))
    #messages.append(message)
    return Response(status=204)

@app.route('/stream')    
def stream():    
    print(session)
    print("seesions")
    room=session.get('room','chat')
    print(room)

    return Response(event_stream(room),    
                          mimetype="text/event-stream")   

@app.route('/')    
def home():    
    if 'user' not in session:    
        return redirect('/login')    
    return u"""    
            <!doctype html>    
            <title>chat</title>
            <meta charset="UTF-8">
            
            <script src="http://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>    
     
            <style>body { max-width: 500px; margin: auto; padding: 
    1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; 
    }</style>    
            <p><b>hi, %s!</b></p>    
            <p>Message: <input id="in" /></p>    
            <pre id="out"></pre>    
            <script>    
                function sse() {    
                    var source = new EventSource('/stream');    
                    var out = document.getElementById('out');    
                    source.onmessage = function(e) {    
                        // XSS in chat is fun    
                        out.innerHTML =  e.data + '\\n' + out.innerHTML;    
                    };    
                }    
                $('#in').keyup(function(e){    
                    if (e.keyCode == 13) {    
                        $.post('/post', {'message': $(this).val()});    
                        $(this).val('');    
                    }    
                });    
                sse();    
            </script>    
        
     """ % session['user']    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True,threaded=True)
    
  
 
    
 

 
 
 


'''
setTimeout("javascript:location.href=replacearg(document.location.href), 5000); 
alert(replacearg(document.location.href));
'''
#return   
'''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Hello,  + user['nickname'] + '</h1>
  </body>
</html>
'''