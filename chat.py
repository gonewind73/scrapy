'''
Created on 2016年7月12日

@author: heguofeng
'''
#!/usr/bin/env python    
import datetime    
import flask    
import redis 
    
from rooms import room,rooms

app = flask.Flask(__name__,static_url_path="")    
app.secret_key = 'asdf'    
myRooms=rooms(100)

def event_stream(roomid):    
    #pubsub = red.pubsub()    
    #pubsub.subscribe(room)    
    # TODO: handle client disconnection.    
    #return( "data: mytest\n\n")
    r=myRooms.getroom(roomid)
    while(True):

        message=r.getmessage()
       
        if(len(message)>0):
            print("run here!")
            yield 'data: %s\n\n' % message  
            r.delmessage()
          
    '''
    while(True):
        print("run ")
        if(len(messages)>0):
            print("run here 2")
            yield 'data: %s\n\n'%messages[0]
            del messages[0]'''
    #for message in pubsub.listen():    
        #print( message)    
        #yield 'data: %s\n\n' % message['data']    
 
@app.route('/login', methods=['GET', 'POST'])    
def login():    
    if flask.request.method == 'POST':    
        print(flask.request.form)
        flask.session['user'] = flask.request.form['user']  
        flask.session['room'] = flask.request.form['room']
        print(flask.session)
        myRooms.subscribe(roomid=flask.session['room'],user=flask.session['user'])
        return flask.redirect('/')    
    return '<form action="/login" method="post">user: <input type=text name="user">room: <input type="text" name="room"><input type="submit" value="Submit"></form>'    
 
@app.route('/post', methods=['POST'])    
def post():    
    message = flask.request.form['message']    
    messages.append(message)
    user = flask.session.get('user', 'anonymous')    
    room= flask.session.get('room', 'chat') 
    print(room) 
    now = datetime.datetime.now().replace(microsecond=0).time()    
    
    red.publish(room, u'[%s] %s: %s' % (now.isoformat(), user, message))   
    r=myRooms.getroom(room)
    print(r)
    r.publish(message)
    #print(myRooms.getmessage(room)) 
    return flask.Response(status=204)    
 
@app.route('/stream')    
def stream():    
    print(flask.session)
    print("seesions")
    room=flask.session.get('room','chat')
    print(room)

    return flask.Response(event_stream(room),    
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
    app.run(host='0.0.0.0', port=8989, threaded=True)  