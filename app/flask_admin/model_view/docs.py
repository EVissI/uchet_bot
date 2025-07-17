from flask_admin.contrib.sqla import ModelView
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SelectField
from app.db.models import Object, ObjectDocument, User
from flask_admin import BaseView, expose
from wtforms.validators import DataRequired

from app.flask_admin.model_view.base import AuthModelView


class DocumentsMenuView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/doc_menu.html")


class ObjectDocumentModelView(AuthModelView):
    can_create = True
    can_edit = False
    can_delete = True

    column_list = ["id", "file_id", "object", "document_type"]
    column_labels = {
        "id": "ID",
        "file_id": "file_id",
        "object": "Объект",
        "document_type": "Тип документа",
    }
    column_searchable_list = ["id", "file_id"]
    column_filters = ["object_id", "document_type"]

    form_columns = ["file_id", "object_select", "document_type", "document_file_type"]
    form_overrides = {
        "file_id": StringField,
        "document_type": SelectField,
    }

    def get_object_query(self):
        return self.session.query(Object).all()

    form_extra_fields = {
        "object_select": QuerySelectField(
            "Объект",
            query_factory=lambda: [],
            get_label="name",
            allow_blank=False,
            validators=[DataRequired()],
        ),
        "document_file_type": SelectField(
            "Тип файла",
            choices=[
                ("photo", "фото"),
                ("pdf", "pdf"),
            ],
            coerce=str,
            validators=[DataRequired()],
        ),
    }

    form_args = {
        "document_type": {
            "label": "Тип документа",
            "choices": [
                ("смета", "смета"),
                ("техническое задание", "техническое задание"),
                ("контакты заказчика", "контакты заказчика"),
            ],
            "coerce": str,
        },
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.object_select.query_factory = self.get_object_query
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.object_select.query_factory = self.get_object_query
        # При редактировании подставляем выбранный объект
        if obj and obj.object:
            form.object_select.data = obj.object
        return form

    def on_model_change(self, form, model, is_created):
        if hasattr(form, "object_select") and form.object_select.data:
            model.object_id = form.object_select.data.id
        if hasattr(form, "document_type") and form.document_type.data:
            model.document_type = ObjectDocument.DocumentType(form.document_type.data)
        if hasattr(form, "document_file_type") and form.document_file_type.data:
            model.document_file_type = ObjectDocument.DocumentFileType(form.document_file_type.data)
        super().on_model_change(form, model, is_created)

    def _object_formatter(self, context, model, name):
        return model.object.name if model.object else "—"
    
    def _document_type_formatter(self, context, model, name):
        choices = dict(self.form_args["document_type"]["choices"])
        doc_type = model.document_type
        key = doc_type.value if hasattr(doc_type, "value") else doc_type
        return choices.get(key, key) if isinstance(choices, dict) else key
    
    def _document_file_type_formatter(self, context, model, name):
        choices = dict([("photo", "фото"), ("pdf", "pdf")])
        doc_file_type = model.document_file_type
        key = doc_file_type.value if hasattr(doc_file_type, "value") else doc_file_type
        return choices.get(key, key)
    
    column_formatters = {
        "object": _object_formatter,
        "document_type": _document_type_formatter,
        "document_file_type": _document_file_type_formatter,
    }

    def is_visible(self):
        return False


class UserDocumentModelView(AuthModelView):
    can_create = True
    can_edit = False
    can_delete = True

    column_list = ["id", "file_id", "user"]
    column_labels = {"id": "ID", "file_id": "file_id", "user": "Пользователь"}
    column_searchable_list = ["id", "file_id"]
    column_filters = ["user_id"]

    form_columns = ["file_id", "user_select"]
    form_overrides = {
        "file_id": StringField,
    }

    def get_user_query(self):
        return self.session.query(User).all()

    form_extra_fields = {
        "user_select": QuerySelectField(
            "Пользователь",
            query_factory=lambda: [],
            get_label="user_enter_fio",
            allow_blank=False,
        )
    }

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.user_select.query_factory = self.get_user_query
        return form

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if hasattr(form, "user_select") and form.user_select.data:
            model.user_id = form.user_select.data.telegram_id
        else:
            model.user_id = None

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else "—"

    column_formatters = {"user": _user_formatter}

    def is_visible(self):
        return False
