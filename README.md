# PNC Student Management System

A Flask-based web application for managing student records with a MySQL database backend.

## Features

- **User Management**: Create, Read, Update, and Delete (CRUD) student records
- **Responsive Design**: Works on both desktop and mobile devices
- **RESTful API**: Built with Flask for backend operations
- **Database Integration**: Uses MySQL for data persistence
- **Modern UI**: Clean and intuitive user interface built with Bootstrap 5

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/phanphoun/flask-api.git
   cd flask-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Create a MySQL database
   - Update the database configuration in `config.py`

5. **Initialize the database**
   ```bash
   python app.py
   ```
   This will create the necessary tables in your MySQL database.

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Project Structure

```
flask-api/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .gitignore
├── README.md
├── models/             # Database models
│   └── __init__.py
├── routes/             # API routes
│   └── __init__.py
└── templates/          # Frontend templates
    ├── index.html
    └── img/
        └── pnc.jpg
```

## API Endpoints

- `GET /users` - Get all users
- `GET /users/<id>` - Get a specific user
- `POST /users` - Create a new user
- `PUT /users/<id>` - Update a user
- `DELETE /users/<id>` - Delete a user

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Bootstrap 5 for the frontend components
- Flask for the web framework
- MySQL for the database
