from Logic.models import *


def add_new_form(name):
    form = Form(name=name, submissions=0)
    db.session.add(form)
    db.session.commit()
    return form.id


def is_exist_duplicate_names_in_form(fields):
    hash_table={}
    for field in fields:
        if field["name"] in hash_table:
            return True
        hash_table[field["name"]] = 1
    return False


def add_new_field_to_form(form_id,label,name,type):
    exist = Field.query.filter_by(name=name,form_id=form_id).first()
    if exist is not None:
        return False
    field = Field(label=label, name=name,type=type,form_id=form_id)
    db.session.add(field)
    db.session.commit()


def get_all_forms():
    forms = Form.query.filter_by().all()
    return list(map(lambda form : {"id":form.id, "name":form.name,"submissions": form.submissions},forms))


def get_all_submissions(form_id):
    form = Form.query.filter_by(id=form_id).first()
    if form is None:
        return None
    fields = form.fields
    users = list(map(lambda submission : submission.user_id, fields[0].submissions))
    ans = []# [{user,fieldName1: input1, fieldName2:input2,...},...]
    fieldnames = [""]
    for field in fields:
        fieldnames.append(field.name)
    ans.append(fieldnames)
    counter = 1
    for user in users:
        row = [counter]
        counter += 1
        for field in fields:
            submission = Submission.query.filter_by(user_id=user,field_id=field.id).first()
            row.append(submission.input)
        ans.append(row)
    return ans


def get_all_fields(form_id):
    form = Form.query.filter_by(id=form_id).first()
    if form is None:
        return None
    fields = form.fields
    return list(map(lambda field: {"id":field.id,"name": field.name,"label":field.label,"type":field.type},fields))\



def generate_new_user_id():
    max_id = db.session.query(db.func.max(Submission.user_id)).scalar()
    if max_id is None:
        max_id = 0
    return max_id+1


def add_new_submission_to_form(submission, form_id):#{field_id:input,...}
    user = generate_new_user_id()
    for key, value in submission.items():
        if len(value) > 50:
            return "The input length must be up to 50"
    for key, value in submission.items():
        new_submission = Submission(user_id=user, field_id=key, input=value)
        db.session.add(new_submission)
        db.session.commit()
    form = Form.query.filter_by(id=form_id).first()
    form.submissions += 1
    db.session.commit()
    return "The submission is added successfully"


def get_form_name(form_id):
    form = Form.query.filter_by(id=form_id).first()
    return form.name