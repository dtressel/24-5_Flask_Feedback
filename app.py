from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import UserRegistrationForm, UserLoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'fruitsmell9753'

connect_db(app)

# with app.app_context():
#     db.create_all()

@app.route('/')
def home_route():
    """Home route redirects to registration page"""

    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def show_register_form():
    """Shows the registration form page"""

    form = UserRegistrationForm()

    if form.validate_on_submit():
        new_user = User.create_user(
            username = form.username.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            password = form.password.data
            )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

        # add user to session
        session['username'] = new_user.username

        return redirect(f'/users/{new_user.username}')
    else:
        print('rendering register.html')
        return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def show_login_page():
    """Shows the login page."""

    form = UserLoginForm()

    if form.validate_on_submit():
        authenticated_user = User.authenticate_user(
            username = form.username.data,
            password = form.password.data
        )
        if authenticated_user:
            # add user to session
            session['username'] = authenticated_user.username

            return redirect(f'/users/{authenticated_user.username}')
        else:
            form.password.errors = ['Incorrect username or password.']
    return render_template('login.html', form = form)

@app.route('/users/<username>')
def show_user_page(username):
    """Shows user page."""

    # If there is a logged in user
    if 'username' in session:
        # If logged in user matches requested user page
        if session['username'] == username:
            user = User.query.get(username)
            return render_template('user_page.html', user=user)
        # If logged in user doesn't match, redirect to logged-in user's page
        else:
            actual_username = session['username']
            return redirect(f'/users/{actual_username}')
            
    # If no logged in user, redirect to login page
    return redirect('/login')

@app.route('/logout', methods = ['POST'])
def logout_user():
    """Logs out the user by removing username from session."""

    session.pop('username')
    return redirect('/')