# Main application file
from flask import Flask, jsonify, request, render_template
import mysql.connector
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5501", "http://127.0.0.1:8000", "http://localhost:5501", "http://localhost:8000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MySQL Connection Function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT'],
            auth_plugin='mysql_native_password'  # Add this line for XAMPP
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Test Database Connection
@app.route('/test-db', methods=['GET'])
def test_db():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
            return jsonify({'message': 'Database connection successful!'}), 200
        except mysql.connector.Error as e:
            return jsonify({'error': f'Database query failed: {e}'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Database connection failed!'}), 500

# Create Users Table (Run once)
def create_users_table():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    city VARCHAR(100) NOT NULL
                )
            ''')
            
            # Check if table is empty and insert sample data
            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                sample_data = [
                    ('John Doe', 28, 'john.doe@example.com', 'Male', 'New York'),
                    ('Alice Smith', 25, 'alice.smith@example.com', 'Female', 'Los Angeles'),
                    ('Bob Johnson', 32, 'bob.johnson@example.com', 'Male', 'Chicago'),
                    ('Carol Davis', 29, 'carol.davis@example.com', 'Female', 'Miami'),
                    ('David Wilson', 35, 'david.wilson@example.com', 'Male', 'Seattle'),
                    ('Emma Brown', 27, 'emma.brown@example.com', 'Female', 'Boston'),
                    ('Frank Miller', 31, 'frank.miller@example.com', 'Male', 'Denver'),
                    ('Grace Lee', 26, 'grace.lee@example.com', 'Female', 'Austin'),
                    ('Henry Garcia', 33, 'henry.garcia@example.com', 'Male', 'Phoenix'),
                    ('Ivy Chen', 24, 'ivy.chen@example.com', 'Female', 'San Francisco')
                ]
                cursor.executemany('''
                    INSERT INTO users (name, age, email, gender, city)
                    VALUES (%s, %s, %s, %s, %s)
                ''', sample_data)
                connection.commit()
                print("Inserted sample data into users table")
                
            print("Users table is ready")
        except mysql.connector.Error as e:
            print(f"Error setting up users table: {e}")
        finally:
            cursor.close()
            connection.close()

# User Routes
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users ORDER BY id')
        users = cursor.fetchall()
        return jsonify(users), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'age', 'email', 'gender', 'city']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO users (name, age, email, gender, city)
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (
                data['name'],
                data['age'],
                data['email'],
                data['gender'],
                data['city']
            )
        )
        connection.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': cursor.lastrowid
        }), 201
    except mysql.connector.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Email already exists'}), 400
        return jsonify({'error': str(e)}), 500
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    # Validate at least one field is provided
    if not data:
        return jsonify({'error': 'No data provided for update'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append('name = %s')
            update_values.append(data['name'])
        if 'age' in data:
            update_fields.append('age = %s')
            update_values.append(data['age'])
        if 'email' in data:
            update_fields.append('email = %s')
            update_values.append(data['email'])
        if 'gender' in data:
            update_fields.append('gender = %s')
            update_values.append(data['gender'])
        if 'city' in data:
            update_fields.append('city = %s')
            update_values.append(data['city'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields provided for update'}), 400
        
        # Add user_id to the values for WHERE clause
        update_values.append(user_id)
        
        # Build and execute the update query
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        cursor.execute(update_query, update_values)
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User updated successfully'}), 200
    except mysql.connector.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Email already exists'}), 400
        return jsonify({'error': str(e)}), 500
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# Health Check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Flask MySQL API',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Create table and insert sample data if needed
    create_users_table()
    app.run(debug=True, host='0.0.0.0', port=8000)