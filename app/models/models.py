from app.ext.db import db
from datetime import datetime
from flask_security import RoleMixin, UserMixin, current_user
from flask_admin import form

import os
import os.path as op
from sqlalchemy.event import listens_for
from app.helpers.helpes import file_path

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

    # Permissions as boolean fields News_types
    can_create_news_types = db.Column(db.Boolean, default=False)
    can_edit_news_types = db.Column(db.Boolean, default=False)
    can_delete_news_types = db.Column(db.Boolean, default=False)
    can_view_news_types = db.Column(db.Boolean, default=False)

    # Permissions as boolean fields Gallery_types
    can_create_gallerie_types = db.Column(db.Boolean, default=False)
    can_edit_gallerie_types = db.Column(db.Boolean, default=False)
    can_delete_gallerie_types = db.Column(db.Boolean, default=False)
    can_view_gallerie_types = db.Column(db.Boolean, default=False)

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
    content = db.Column(db.Text)

    path = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    news_type_id = db.Column(db.Integer, db.ForeignKey('news_types.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    
    author = db.relationship('User', backref=db.backref('news', lazy=True))

    news_type = db.relationship('News_types', backref=db.backref('news', lazy=True))
    
    def format_brazilian_datetime(self, date_time):
        """Formats a datetime object to Brazilian format (dd/mm/yyyy HH:MM:SS)."""
        return date_time.strftime('%d/%m/%Y %H:%M:%S')
    
    def __str__(self):
        return self.title

class Galerie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    path = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gallerie_type_id = db.Column(db.Integer, db.ForeignKey('gallerie_types.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.today())
    updated_at = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())
    
    gallerie_type = db.relationship('Gallerie_types', backref=db.backref('gallerie', lazy=True))
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

    publico = db.Column(db.Boolean(), default=False)

    def __str__(self):
        return self.name

class News_types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    publico = db.Column(db.Boolean(), default=False)

    def __str__(self):
        return self.name

class Gallerie_types(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    publico = db.Column(db.Boolean(), default=False)

    def __str__(self):
        return self.name

class Sobre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    titulo = db.Column(db.String(255), nullable=True)
    
    conteudo = db.Column(db.String, nullable=True)
    
    def __str__(self):
        return self.titulo

# Delete hooks for models, delete files if models are getting deleted

@listens_for(Docs, "after_delete")
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

@listens_for(Galerie, "after_delete")
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path, form.thumbgen_filename(target.path)))
        except OSError:
            pass
