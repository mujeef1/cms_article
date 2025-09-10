"""
Routes and views for the Flask application with Microsoft Sign In integration.
"""
from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from FlaskWebProject import app, db, LOG
from FlaskWebProject.forms import LoginForm, PostForm
from FlaskWebProject.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
import msal
import uuid

# Azure Blob storage image URL
imageSourceUrl = f"https://{app.config['BLOB_ACCOUNT']}.blob.core.windows.net/{app.config['BLOB_CONTAINER']}/"

# --- Routes ---

@app.route('/')
@app.route('/home')
@login_required
def home():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.all()
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        post = Post()
        post.save_changes(form, request.files.get('image_path'), current_user.id, new=True)
        LOG.info(f'New post added by user: {current_user.id}')
        return redirect(url_for('home'))
    return render_template('post.html', title='Create Post', imageSource=imageSourceUrl, form=form)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(formdata=request.form, obj=post)
    if form.validate_on_submit():
        post.save_changes(form, request.files.get('image_path'), current_user.id)
        LOG.info(f'Post {id} edited by user: {current_user.id}')
        return redirect(url_for('home'))
    return render_template('post.html', title='Edit Post', imageSource=imageSourceUrl, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to home
    if current_user.is_authenticated:
        LOG.info(f'User {current_user.id} is already authenticated')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            LOG.warning(f'Login unsuccessful for user: {form.username.data}')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        LOG.info(f'User {user.id} logged in successfully via form')
        return redirect(next_page)

    # MSAL Auth URL for Microsoft Sign In button
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template('login.html', title='Sign In', form=form, auth_url=auth_url)

@app.route(Config.REDIRECT_PATH)
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))

    if "error" in request.args:
        LOG.error('Authentication/Authorization failure')
        return render_template("auth_error.html", result=request.args)

    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Config.SCOPE,
            redirect_uri=url_for('authorized', _external=True, _scheme='https')
        )
        if "error" in result:
            LOG.error('Did not acquire a token for OAUTH')
            return render_template("auth_error.html", result=result)

        session["user"] = result.get("id_token_claims")
        username = session["user"].get("preferred_username", "admin")

        # Check if user exists, else create
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        _save_cache(cache)
        LOG.info(f'User {user.id} logged in via Microsoft Sign In')

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        LOG.info(f'User {current_user.id} logged out')
    logout_user()
    if session.get("user"):
        session.clear()
        return redirect(
            f"{Config.AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('login', _external=True)}"
        )
    return redirect(url_for('login'))

# --- MSAL Helper Functions ---

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get('token_cache'):
        cache.deserialize(session['token_cache'])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session['token_cache'] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID,
        authority=authority or Config.AUTHORITY,
        client_credential=Config.CLIENT_SECRET,
        token_cache=cache
    )

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for('authorized', _external=True, _scheme='https')
    )
