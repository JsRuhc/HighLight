#! /usr/bin/python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright 2019 (C) Hui Lan <hui.lan@cantab.net>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
from UseSqlite import InsertQuery, RecordQuery
import pickle_idea, pickle_idea2
import os
import random, glob
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash, get_flashed_messages,Blueprint
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level
from signup_bp import signup_bp
from login_bp import login_bp
from logout_bp import logout_bp
from mark_bp import mark_bp
from user_bp import user_bp

import tool


app = Flask(__name__)
app.secret_key = 'lunch.time!'

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(mark_bp)
app.register_blueprint(user_bp)


path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './' # comment this line in deployment



@app.route("/<username>/reset", methods=['GET', 'POST'])
def user_reset(username):
    if request.method == 'GET':
        session['articleID'] = None
        return redirect(url_for('user_bp.userpage', username=username))
    else:
        return 'Under construction'

@app.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' +  'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        d = tool.load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [tool.get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
        return redirect(url_for('user_bp.userpage', username=username))
    else:
        return 'Under construction'


@app.route("/<username>/<word>/unfamiliar", methods=['GET', 'POST'])
def unfamiliar(username,word):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.unfamiliar(user_freq_record,word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return redirect(url_for('user_bp.userpage', username=username))

@app.route("/<username>/<word>/familiar", methods=['GET', 'POST'])
def familiar(username,word):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.familiar(user_freq_record,word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return redirect(url_for('user_bp.userpage', username=username))

@app.route("/<username>/<word>/del", methods=['GET', 'POST'])
def deleteword(username,word):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea2.deleteRecord(user_freq_record,word)
    flash(f'<strong>{word}</strong> is no longer in your word list.')
    return redirect(url_for('user_bp.userpage', username=username))
    
# @app.route("/mark", methods=['GET', 'POST'])
# def mark_word():
#     if request.method == 'POST':
#         d = tool.load_freq_history(path_prefix + 'static/frequency/frequency.p')
#         lst_history = pickle_idea.dict2lst(d)
#         lst = []
#         for word in request.form.getlist('marked'):
#             lst.append((word, 1))
#         d = pickle_idea.merge_frequency(lst, lst_history)
#         pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
#         return redirect(url_for('mainpage'))
#     else:
#         return 'Under construction'



@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        page = '<form method="post" action="/mark">\n'
        count = 1
        for x in lst:
            page += '<p><font color="grey">%d</font>: <a href="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (count, youdao_link(x[0]), x[0], x[1], x[0])
            count += 1
        page += ' <input type="submit" value="确定并返回"/>\n'
        page += '</form>\n'
        # save history 
        d = tool.load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        
        return page
    elif request.method == 'GET': # when we load a html page
        page = '''
             <html lang="zh">
               <head>
               <meta charset="utf-8">
               <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />
               <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

                 <title>EnglishPal 英文单词高效记</title>

               </head>
               <body>
        '''
        page += '<div class="container-fluid">'
        page += '<p><b><font size="+3" color="red">English Pal - Learn English smartly!</font></b></p>'
        if session.get('logged_in'):
            page += ' <a href="%s">%s</a></p>\n' % (session['username'], session['username'])
        else:
            page += '<p><a href="/login">登录</a>  <a href="/signup">成为会员</a> <a href="/static/usr/instructions.html">使用说明</a></p>\n'
        #page += '<p><img src="%s" width="400px" alt="advertisement"/></p>' % (get_random_image(path_prefix + 'static/img/'))
        page += '<p><b>%s</b></p>' % (tool.get_random_ads())
        page += '<div class="alert alert-success" role="alert">共有文章 <span class="badge bg-success"> %d </span> 篇</div>' % (tool.total_number_of_essays())
        page += '<p>粘帖1篇文章 (English only)</p>'
        page += '<form method="post" action="/">'
        page += ' <textarea name="content" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get文章中的词频"/>'
        page += ' <input type="reset" value="清除"/>'
        page += '</form>'
        d = tool.load_freq_history(path_prefix + 'static/frequency/frequency.p')
        if len(d) > 0:
            page += '<p><b>最常见的词</b></p>'
            for x in sort_in_descending_order(pickle_idea.dict2lst(d)):
                if x[1] <= 99:
                    break
                page += '<a href="%s">%s</a> %d\n' % (youdao_link(x[0]), x[0], x[1])

        page += ' <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
        page += '</div>'
        page += '</body></html>'
        return page






if __name__ == '__main__':
    #app.secret_key = os.urandom(16)
    #app.run(debug=False, port='6000')
    app.run(debug=True)        
    #app.run(debug=True, port='6000')
    #app.run(host='0.0.0.0', debug=True, port='6000')
