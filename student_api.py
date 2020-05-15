from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello World'
    })

@app.route('/student/all')
def get_all_student():
    con = sqlite3.connect('student.sqlite3')
    con.row_factory = dict_factory
    cur = con.cursor()
    all_students = cur.execute("SELECT * FROM tbl_student").fetchall()
    cur.close()
    con.close()
    return jsonify(all_students)

@app.route('/student')
def get_student():
    param = request.args
    name = param.get('name', '')
    order_by = param.get('order_by', None)
    if order_by is None or order_by not in ('id', 'class_id', 'name'):
        order_by = 'student_id'
    sort_order = param.get('sort_order')
    if sort_order is None or (sort_order.lower() != 'asc' and sort_order.lower() != 'desc'):
        sort_order = 'ASC'
    con = sqlite3.connect('student.sqlite3')
    con.row_factory = dict_factory
    cur = con.cursor()
    all_students = cur.execute("SELECT * FROM tbl_student WHERE student_name LIKE '%" + name + "%' ORDER BY " + order_by + " " + sort_order).fetchall()
    cur.close()
    con.close()
    return jsonify(all_students)

@app.route('/student/add', methods=['POST'])
def add_new_student():
    print(request.json)
    student_name = request.json.get('student_name', None)
    student_address = request.json.get('student_address', None)
    class_id = request.json.get('class_id', None)
    if student_name is None or student_address is None or class_id is None:
        return make_response(jsonify({
            'message': 'Missing required parameter'
        }), 400)
    con = sqlite3.connect('student.sqlite3')
    cur = con.cursor()
    data = (student_name, student_address, class_id)
    cur.execute("INSERT INTO tbl_student(student_name, student_address, class_id) VALUES('%s', '%s', %s)" % (data))
    con.commit()
    last_id = cur.lastrowid
    cur.close()
    con.close()
    return make_response(jsonify({
        'message': 'Inserted data successfully',
        'student_id': last_id
    }), 200)

@app.route('/student/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_or_delete_student(student_id):
    if request.method == 'GET':
        con = sqlite3.connect('student.sqlite3')
        con.row_factory = dict_factory
        cur = con.cursor()
        student = cur.execute("SELECT * FROM tbl_student WHERE student_id=%s" % (student_id)).fetchone()
        return jsonify(student)
    elif request.method == 'PUT':
        student_name = request.json.get('student_name', None)
        student_address = request.json.get('student_address', None)
        class_id = request.json.get('class_id', None)
        if student_name is None or student_address is None or class_id is None:
            return make_response(jsonify({
                'message': 'Missing required parameter'
            }), 400)
        con = sqlite3.connect('student.sqlite3')
        cur = con.cursor()
        data = (student_name, student_address, class_id, student_id)
        cur.execute("UPDATE tbl_student SET student_name='%s', student_address='%s', class_id=%s WHERE student_id=%s" % (data))
        con.commit()
        n = cur.rowcount
        cur.close()
        con.close()
        if n > 0:
            return make_response(jsonify({
                'message': 'Update student successfully',
            }), 200)
        else:
            return make_response(jsonify({
                'message': 'Student id not found'
            }), 404)
    elif request.method == 'DELETE':
        con = sqlite3.connect('student.sqlite3')
        cur = con.cursor()
        cur.execute("DELETE FROM tbl_student WHERE student_id=%s" % (student_id))
        con.commit()
        n = cur.rowcount
        cur.close()
        con.close()
        if n > 0:
            return make_response(jsonify({
                'message': 'Deleted student successfully',
            }), 200)
        else:
            return make_response(jsonify({
                'message': 'Student id not found'
            }), 404)
    else:
        pass

app.run(host='0.0.0.0')