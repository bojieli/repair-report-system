#!/usr/bin/env python3
from app import app
from app import db
from random import randint

debug = True

def start():
    if debug:
        db.create_all()
    app.run(host="0.0.0.0",port=8080)



if __name__ == '__main__':
    start()
