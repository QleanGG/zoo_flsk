from flask import Flask, jsonify, request, redirect,url_for
from flask_cors import CORS
import sqlite3

api = Flask(__name__)
CORS(api)
con = sqlite3.connect("zoo.db",check_same_thread=False)
cur = con.cursor()

# animals table
cur.execute('''
    CREATE TABLE IF NOT EXISTS zoo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    AnimalName TEXT NOT NULL UNIQUE,
    type TEXT,
    age INTEGER
);''')

# cur.execute('INSERT INTO zoo (AnimalName,type,age) VALUES(?,?,?)',('Guy','Lion',26))
# con.commit()
@api.route('/', methods =["GET"])
def home():
    return jsonify('Hello World')

@api.route('/get_animals', methods =["GET"])
def get_animals():
    try:
        cur.execute("SELECT * FROM zoo")

        rows = cur.fetchall()

        animals = [{'id': row[0], 'AnimalName': row[1], 'type': row[2], 'age': row[3]} for row in rows]
        return jsonify({'animals': animals})
    except Exception as e:
        return jsonify({'error': str(e)})
        
@api.route('/add_animal', methods = ["POST"])
def add_animals():
    if request.method == 'POST':
        try:
            data = request.get_json()
            req_name = data.get('animalName')
            req_type = data.get('type')
            req_age = data.get('age')
        
            # Verify that the data is received correctly
            print(data)

            # Insert data into the SQLite table
            cur.execute('INSERT INTO zoo (AnimalName, type, age) VALUES (?, ?, ?)', (req_name, req_type, req_age))
            con.commit()
            
            return jsonify({'success': True, 'message': 'Animal added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid request method'})

@api.route('/delete_animal/<int:id>', methods = ["DELETE"])
def delete_animals(id):
    if request.method == 'DELETE':
        try:
            cur.execute('DELETE FROM zoo WHERE ID = ?',(id,))
            con.commit()
            return jsonify({'success': True, 'message': 'Animal added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid request method'})
    
@api.route('/edit_animal/<int:id>', methods = ["PUT"])
def edit_animals(id):
    if request.method == 'PUT':
        try:
            data = request.get_json()
            req_name = data.get('animalName')
            req_type = data.get('type')
            req_age = data.get('age')
            print(req_name,req_age,req_type)
            cur.execute('''
                UPDATE zoo 
                SET AnimalName = ?, type = ?, age=?
                WHERE ID = ?;
                ''',(req_name,req_type,req_age,id))
            con.commit()
            return jsonify({'success': True, 'message': 'Animal added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid request method'})

if __name__ == '__main__':
    api.run(debug=True)