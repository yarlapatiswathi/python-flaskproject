from flask import Flask,render_template,url_for,redirect,flash
from project import app,db,bcrypt,login_manager,mail
from project.models import User
from project.forms import RegistrationForm,LoginForm,ForgotPasswordForm,NewPasswordForm
from flask_login import login_user,logout_user,current_user,login_required
from flask_mail import Message
@app.route('/')
@app.route('/homepage')
def home():
    return render_template('homepage.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=RegistrationForm()
    if form.validate_on_submit():
        encrypted_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}',category='success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'Account login success for {form.email.data}',category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Account login unsuccess for {form.email.data}',category='danger')
            return redirect(url_for('login'))
    return render_template('Login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_email(user):
    token=user.generate_token()
    print("requested token",token)
    msg=Message('Password Reset Request',recipients=[user.email],sender='noreply@gmail.com')
    msg.body=f'''To reset your password, Please click on the link below
                {url_for('newpassword',token=token,_external=True)}'''
    mail.send(msg)



@app.route('/forgot_password',methods=['POST','GET'])
def forgot_password():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            print("sending email")
            send_email(user)
            print('email sent')
            flash(f'Code sent to your Email. Please check {form.email.data}',category='success')
            return redirect(url_for('login'))
        else:
            flash(f'Kindly check your email','warning')
    return render_template('forgot_password.html',title='Forgot Password',form=form)

@app.route('/newpassword/<token>',methods=['POST','GET'])
def newpassword(token):
    print("newpassword token",token)
    user_id=User.verify_token(token)
    if not user_id:
        flash(f'This is invalid token or expired.Please try again.','warning')
        return redirect(url_for('forgot_password'))
    form=NewPasswordForm()
    if form.validate_on_submit():
        user=User.query.filter_by(id=user_id).first()
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f'Password changed.Please login!.','success')
        return redirect(url_for('login'))
    return render_template('NewPassword.html',title='New Password',form=form)