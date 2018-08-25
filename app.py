from flask import Flask, render_template, request, send_from_directory, redirect
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
from Logic.models import db
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/formList')
def form_list():
    from Logic.facade import get_all_forms
    return render_template('form_list.html', rows=get_all_forms())


@app.route('/formBuilder')
def form_builder():
    return render_template('form_builder.html')


@app.route('/js/<file>')
def js(file):
    return send_from_directory('./templates/', file)


@app.route('/style/<file>')
def css(file):
    return send_from_directory('./templates/', file)


@app.route('/submissions/<form_id>')
def submissions(form_id):
    from Logic.facade import get_all_submissions,get_form_name
    return render_template('form_submissions.html', rows=get_all_submissions(form_id),form_name=get_form_name(form_id))


@app.route('/submit/<form_id>', methods=['GET', 'POST'])
def submit(form_id):
    from Logic.facade import get_all_fields,add_new_submission_to_form,get_form_name
    all_fields = get_all_fields(form_id)
    if request.method == 'POST':
        submission = {}
        for field in all_fields:
            # Assuming that the name is unique
            field_name = field["name"]
            field_id = field["id"]
            submission[str(field_id)] = request.form[str(field_name)]
        add_new_submission_to_form(submission,form_id)
        return redirect("/submissions/"+str(form_id))
    else:
        return render_template('form_submit.html', rows=all_fields,form_name=get_form_name(form_id))


@socketio.on('connect')
def connect():
    print("client connected")


@socketio.on('add_new_form')
def add_new_form(json):
    from Logic.facade import add_new_form,add_new_field_to_form,is_exist_duplicate_names_in_form
    form_name = json["form_name"]
    fields = json["fields"]
    if is_exist_duplicate_names_in_form(fields):
        emit('form_not_saved',{"reason": "Sorry , but the field name must be unique"})
        return
    form_id = add_new_form(form_name)
    for field in fields:
        add_new_field_to_form(form_id, field['label'], field['name'], field['type'])

    emit('form_saved')


@socketio.on('disconnect_client')
def disconnect(json):
    print('client disconnected: received json - ' + str(json))


if __name__ == '__main__':
    socketio.run(app)







