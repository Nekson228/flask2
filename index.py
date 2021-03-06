import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, FileField
import json
from os import listdir
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('index.html', title=title)


@app.route('/training/<prof>')
def training(prof: str):
    prof = prof.lower()
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list>')
def list_prof(list):
    with open("static/json/profs.json", "rt", encoding="utf8") as f:
        prof_list = json.loads(f.read())
    return render_template('list.html', profs=prof_list, list_type=list)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    data = {
        'title': 'Прикол',
        'surname': 'Поглао',
        'name': 'Некит',
        'education': 'Низшее',
        'profession': 'Нету',
        'sex': 'male',
        'motivation': 'Хочу чтоб космическую станцию захватили пришельцы!',
        'ready': False,
    }
    return render_template('answer.html', **data)


class DoubleProtectionForm(FlaskForm):
    astronaut_id = StringField('ID Астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль Астронавта', validators=[DataRequired()])
    captain_id = StringField('ID Капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль Капитана', validators=[DataRequired()])
    submit = SubmitField('Получить доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = DoubleProtectionForm()
    if form.validate_on_submit():
        return redirect('/login/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/login/success')
def success():
    return render_template('success.html', text='Доступ разрешен!')


@app.route('/distribution')
def distribution():
    astronauts = ['Некит Поглов', 'Павел Эс', 'Иван Кириешка', 'Андроид Артишок']
    return render_template('distribution.html', staff=astronauts)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    color = f'rgb(0, 0, {round(255 / age * 15)})' if sex.lower() == 'male' else f'rgb({round(255 / age * 15)}, 0, 0)'
    return render_template('table.html', color=color, age=age)


class FileForm(FlaskForm):
    img_field = FileField('Добавить фото', validators=[FileRequired()])
    submit_field = SubmitField('Загрузить')


@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    form = FileForm()
    if request.method == 'GET':
        images = listdir('static/img/gallery')
        if form.validate_on_submit():
            return redirect('/gallery/success')
        return render_template('gallery.html', imgs=images, form=form)
    elif request.method == 'POST':
        file = form.img_field.data
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/img/gallery', filename))
        return redirect('/gallery/success')


@app.route('/gallery/success')
def gallery_success():
    return render_template('success.html', text='Фото отправлено')


@app.route('/member')
def member():
    with open('static/json/members.json', mode='rt', encoding='utf8') as jsonFile:
        members_data = json.loads(jsonFile.read())['members']
    return render_template('member.html', members=members_data)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080, debug=True)
