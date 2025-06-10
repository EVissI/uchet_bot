from datetime import datetime, time
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.flask_admin.model_view.base import AuthModelView
from app.db.models import WorkerNotification, ForemanNotification
from wtforms import TimeField, TextAreaField

class NotificationsMenuView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notifications_menu.html')

class BaseNotificationView(AuthModelView):
    can_create = True
    can_edit = True
    can_delete = True
    
    form_excluded_columns = ['created_at', 'updated_at']
    
    form_overrides = {
        'message': TextAreaField,
        'first_notification_time': TimeField,
        'second_notification_time': TimeField,
    }
    
    column_list = ['message', 'first_notification_time', 'second_notification_time']
    column_labels = {
        'message': 'Сообщение',
        'first_notification_time': 'Время первого уведомления',
        'second_notification_time': 'Время второго уведомления'
    }
    
    form_widget_args = {
        'message': {
            'rows': 5
        }
    }
    def on_model_change(self, form, model, is_created):
        if isinstance(form.first_notification_time.data, time):
            today = datetime.today().date()  
            model.first_notification_time = datetime.combine(today, form.first_notification_time.data)
            
        if isinstance(form.second_notification_time.data, time):
            today = datetime.today().date()  
            model.second_notification_time = datetime.combine(today, form.second_notification_time.data)
           
        super().on_model_change(form, model, is_created)

    def _format_time(self, context, model, name):
        value = getattr(model, name)
        if value:
            return value.strftime('%H:%M') if isinstance(value, (datetime, time)) else str(value)
        return ''

    column_formatters = {
        'first_notification_time': _format_time,
        'second_notification_time': _format_time
    }

class WorkerNotificationView(BaseNotificationView):
    column_description = {
        'message': 'Сообщение для рабочих',
        'first_notification_time': 'Время первого уведомления для рабочих',
        'second_notification_time': 'Время второго уведомления для рабочих'
    }

class ForemanNotificationView(BaseNotificationView):
    column_description = {
        'message': 'Сообщение для бригадиров',
        'first_notification_time': 'Время первого уведомления для бригадиров',
        'second_notification_time': 'Время второго уведомления для бригадиров'
    }