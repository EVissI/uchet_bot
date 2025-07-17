from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from loguru import logger
from wtforms import TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from app.db.models import Object, User
from app.flask_admin.model_view.base import AuthModelView


class ChecksMenuView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/checks_menu.html")


class CheckModelView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ["id", "file_id", "amount", "description", "own_expense", "user"]
    column_labels = {
        "id": "ID",
        "file_id": "file_id",
        "amount": "Сумма",
        "description": "Описание",
        "own_expense": "За свой счёт",
        "user": "Пользователь",
    }
    column_searchable_list = ["id", "description", "amount"]
    column_filters = ["own_expense", "user_id"]

    form_columns = ["file_id", "amount", "description", "own_expense", "user_select"]
    form_overrides = {
        "description": TextAreaField,
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

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.user_select.query_factory = self.get_user_query
        return form

    def on_form_prefill(self, form, id):
        check = self.get_one(id)
        if check and check.user:
            form.user_select.data = check.user
        else:
            form.user_select.data = None

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


class ObjectCheckModelView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        "id",
        "file_id",
        "amount",
        "description",
        "own_expense",
        "object",
        "user",
    ]
    column_labels = {
        "id": "ID",
        "file_id": "file_id",
        "amount": "Сумма",
        "description": "Описание",
        "own_expense": "За свой счёт",
        "object": "Объект",
        "user": "Пользователь",
    }
    column_searchable_list = ["id", "description", "amount"]
    column_filters = ["own_expense", "object_id", "user_id"]

    form_columns = [
        "file_id",
        "amount",
        "description",
        "own_expense",
        "object_select",
        "user_select",
    ]
    form_overrides = {
        "description": TextAreaField,
    }


    form_extra_fields = {
        "object_select": QuerySelectField(
            "Объект",
            query_factory=lambda: [],
            get_label="name",
            allow_blank=False,
        ),
        "user_select": QuerySelectField(
            "Пользователь",
            query_factory=lambda: [],
            get_label="user_enter_fio",
            allow_blank=False,
        ),
    }
    def get_object_query(self):
        return self.session.query(Object).all()

    def get_user_query(self):
        return self.session.query(User).all()

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.object_select.query_factory = self.get_object_query
        form.user_select.query_factory = self.get_user_query
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.object_select.query_factory = self.get_object_query
        form.user_select.query_factory = self.get_user_query
        return form

    def on_form_prefill(self, form, id):
        check = self.get_one(id)
        if check and check.object:
            form.object_select.data = check.object
        else:
            form.object_select.data = None
        if check and check.user:
            form.user_select.data = check.user
        else:
            form.user_select.data = None
    def on_model_change(self, form, model, is_created):
        logger.info("object_select.data:", form.object_select.data)
        logger.info("user_select.data:", form.user_select.data)
        super().on_model_change(form, model, is_created)
        if hasattr(form, "object_select") and form.object_select.data:
            model.object_id = form.object_select.data.id
        else:
            model.object_id = None
        if hasattr(form, "user_select") and form.user_select.data:
            model.user_id = form.user_select.data.telegram_id
        else:
            model.user_id = None

    def _description_formatter(self, context, model, name):
        text = getattr(model, name) or ""
        return (text[:80] + "...") if len(text) > 80 else text

    def _object_formatter(self, context, model, name):
        return model.object.name if model.object else "—"

    def _user_formatter(self, context, model, name):
        return model.user.user_enter_fio if model.user else "—"

    column_formatters = {
        "description": _description_formatter,
        "object": _object_formatter,
        "user": _user_formatter,
    }

    def is_visible(self):
        return False