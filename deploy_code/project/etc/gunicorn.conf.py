import os

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_VAR = os.path.join(_ROOT, "var")
_ETC = os.path.join(_ROOT, "etc")

loglevel = "info"
errorlog = os.path.join(_VAR, "log/flask-error.log")
accesslog = os.path.join(_VAR, "log/flask-access.log")

bind = "0.0.0.0:5000"
workers = 4

timeout = 3 * 60
keepalive = 24 * 60 * 60

capture_output = True