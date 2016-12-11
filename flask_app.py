'''
Created on 2016年7月12日

@author: heguofeng
'''
#!/usr/bin/env python    
import datetime    
import flask    
import gevent

from rooms import room,rooms

app = flask.Flask(__name__,static_url_path="")    
app.secret_key = 'asdf'    
myRooms=rooms(100)

def event_stream(roomid):    
    r=myRooms.getroom(roomid)
    while(True):
        message,index=r.getmessage()
        if(len(message)>0):
            print("event_stream #1")
            yield 'data: %s\n\n' % message  
            #gevent.sleep(0.5)
            print("event_stream #2 delete")
            r.delmessage(index)

 
@app.route('/login', methods=['GET', 'POST'])    
def login():    
    if flask.request.method == 'POST':    
        froomid=flask.request.form['room']
        fuser=flask.request.form['user']
        flask.session['user'] =  fuser 
        flask.session['room'] =  froomid
        #print(flask.session)
        myRooms.subscribe(roomid=froomid,user=fuser)
        return flask.redirect('/')    
    return '<form action="/login" method="post">user: <input type=text name="user">room: <input type="text" name="room"><input type="submit" value="Submit"></form>'    
 
@app.route('/post', methods=['POST'])    
def post():    
    fmessage = flask.request.form['message']    
    fuser = flask.session.get('user', 'anonymous')    
    froom= flask.session.get('room', 'chat') 

    now =  datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")    
    r=myRooms.getroom(froom)
    message=""
    message=message.join((now," ",fuser,":",fmessage))
    
    r.publish(message)
    print(r.getmessage()) 
    return flask.Response(status=204)    
 
@app.route('/stream')    
def stream():    
    print(flask.session)
    froom=flask.session.get('room','chat')

    return flask.Response(event_stream(froom),    
                          mimetype="text/event-stream")    
 
@app.route('/')    
def home():    
    if 'user' not in flask.session:    
        return flask.redirect('/login')    
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
        
     """ % flask.session['user']    
 
if __name__ == '__main__':    
    app.debug = True    
    app.run(host='0.0.0.0', port=80, threaded=True)  