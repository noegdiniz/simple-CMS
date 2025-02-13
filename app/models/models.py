from app.ext.db import db
from datetime import datetime
from flask_security import RoleMixin
from flask_security import UserMixin
from flask_admin import form

import os
import os.path as op
from sqlalchemy.event import listens_for
from app.helpers.helpes import file_path_galeria, file_path_icons, file_path_docs

# Define models
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

        
    # Permissions as boolean fields User
    can_create_user = db.Column(db.Boolean, default=False)
    can_edit_user = db.Column(db.Boolean, default=False)
    can_delete_user = db.Column(db.Boolean, default=False)
    can_view_user = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields News
    can_create_news = db.Column(db.Boolean, default=False)
    can_edit_news = db.Column(db.Boolean, default=False)
    can_delete_news = db.Column(db.Boolean, default=False)
    can_view_news = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Gallerie
    can_create_gallerie = db.Column(db.Boolean, default=False)
    can_edit_gallerie = db.Column(db.Boolean, default=False)
    can_delete_gallerie = db.Column(db.Boolean, default=False)
    can_view_gallerie = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Docs
    can_create_docs = db.Column(db.Boolean, default=False)
    can_edit_docs = db.Column(db.Boolean, default=False)
    can_delete_docs = db.Column(db.Boolean, default=False)
    can_view_docs = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Docs_types
    can_create_docs_types = db.Column(db.Boolean, default=False)
    can_edit_docs_types = db.Column(db.Boolean, default=False)
    can_delete_docs_types = db.Column(db.Boolean, default=False)
    can_view_docs_types = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Home
    can_create_home = db.Column(db.Boolean, default=False)
    can_edit_home = db.Column(db.Boolean, default=False)
    can_delete_home = db.Column(db.Boolean, default=False)
    can_view_home = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Home
    can_create_role = db.Column(db.Boolean, default=False)
    can_edit_role = db.Column(db.Boolean, default=False)
    can_delete_role = db.Column(db.Boolean, default=False)
    can_view_role = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    
    def has_permission(self, permission):
        """Check if the user has a specific permission across all roles."""
        for role in self.roles:
            if getattr(role, permission, False):
                return True
        return False
    
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )
    
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)

    def __str__(self):
        return self.email

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())

    author = db.relationship('User', backref=db.backref('news', lazy=True))

    def __str__(self):
        return self.title
    
class Galerie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    path = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    
    author = db.relationship('User', backref=db.backref('galeries', lazy=True))

    def __str__(self):
        return self.title

class Docs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)

    path = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('docs_types.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())

    author = db.relationship('User', backref=db.backref('docs', lazy=True))
    doc_type = db.relationship('Docs_types', backref=db.backref('docs', lazy=True))

    def __str__(self):
        return self.title
    
class Docs_types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __str__(self):
        return self.name
    
class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_title = db.Column(db.String(100), nullable=False, unique=True)

    nav_title = db.Column(db.String(255), nullable=True)
    
    home_text = db.Column(db.String(255), nullable=True)

    path = db.Column(db.String(255), nullable=True)

    def __str__(self):
        return self.name

# Delete hooks for models, delete files if models are getting deleted
@listens_for(Home, "after_delete")
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path_icons, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

@listens_for(Docs, "after_delete")
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path_docs, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

@listens_for(Galerie, "after_delete")
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path_galeria, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path_galeria, form.thumbgen_filename(target.path)))
        except OSError:
            pass
