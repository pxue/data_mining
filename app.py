#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, sqlite3

from Crypto.Cipher import AES
from flask import Flask, request, g
from hashlib import md5
from binascii import hexlify, unhexlify

from presto import get_balance

PORT = int(os.environ.get("PORT", 5000))
TOKEN = str(os.environ.get("TOKEN", ""))
IV = str(os.environ.get("IV", "This is an IV456"))
DATABASE = str(os.environ.get("DB", "_presto.db"))

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g._database = db
        try:
            c = db.cursor()
            c.execute('CREATE TABLE presto (user_id text, username text, password text)')
            c.close()
        except Exception, e:
            print e
            sys.stdout.flush()
    return db

def get_encrypted(key, plaintext):
    t = AES.new(key, AES.MODE_CFB, IV)
    return hexlify(t.encrypt(plaintext))

def get_decrypted(key, ciphertext):
    t = AES.new(key, AES.MODE_CFB, IV)
    return t.decrypt(unhexlify(ciphertext))

def helper():
    return '''
    Valid commands: login, balance, (more to come)
    To login: /presto login [username] [password]
    To check your balance: /presto balance
    '''

# poor man's oauth.
def login(key, user_id, username, password):
    conn = get_db()

    cur = conn.cursor()
    cur.execute('SELECT * FROM presto WHERE user_id=?', (user_id,))
    user = cur.fetchone()
    cur.close()

    with conn:
        if not user:
            conn.execute('INSERT INTO presto (user_id, username, password) VALUES (?, ?, ?)',
                (user_id, get_encrypted(key, username), get_encrypted(key, password)))
        else:
            conn.execute('UPDATE presto SET password = ? WHERE user_id = ?', 
                    (get_encrypted(key, username), get_encrypted(key, password), user_id))

    return "successfully logged in"

def balance(key, user_id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM presto WHERE user_id=?', (user_id,))
    user = cur.fetchone()
    cur.close()
    if not user:
        return 'no user found'
    username = get_decrypted(key, user['username'])
    password = get_decrypted(key, user['password'])
    return get_balance(username, password)

@app.route("/presto", methods=["POST"])
def presto():
    command = request.form.get('text').split()
    user_id = request.form.get('user_id')
    key = md5('%s%s' % (TOKEN, user_id)).hexdigest()

    if len(command) < 1 or command[0] == 'help':
        return helper()
    elif command[0] == 'login': 
        if len(command[1:]) != 2:
            return "missing username or password"
        username, password = command[1:]
        return login(key, user_id, username, password)
    elif command[0] == 'balance':
        return balance(key, user_id)
    else:
        return "unknown command, use /presto help to see valid commands"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
