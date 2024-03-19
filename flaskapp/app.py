from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
db_config_path = os.path.join(base_dir, 'db.yaml')

# Load database configuration from db.yaml using the absolute path
db = yaml.load(open(db_config_path), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/add', methods=['POST'])
def add_entry():
    details = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO entries(name, description) VALUES (%s, %s)", (details['name'], details['description']))
    mysql.connection.commit()
    cur.close()
    return jsonify(details), 201

@app.route('/entries', methods=['GET'])
def get_entries():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM entries")
    if result > 0:
        entries = cur.fetchall()
        return jsonify([{'id': entry[0], 'name': entry[1], 'description': entry[2]} for entry in entries])
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
