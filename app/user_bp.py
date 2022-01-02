from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
import pickle_idea, pickle_idea2
from datetime import datetime
from flask import  request,  render_template,  session,  flash, Blueprint
import tool

user_bp = Blueprint('user_bp',__name__)
path_prefix = './'


@user_bp.route("/<username>", methods=['GET', 'POST'])
def userpage(username):
    
    if not session.get('logged_in'):
        return '<p>请先<a href="/login">登录</a>。</p>'

    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return '<p>账号 %s 过期。</p><p>为了提高服务质量，English Pal 收取会员费用， 每天0元。</p> <p>请决定你要试用的时间长度，扫描下面支付宝二维码支付。 支付时请注明<i>English Pal Membership Fee</i>。 我们会于12小时内激活账号。</p><p><img src="static/donate-the-author-hidden.jpg" width="120px" alt="支付宝二维码" /></p><p>如果有问题，请加开发者微信 torontohui。</p> <p><a href="/logout">登出</a></p>' % (username)

    
    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' +  'frequency_%s.pickle' % (username)

    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        page = '<meta charset="UTF8">'        
        page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />'        
        page += '<p>勾选不认识的单词</p>'
        page += '<form method="post" action="/%s/mark">\n' % (username)
        page += ' <input type="submit" name="add-btn" value="加入我的生词簿"/>\n'        
        count = 1
        words_tests_dict = pickle_idea.load_record(path_prefix + 'static/words_and_tests.p')        
        for x in lst:
            page += '<p><font color="grey">%d</font>: <a href="%s" title="%s">%s</a> (%d)  <input type="checkbox" name="marked" value="%s"></p>\n' % (count, youdao_link(x[0]), tool.appears_in_test(x[0], words_tests_dict), x[0], x[1], x[0])
            count += 1
        page += '</form>\n'
        return page
    
    elif request.method == 'GET': # when we load a html page


        d = tool.load_freq_history(user_freq_record)  # 获取生词库中生词
        if len(d) > 0:
            lst = pickle_idea2.dict2lst(d)
            lst2 = []
            highlight = ""
            k = ","
            for t in lst:
                lst2.append((t[0], len(t[1])))
            for x in sort_in_descending_order(lst2):
                word = x[0]
                if highlight =='':
                    highlight = highlight+str(word)
                else:
                    highlight = highlight +str(k) + str(word)
            session['highlight']=highlight

        page = '<meta charset="UTF8">\n'
        page += '<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=3.0, user-scalable=yes" />\n'
        page += '<meta name="format-detection" content="telephone=no" />\n' # forbid treating numbers as cell numbers in smart phones
        page += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'
        page += '<title>EnglishPal Study Room for %s</title>' % (username)
        page += '<div class="container-fluid">'
        page += '<p><b>English Pal for <font color="red">%s</font></b> <a class="btn btn-secondary" href="/logout" role="button">登出</a></p>' % (username)
        page += tool.get_flashed_messages_if_any()
        page += '<p><b>阅读文章并回答问题</b></p>\n'
        page += '<p><a class="btn btn-success" href="/%s/reset" role="button" > 下一篇 Next Article </a></p>' % (username)
        highlight = session.get('highlight')
        print(highlight,'123123')
        page +='高亮颜色：'
        page +='<input type="color" id="color" value="#0FC0CB">'
        page +='<input type="button" id="button3" value="应用" onclick="showit2()"/ ><br><br>'
        page +=' <input type="button" id="button" value="生词库高亮" onclick="add(&quot;%s&quot),showit()"/ >'%(highlight)
        page +='<input type="button" id="button2" value="清除高亮" onclick="hideit()"/ ><br>'
        page +='<button   id="btn1"  οnclick="btn1();" disabled=true >阅读模式开启</button>'
        page +='<button   id="btn2"  οnclick="btn2();" >添加单词</button><br>'
        page += '<div >%s</div>'% (tool.get_user_level(user_freq_record, session['articleID']))
        page += '<div id="text-content">%s</div>'% (tool.get_today_article(user_freq_record, session['articleID']))
        d = session.get('reading')
        page += '<p><b>%s</b></p>' % (tool.get_question_part(d['question']))
        page += '%s' % (tool.get_answer_part(d['question']))
        page += '<p><b>收集生词吧</b> （可以在正文中划词，也可以复制黏贴）</p>'
        page += '<form method="post" action="/%s">' % (username)
        page += ' <textarea name="content" id="selected-words" rows="10" cols="120"></textarea><br/>'
        page += ' <input type="submit" value="get 所有词的频率"/>'
        page += ' <input type="reset" value="清除"/>'
        page +=' <input type="button" id="button" value="生词库高亮" onclick="add(&quot;%s&quot),showit()"/ >'%(highlight)
        page +='<input type="button" id="button2" value="清除高亮" onclick="hideit()"/ ><br>'
        page += '</form>\n'
        page += ''' 
                # <script>
                    
                   function getWord(){ 
                       var word = window.getSelection?window.getSelection():document.selection.createRange().text;
                       return word;
                       }
                   }
                   function fillinWord(){
                       var element = document.getElementById("selected-words");
                       element.value = element.value + " " + getWord();
                   }
                   document.getElementById("text-content").addEventListener("click", fillinWord, false);
                   document.getElementById("text-content").addEventListener("touchstart", fillinWord, false);
                 </script>
                 '''
        if session.get('thisWord'):
            page += '''
                   <script type="text/javascript">
                        //point to the anchor in the page whose id is aaa if it exists
                        window.onload = function(){
                            var element = document.getElementsByName("aaa");
                            if (element != null)
                                document.getElementsByName("aaa")[0].scrollIntoView(true);
                        }
                   </script> 
                   '''

        d = tool.load_freq_history(user_freq_record)
        if len(d) > 0:
            page += '<p><b>我的生词簿</b></p>'
            lst = pickle_idea2.dict2lst(d)
            lst2 = []
            highlight = ""
            k = ","
            for t in lst:
                lst2.append((t[0], len(t[1])))
            for x in sort_in_descending_order(lst2):
                word = x[0]
                if highlight =='':
                    highlight = highlight+str(word)
                else:
                    highlight = highlight +str(k) + str(word)
                freq = x[1]

                if session.get('thisWord') == x[0] and session.get('time') == 1:
                    page += '<a name="aaa"></a>'        # 3. anchor
                    session['time'] = 0                 # discard anchor
                if isinstance(d[word], list):           # d[word] is a list of dates
                    if freq > 1:
                        page += '<p class="new-word"> <a class="btn btn-light" href="%s" role="button">%s</a>(<a title="%s">%d</a>) <a class="btn btn-success" href="%s/%s/familiar" role="button">熟悉</a> <a class="btn btn-warning" href="%s/%s/unfamiliar" role="button">不熟悉</a>  <a class="btn btn-danger" href="%s/%s/del" role="button">删除</a> </p>\n' % (youdao_link(word), word, '; '.join(d[word]), freq,username, word,username,word, username,word)
                    else:
                        page += '<p class="new-word"> <a class="btn btn-light" href="%s" role="button">%s</a>(<a title="%s">%d</a>) <a class="btn btn-success" href="%s/%s/familiar" role="button">熟悉</a> <a class="btn btn-warning" href="%s/%s/unfamiliar" role="button">不熟悉</a>  <a class="btn btn-danger" href="%s/%s/del" role="button">删除</a> </p>\n' % (youdao_link(word), word, '; '.join(d[word]), freq,username, word,username,word, username,word)
                elif isinstance(d[word], int): # d[word] is a frequency. to migrate from old format.
                    page += '<a href="%s">%s</a>%d\n' % (youdao_link(word), word, freq)
            session['highlight']=highlight
        # page += '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
        # #page += '</div>'
        page += ''' 
                <script language="javascript">
                    var bt1 = document.getElementById("btn1")
                    var bt2 = document.getElementById("btn2")

                    bt1.addEventListener("click",function ()
                    {
                            var audio = new Audio();
                            audio.src ='http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=Hello%20World';
                            audio.play();
                            document.getElementById("btn1").disabled=true;
                            document.getElementById("btn1").innerHTML="阅读模式开启";
                            document.getElementById("btn2").disabled=false;
                            document.getElementById("btn2").innerHTML="点击开启添加单词";
                            i = 2
                        })
                        bt2.addEventListener("click",function ()
                    {
                            document.getElementById("btn1").disabled=false;
                            document.getElementById("btn1").innerHTML="点击开启阅读模式";
                            document.getElementById("btn2").disabled=true;
                            document.getElementById("btn2").innerHTML="添加单词模式开启";
                            i =1;
                        })

                    var content =document.getElementById('text-content');    //获取文章内容
                    var contents = content.innerHTML;                                       
                    var keyword = [];
                    var keyword2= [];
                    var keyword3 = [];
                    var i = 0;
                    var text = document.getElementById("text");
                    var button = document.getElementById("button");
                    
                    content.onmouseup = function(){
                     var color = document.getElementById('color');            //获取颜色
                        var colors = color.value
                        keyword = keyword.concat(keyword2);
                        if(selectText() != ''){
                             if(selectText().length>1){
                             var element = document.getElementById("selected-words");
                             element.value = element.value + " " + selectText();            //讲选择的内容加入到编辑框中
                             keyword=keyword.concat(selectText());
                             }                                                                                  
                         for (var j = 0; j < keyword.length; j++) {
                             var value=keyword[j];
                             var values = contents.split(value);                                                          //分离出文章内容中的对应单词
                             var re = new RegExp('(' + keyword.join('|') + ')', 'ig')                                     
                             content.innerHTML = contents.replace(re, '<span style="background:'+colors+';">$1</span>')   //改变文章内容中的单词背景颜色
                    }
                    }
                    }
                    function selectText(){                                          //选择文本
                        if(i==1){
                            if(document.Selection){       
                                //ie浏览器
                                return document.selection.createRange().text;     	 
                            }else{    
                                //标准浏览器
                                return window.getSelection().toString();	 
                            }
                        }	 
                    }
                    
                    function showit()                                           //隐藏高亮或阅读下篇文章后再次展示高亮  对应高亮按钮方法
                    {    var color = document.getElementById('color');
                        var colors = color.value
                        keyword2=keyword2.concat(keyword)
                        keyword3=keyword3.concat(keyword2)
                        for (var a = 0; a < keyword2.length; a++) {
                        if(keyword2[a]!=''){
                        var value=keyword2[a];
                        var values = contents.split(value);                                                          //分离出文章内容中的对应单词
                        var values = contents.split(value);                                                            
                        var ra = new RegExp('(' + keyword2.join('|') + ')', 'ig')
                        content.innerHTML = contents.replace(ra, '<span style="background:'+colors+';">$1</span>')  //改变文章内容中的单词背景颜色
                    }
                    }
                    }
                    function hideit()                                               //隐藏高亮
                    {    
                        keyword2=keyword2.concat(keyword)
                         keyword3=keyword3.concat(keyword2)
                         for (var a = 0; a < keyword3.length; a++) {
                         var value=keyword3[a];
                         var values = contents.split(value);
                         var ra = new RegExp('(' + keyword2.join('|') + ')', 'ig')
                         content.innerHTML = contents.replace(ra , '<span style="background:;">$1</span>')
                        
                    }
                         keyword3=[];
                         keyword2=[];
                         keyword.splice(0,keyword.length);
                    }
                    function showit2()                                             // 对应 更改颜色中的方法 展示高亮 
                    {    
                        var color = document.getElementById('color');
                        var colors = color.value
                        keyword2=keyword2.concat(keyword);
                        keyword3=keyword3.concat(keyword2);
                         for (var a = 0; a < keyword2.length; a++) {
                         var value=keyword2[a];
                         var values = contents.split(value);
                         var ra = new RegExp('(' + keyword2.join('|') + ')', 'ig')
                         content.innerHTML = contents.replace(ra, '<span style="background:'+colors+';">$1</span>')
                    }
                    }
              function add(high)
                    {    
                       var s = high.split(",");
                        keyword2=keyword2.concat(s)
                    }
                    
                    </script> 
                 '''
        return page