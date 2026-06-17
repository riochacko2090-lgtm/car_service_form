from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_name TEXT NOT NULL,
            variant TEXT,
            car_number TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            address TEXT,
            phone TEXT NOT NULL,
            email TEXT,
            booking_date TEXT,
            booking_time TEXT,
            expected_delivery TEXT,
            service_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Create the database and table when the app starts
init_db()

# 1. User Booking Form Page (Home Route)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extracting data from the HTML form
        car_name = request.form['car_name']
        variant = request.form['variant']
        car_number = request.form['car_number']
        owner_name = request.form['owner_name']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        booking_date = request.form['booking_date']
        booking_time = request.form['booking_time']
        expected_delivery = request.form['expected_delivery']
        service_type = request.form['service_type']

        # Inserting data into the SQLite database
        conn = sqlite3.connect('service_center.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (car_name, variant, car_number, owner_name, address, phone, email, booking_date, booking_time, expected_delivery, service_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (car_name, variant, car_number, owner_name, address, phone, email, booking_date, booking_time, expected_delivery, service_type))
        conn.commit()
        conn.close()
        
        return "<h1>Booking Submitted Successfully!</h1><a href='/'>Go Back</a>"
        
    return render_template('index.html')

# 2. Admin Panel Page (To view all bookings)
@app.route('/admin')
def admin():
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    data = cursor.fetchall()
    conn.close()
    return render_template('admin.html', bookings=data)

# 3. Delete Route (To remove a booking by its ID)
@app.route('/delete/<int:id>')
def delete_booking(id):
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)