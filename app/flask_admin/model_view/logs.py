from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from datetime import datetime
import json

from markupsafe import Markup
from app.db.models import AdminUser, User, Object, Tool, ObjectDocument
from app.db import models  # Импортируем все модели
from sqlalchemy.inspection import inspect
from app.flask_admin.model_view.base import AuthModelView


class AdminActionLogView(AuthModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = [
        "id",
        "admin_user",
        "action",
        "model",
        "record_id",
        "created_at",
        "details",
    ]
    column_labels = {
        "id": "ID",
        "admin_user": "Администратор",
        "action": "Действие",
        "model": "Сущность",
        "record_id": "ID записи",
        "created_at": "Дата и время",
        "details": "Детали",
    }

    column_filters = ["admin_user.username", "action", "model", "created_at"]

    column_searchable_list = ["model", "action", "admin_user.username"]

    column_default_sort = ("created_at", True)

    FIELD_TRANSLATIONS = {
        "name": "Название",
        "description": "Описание",
        "status": "Статус",
        "user_select": "Пользователь",
        "object_select": "Объект",
        "tool_select": "Инструмент",
    }

    VALUE_TRANSLATIONS = {
        "status": {"free": "свободный", "in_work": "занят", "repair": "в ремонте"},
        "document_type": {
            "estimate": "смета",
            "technical_task": "техническое задание",
            "customer_contacts": "контакты заказчика",
        },
        "role": {
            "admin": "Администратор",
            "worker": "Рабочий",
            "foreman": "Бригадир",
            "buyer": "Закупщик",
        },
    }

    def _get_model_class(self, model_name):
        """Получаем класс модели по имени"""
        return getattr(models, model_name, None)

    def _format_model_value(self, model_instance):
        """Форматируем значение модели для отображения"""
        if hasattr(model_instance, "user_enter_fio"):
            return model_instance.user_enter_fio
        if hasattr(model_instance, "name"):
            return model_instance.name
        return str(model_instance)

    def _format_field_value(self, field_name, value):
        """Форматируем значение поля"""
        # Для булевых значений
        if isinstance(value, bool):
            return "Да" if value else "Нет"

        # Для enum-подобных значений
        if field_name in self.VALUE_TRANSLATIONS:
            return self.VALUE_TRANSLATIONS[field_name].get(value, value)

        return value

    def _action_formatter(self, context, model, name):
        action_types = {
            "create": "Создание",
            "edit": "Редактирование",
            "delete": "Удаление",
        }
        return action_types.get(model.action, model.action)

    def _get_model_instance(self, model_class, value):
        """Получаем инстанс модели с учетом разных первичных ключей"""
        if not model_class:
            return None

        primary_key = model_class.__table__.primary_key.columns.keys()[0]

        if model_class == User:
            return (
                self.session.query(User)
                .filter(User.telegram_id == value.get("id"))
                .first()
            )


        return self.session.get(model_class, value.get("id"))

    def _details_formatter(self, context, model, name):
        if not model.details:
            return ""

        try:
            details = (
                json.loads(model.details)
                if isinstance(model.details, str)
                else model.details
            )
            formatted_items = []

            for k, v in (details.get("data", {}) or details.get("changes", {})).items():
                field_name = self.FIELD_TRANSLATIONS.get(k, k)

                if isinstance(v, dict) and "id" in v:
                    try:
                        model_name = k.replace("_select", "").capitalize()
                        if "object at" in str(v):
                            model_name = str(v).split()[0].split(".")[-1]

                        model_class = self._get_model_class(model_name)
                        if model_class:
                            instance = self._get_model_instance(model_class, v)
                            v = (
                                self._format_model_value(instance)
                                if instance
                                else str(v)
                            )
                    except Exception as e:
                        v = str(v)
                else:
                    v = self._format_field_value(k, v)

                if isinstance(v, str):
                    v = v.replace("\n", "<br>")

                formatted_items.append(f"{field_name}: {v}")

            return Markup("<br>".join(formatted_items))
        except Exception as e:
            return str(model.details)

    def _datetime_format(self, context, model, name):
        value = getattr(model, name)
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                return value
        return value.strftime("%d.%m.%Y %H:%M:%S") if value else ""

    def _admin_formatter(self, context, model, name):
        if not model.admin_user:
            return "—"

        try:
            admin = self.session.get(AdminUser, model.admin_user_id)
            return admin.username if admin else f"Admin #{model.admin_user_id}"
        except Exception as e:
            return f"Admin #{model.admin_user_id}"

    column_formatters = {
        "action": _action_formatter,
        "details": _details_formatter,
        "created_at": _datetime_format,
        "admin_user": _admin_formatter,
    }

    column_type_formatters = {}

    column_export_list = [
        "id",
        "admin_user.username",
        "action",
        "model",
        "record_id",
        "created_at",
        "details",
    ]

    def is_visible(self):
        return True
