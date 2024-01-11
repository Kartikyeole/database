from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create a table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        roll_no INTEGER UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        mobile_number TEXT NOT NULL,
        email TEXT NOT NULL,
        branch TEXT NOT NULL,
        erp_id TEXT UNIQUE NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

@app.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.get_json()

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO students (roll_no, first_name, last_name, mobile_number, email, branch, erp_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['roll_no'], data['first_name'], data['last_name'], data['mobile_number'], data['email'], data['branch'], data['erp_id']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data inserted successfully'})

@app.route('/read_data/<erp_id>', methods=['GET'])
def read_data(erp_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE erp_id = ?', (erp_id,))
    student = cursor.fetchone()

    conn.close()

    if student:
        result = {
            'roll_no': student[1],
            'first_name': student[2],
            'last_name': student[3],
            'mobile_number': student[4],
            'email': student[5],
            'branch': student[6],
            'erp_id': student[7]
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Data not found for the given erp_id'})

if __name__ == '__main__':
    app.run(debug=True)
