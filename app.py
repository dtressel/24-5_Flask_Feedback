from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import UserRegistrationForm, UserLoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'fruitsmell9753'

connect_db(app)

# with app.app_context():
#     db.drop_all()
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
        user = User.query.get_or_404(username)
        return render_template('user_page.html', user=user)
            
    # If no logged in user, redirect to login page
    return redirect('/login')

@app.route('/logout', methods = ['POST'])
def logout_user():
    """Logs out the user by removing username from session."""

    session.pop('username')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes user and removes their feedback."""

    user_to_delete = User.query.get(username)
    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Shows add feedback form and handles form submission."""

    form = FeedbackForm()

    if form.validate_on_submit():
        new_feedback = Feedback(
            title = form.title.data,
            content = form.content.data,
            username = username
            )
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('new_feedback.html', form = form)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    """Shows a form to edit a feedback and handles form submission."""

    form = FeedbackForm()

    feedback_to_edit = Feedback.query.get_or_404(feedback_id)

    if form.validate_on_submit():
        feedback_to_edit.title = form.title.data
        feedback_to_edit.content = form.content.data
        db.session.add(feedback_to_edit)
        db.session.commit()
        return redirect(f'/users/{feedback_to_edit.user}')

    return render_template('edit_feedback.html', form = form, feedback = feedback_to_edit)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Deletes a feedback."""

    feedback_to_delete = Feedback.query.get(feedback_id)
    db.session.delete(feedback_to_delete)
    db.session.commit()
    username = session['username']

    return redirect(f'/users/{username}')