import re

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from prisma import Prisma

# Create Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set your secret key here

# Initialize Prisma client
prisma = Prisma()

# Route for login
@app.route('/pythonlogin/', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        try:
            print("Attempting to connect to Prisma...")
            # Connect to Prisma before querying
            await prisma.connect()
            print("Connected to Prisma")

            user = await prisma.kiro.find_first(where={"username": username, "password": password})
            print("Query executed")

            if user:
                session['loggedin'] = True
                session['id'] = user.id
                session['username'] = user.username
                print("User found")
                return redirect(url_for('home'))
            else:
                flash("Incorrect username/password!", "danger")
                print("Incorrect username/password")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            print(f"An error occurred: {str(e)}")
        finally:
            # Disconnect Prisma after querying
            flash("finally")
            print(f"finally")
            await prisma.disconnect()
    
    return render_template('front/index.html', title="Login")

# Route for registration
# Route for registration
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        try:
            print("Attempting to connect to Prisma...")
            # Connect to Prisma before querying
            await prisma.connect()
            print("Connected to Prisma")

            user = await prisma.kiro.find_first(where={"username": username})
            print("Query executed")

            if user:
                flash("Username already exists!", "danger")
                print("Username already exists")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash("Invalid email address!", "danger")
                print("Invalid email address")
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash("Username must contain only characters and numbers!", "danger")
                print("Invalid username format")
            elif not username or not password or not email:
                flash("Please fill out the form!", "danger")
                print("Please fill out the form")
            else:
                new_user = await prisma.kiro.create(
                    data={"username": username, "password": password, "email": email}
                )
                flash("You have successfully registered!", "success")
                print("User registered successfully")
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            print(f"An error occurred: {str(e)}")
        finally:
                    # Disconnect Prisma after querying
                    flash("finally")
                    print(f"finally")
                    await prisma.disconnect()
    elif request.method == 'POST':
        flash("Please fill out the form!", "danger")
        print("Please fill out the form")
    
    return render_template('front/index.html', title="Register")

# Route for home page
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('/home/home.html', username=session['username'], title="Home")
    return redirect(url_for('login'))

# Route for profile page
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('auth/profile.html', username=session['username'], title="Profile")
    return redirect(url_for('login'))

# Route for submitting audio
@app.route('/submit_audio', methods=['POST'])
def submit_audio():
    if 'loggedin' in session:
        audio_file = request.files['audio_file']
        file_path = "/Users/kiroloskhela/Desktop/Grad/Integration/tmp/temp_audio_6.wav"
        audio_file.save(file_path)
        # Here you can perform the necessary operations with the audio file and return the response
        return render_template('home/home.html', title="Login")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



