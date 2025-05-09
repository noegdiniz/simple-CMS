from flask_admin.contrib.sqla import ModelView
from app.models.models import Sobre, User, News, Galerie, Docs, Docs_types, Role, User, News_types, Gallerie_types
from flask import redirect, url_for, request, abort
from flask_security import current_user, login_required
from flask_admin import helpers as admin_helpers
from app.login.login import security
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose, form
from markupsafe import Markup
from app.ext import db
from datetime import date

from app.helpers.helpes import file_path
from wtforms import fields
from wtforms import widgets
from flask_admin.model import typefmt


def date_format(view, value):
    return value.strftime('%d.%m.%Y %H:%M')
    
MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    date: date_format
})

# define a custom wtforms widget and field.
# see https://wtforms.readthedocs.io/en/latest/widgets.html#custom-widgets
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes and set display to none
        existing_classes = kwargs.pop("class", "") or kwargs.pop("class_", "")
        kwargs["class"] = "{} {}".format(existing_classes, "editor")
        kwargs["style"] = "display: none;"
        return super().__call__(field, **kwargs)

class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()

class RootModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS

    @staticmethod
    def _user_formatter(view, context, model, name):
        if model.updated_at:
           markupstring = "<a href='%s'>%s</a>" % (model.url, model.urltitle)
           return Markup(markupstring)
        else:
           return ""

    column_formatters = {
        'url': _user_formatter
    }

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not
        accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))
    
class AdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(AdminIndexView, self).index()

    def is_accessible(self):
        return current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not
        accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))

# Create customized model view class
class UserAdmin(RootModelView):
    column_list = ['username','email','active', 'roles']
    form_columns = ['username', 'email', 'active', 'roles']

    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_user')
    
    def can_create(self):
        return current_user.has_permission('can_create_user')

    def can_edit(self):
        return current_user.has_permission('can_edit_user')

    def can_delete(self):
        return current_user.has_permission('can_delete_user')
    
class NewsAdmin(RootModelView):
    form_overrides = {"content": CKTextAreaField}
    create_template = "create_page.html"
    edit_template = "edit_page.html"

    form_columns = ['title', 'content', 'path', 'news_type']

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ""

        return Markup(
            '<img src="{}">'.format(
                url_for("static", filename=form.thumbgen_filename(model.path))
            )
        )

    column_formatters = {"path": _list_thumbnail}

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        "path": form.ImageUploadField(
            "Image", base_path=file_path, thumbnail_size=(100, 100, True)
        )
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_news')
    
    def can_create(self):
        return current_user.has_permission('can_create_news')

    def can_edit(self):
        return current_user.has_permission('can_edit_news')

    def can_delete(self):
        return current_user.has_permission('can_delete_news')

    def on_model_change(self, form, model, is_created):
        if current_user.is_authenticated:
            model.author_id = current_user.id
        super().on_model_change(form, model, is_created)

class GallerieAdmin(RootModelView):
    form_columns = ['title', 'description', 'path', 'content', 'gallerie_type']

    form_overrides = {"content": CKTextAreaField}
    create_template = "create_page.html"
    edit_template = "edit_page.html"

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ""

        return Markup(
            '<img src="{}">'.format(
                url_for("static", filename=form.thumbgen_filename(model.path))
            )
        )

    column_formatters = {"path": _list_thumbnail}

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        "path": form.ImageUploadField(
            "Image", base_path=file_path, thumbnail_size=(100, 100, True)
        )
    }

    def on_model_change(self, form, model, is_created):
        if current_user.is_authenticated:
            model.author_id = current_user.id
        super().on_model_change(form, model, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_gallerie')
    
    def can_create(self):
        return current_user.has_permission('can_create_gallerie')

    def can_edit(self):
        return current_user.has_permission('can_edit_gallerie')

    def can_delete(self):
        return current_user.has_permission('can_delete_gallerie')

class DocsAdmin(RootModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {"path": form.FileUploadField}

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        "path": {"label": "File", "base_path": file_path, "allow_overwrite": False}
    }

    form_columns = ['title', 'path', 'doc_type']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_docs')
    
    def can_create(self):
        return current_user.has_permission('can_create_docs')

    def can_edit(self):
        return current_user.has_permission('can_edit_docs')

    def can_delete(self):
        return current_user.has_permission('can_delete_docs')

    def on_model_change(self, form, model, is_created):
        if current_user.is_authenticated:
            model.author_id = current_user.id
        super().on_model_change(form, model, is_created)
        
class DocsTypesAdmin(RootModelView):
    form_columns = ['name', 'description', 'publico']
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_docs_types')
    
    def can_create(self):
        return current_user.has_permission('can_create_docs_types')

    def can_edit(self):
        return current_user.has_permission('can_edit_docs_types')

    def can_delete(self):
        return current_user.has_permission('can_delete_docs_types')

class GallerieTypesAdmin(RootModelView):
    form_columns = ['name', 'description', 'publico']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_gallerie_types')
    
    def can_create(self):
        return current_user.has_permission('can_create_gallerie_types')

    def can_edit(self):
        return current_user.has_permission('can_edit_gallerie_types')

    def can_delete(self):
        return current_user.has_permission('can_delete_gallerie_types')

class NewsTypesAdmin(RootModelView):
    form_columns = ['name', 'description', 'publico']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_news_types')
    
    def can_create(self):
        return current_user.has_permission('can_create_news_types')

    def can_edit(self):
        return current_user.has_permission('can_edit_news_types')

    def can_delete(self):
        return current_user.has_permission('can_delete_news_types')

class HomeAdmin(RootModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_home')
    
    def can_create(self):
        return current_user.has_permission('can_create_home')

    def can_edit(self):
        return current_user.has_permission('can_edit_home')

    def can_delete(self):
        return current_user.has_permission('can_delete_home')

class RoleAdmin(RootModelView):
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission('can_view_role')
    
    def can_create(self):
        return current_user.has_permission('can_create_role')

    def can_edit(self):
        return current_user.has_permission('can_edit_role')

    def can_delete(self):
        return current_user.has_permission('can_delete_role')

def configure(app):

    # Flask-Admin setup
    admin = Admin(app, name='CMS Admin',index_view=AdminIndexView(), template_mode='bootstrap3', base_template="my_master.html")
    
    admin.add_view(NewsAdmin(News, app.db.session, name='Noticias', category='Conteudo'))
    admin.add_view(GallerieAdmin(Galerie, app.db.session, name='Galeria', category='Conteudo'))
    admin.add_view(DocsAdmin(Docs, app.db.session, name='Documentos', category='Conteudo'))
    admin.add_view(DocsTypesAdmin(Docs_types, app.db.session, name='Tipo Documento', category='Conteudo'))
    
    admin.add_view(GallerieTypesAdmin(Gallerie_types, app.db.session, name='Tipo Galeria', category='Conteudo'))
    admin.add_view(NewsTypesAdmin(News_types, app.db.session, name='Tipo Noticia', category='Conteudo'))
    
    admin.add_view(HomeAdmin(Sobre, app.db.session, name='Home', category='Conteudo'))

    admin.add_view(RoleAdmin(Role, app.db.session, name='Perfil', category='Usuarios/Perfis'))

    admin.add_view(UserAdmin(User, app.db.session, name='Usuarios', category='Usuarios/Perfis'))
    
    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            theme='bootstrap3',
            h=admin_helpers,
            get_url=url_for,
        )
