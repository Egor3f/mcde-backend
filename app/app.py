import hashlib
import os
import time
from datetime import timedelta
from functools import wraps

from docker.models.containers import Container
from flask import Flask, render_template, jsonify, redirect, request, abort, session
from flask_cors import CORS
from flask_sessionstore import sessions
from redis import Redis

import utils
from secrets import PASS_HASH, CURRENT_LOGTOK

app = Flask(__name__)
redis = Redis(os.environ.get('REDIS_HOST'))
app.config['SESSION_TYPE'] = 'redis'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=2)
app.config['SESSION_REDIS'] = redis
CORS(app)


class MySessionInterface(sessions.RedisSessionInterface):
    def open_session(self, app, request):
        sid = request.args.get('sid', '')
        if len(sid) > 0:
            val = self.redis.get(self.key_prefix + sid)
            if val is not None:
                try:
                    data = self.serializer.loads(val)
                    return self.session_class(data, sid=sid)
                except:
                    return self.session_class(sid=sid, permanent=self.permanent)
        return super().open_session(app, request)

app.session_interface = MySessionInterface(redis, 'mcde_session:', False, True)


def protect_bruteforce(antibrute_requests=5, antibrute_timeout=15 * 60, prefix='mcde_redis_anti_bruteforce:'):
    def innerDecorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            ip = request.remote_addr
            redis.rpush(prefix + ip, int(time.time()))

            if redis.llen(prefix + ip) > antibrute_requests:
                last_timestamp = int(redis.lpop(prefix + ip))
                if time.time() - last_timestamp < antibrute_timeout:
                    abort(429)

            return func(*args, **kwargs)
        return inner

    return innerDecorator


@protect_bruteforce()
def check_password(pwd: str):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest() == PASS_HASH


def protect(render_login_page=False):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if session.get('logtok', '') == CURRENT_LOGTOK:
                return func(*args, **kwargs)
            else:
                if 'password' in request.form and check_password(request.form.get('password')):
                    session['logtok'] = CURRENT_LOGTOK
                    return redirect(request.url)
                if render_login_page:
                    return render_template('login.html')
                else:
                    abort(401)
        return inner
    return decorator


@app.route('/', methods=['GET', 'POST'])
@protect(True)
def index():
    return render_template('index.html')


@app.route('/api/open-container')
@protect()
def open_container():
    host = request.args.get('host')
    port = int(request.args.get('port'))
    return redirect(f'http://s{session.sid}.h{host}.p{port}.cont.{request.host}')


@app.route('/api/containers')
@protect()
def list_containers():
    return jsonify(utils.serializeObjectListAttrs(utils.getDockerClient().containers.list(True), 'name', 'status', 'ports'))


@app.route('/api/container/<name>/power/<command>')
@protect()
def power_command(name, command):
    ALLOWED_COMMANDS = ['start', 'stop', 'restart']
    if command not in ALLOWED_COMMANDS:
        abort(400)
    container: Container = utils.getDockerClient().containers.get(name)
    getattr(container, command)()
    return 'Ok'


@app.route('/api/auth')
@protect()
def auth_session():
    return '1'


if __name__ == '__main__':
    app.run()
