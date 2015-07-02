from flask import Blueprint,jsonify,request, Markup
from app.utils import rand_str, handle_upload
from app import app
import re

api = Blueprint('api',__name__)

def generic_upload(file, type):
    ok,message = handle_upload(file, type)
    script_head = '<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction(2,'
    script_tail = ');</script>'
    if ok:
        url = '/uploads/' + type + 's/' + message
        return script_head + '"' + url + '"' + script_tail
    else:
        return script_head + '""' + ',' + '"' + message + '"' + script_tail

@api.route('/upload/image',methods=['POST'])
@app.csrf.exempt
def upload_image():
    return generic_upload(request.files['upload'], 'image')

@api.route('/upload/file', methods=['POST'])
@app.csrf.exempt
def upload_file():
    return generic_upload(request.files['upload'], 'file')

