from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://serik_s:qwerty@ds033036.mlab.com:33036/connect_to_mongo'

mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def index():
    users = mongo.db.users

    output = []

    for q in users.find():
        output.append({'_id': q['_id'], 'name': q['name'], 'language': q['language']})

    return render_template("index.html", result=output)


@app.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    users = mongo.db.users

    one = users.find_one({'_id': ObjectId(user_id)})

    if one:
        output = {'name': one['name'], 'language': one['language']}
    else:
        output = 'No results found!'

    return render_template("read.html", result=output)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            users.insert({'name': request.form['username'], 'language': request.form['user-language']})
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('create.html')


@app.route('/find')
def find():
    user = mongo.db.users
    person = user.find_one({'name': 'Person'})
    return 'You found ' + person['name'] + '. His language is ' + person['language']


@app.route('/update/<user_id>', methods=['GET', 'POST'])
def update(user_id):
    users = mongo.db.users
    updatingPerson = users.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':

        # existing_user = users.find_one({'name': request.form['username']})
        # users.insert({'name': request.form['username'], 'language': request.form['user-language']})
        updatingPerson['name'] = request.form['username']
        updatingPerson['language'] = request.form['user-language']
        users.save(updatingPerson)
        return redirect(url_for('index'))

        # return 'That username already exists!'
    return render_template('update.html', result=updatingPerson)


@app.route('/delete/<user_id>')
def delete(user_id):
    users = mongo.db.users
    deletingUser = users.find_one({'_id': ObjectId(user_id)})


    users.remove(deletingUser)
    return redirect(url_for('index'))

    # return render_template('delete.html', result=deletingUser)


if(__name__) == '__main__':
    app.run(debug=True)
