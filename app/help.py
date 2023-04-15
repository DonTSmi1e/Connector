from flask import Blueprint, render_template, redirect, url_for

help = Blueprint('help', __name__)

help_list = [["Правила сообщества", "help/rules.html", "0"], ["Меня забанили, что будет с аккаунтом?", "help/help_1.html", "1"]]

@help.route('/help')
def index():
    return render_template('help/help.html', help_list=help_list)

@help.route('/help/<int:id>')
def page(id):
    try:
        help_list[id]
    except:
        return redirect(url_for('help.index'))
    else:
        return render_template(help_list[id][1])