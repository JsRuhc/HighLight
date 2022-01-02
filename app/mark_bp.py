from flask import  request, render_template,redirect, session, flash, Blueprint
import tool
import pickle_idea


mark_bp = Blueprint('mark_bp',__name__)

path_prefix = '/var/www/wordfreq/wordfreq/'

@mark_bp.route("/mark", methods=['GET', 'POST'])
def mark_word():
    if request.method == 'POST':
        d = tool.load_freq_history(path_prefix + 'static/frequency/frequency.p')
        lst_history = pickle_idea.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, 1))
        d = pickle_idea.merge_frequency(lst, lst_history)
        pickle_idea.save_frequency_to_pickle(d, path_prefix + 'static/frequency/frequency.p')
        return redirect(tool.url_for('mainpage'))
    else:
        return 'Under construction'