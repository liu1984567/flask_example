"""
    model.py

    Implements the management.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from markdown import markdown
import bleach
from . import db
from . import login_manager, logger

class Permission:
    FOLLOW = 0x1
    COMMENT = 0x2
    WRITE_ARTICLES = 0x4
    MODERATE_COMMENTS = 0x8
    ADMINISTER = 0x80

class RolePermissionCode:
    USER = Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES
    MODERATOR = USER | Permission.MODERATE_COMMENTS
    ADMINISTRATOR = 0xFF

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(65), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name
    @staticmethod
    def init_roles():
        roles = {
                'User': RolePermissionCode.USER, 
                'Moderator': RolePermissionCode.MODERATOR, 
                'Administrator': RolePermissionCode.ADMINISTRATOR
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), unique=True, index=True)
    email = db.Column(db.String(65), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(65))
    location = db.Column(db.String(65))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen    = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=RolePermissionCode.ADMINISTRATOR).first()
            else:
                self.role = Role.query.filter_by(permissions=RolePermissionCode.USER).first()

    def __repr__(self):
        return '<user %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a reable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'confirm': self.id})
        return token

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id :
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def generate_resetpwd_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'resetpwd': self.id})
        return token

    def check_resetpwd_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('resetpwd') != self.id :
            return False
        return True

    def can(self, permissions):
        return self.role is not None and ((self.role.permissions & permissions) == permissions)

    def is_administrator(self):
        return self.can(RolePermissionCode.ADMINISTRATOR)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(f)
        
    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return db.session.query(Post).select_from(Follow).filter_by(follower_id=self.id).join(Post, Follow.followed_id == Post.author_id)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                    username=forgery_py.internet.user_name(True),
                    password=forgery_py.lorem_ipsum.word(),
                    confirmed=True,
                    name=forgery_py.name.full_name(),
                    location=forgery_py.address.city(),
                    about_me=forgery_py.lorem_ipsum.sentence(),
                    member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return '<post:%r %d>' % (self.author.username, self.id)

    @staticmethod
    def markdown_to_html(body_mk):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
                'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        body_html = markdown(body_mk, output_format='html') 
        logger.info(body_html)
        body_html = bleach.clean(body_html, tags=allowed_tags, strip=True)
        logger.info(body_html)
        body_html = bleach.linkify(body_html)
        logger.info(body_html)
        return body_html

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count-1)).first()
            p = Post(author=u,
                    body=forgery_py.lorem_ipsum.sentence(),
                    timestamp=forgery_py.date.date(True))
            db.session.add(p)
            db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
