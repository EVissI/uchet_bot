import asyncio
from datetime import datetime, timezone
import os
import flask
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from app.config import setup_logger
from app.flask_admin.model_view import (CheckModelView, ObjectCheckModelView,
ObjectModelView, ToolModelView,MaterialReminderModelView,UserModelView,ChecksMenuView,
DocumentsMenuView, ObjectDocumentModelView, UserDocumentModelView)
from app.flask_admin.model_view.logs import AdminActionLogView
from app.flask_admin.model_view.notification import ForemanNotificationView, NotificationsMenuView, WorkerNotificationView
from app.flask_admin.model_view.profit_accounting import ObjectProficAccountingModelView, ProficAccountingModelView

logger = setup_logger("admin_panel")
from loguru import logger

from flask import Flask
from flask_admin import Admin,AdminIndexView
from flask_admin.form import SecureForm
from app.db.database import sync_session
from app.db.models import AdminActionLog, AdminUser, Check, ForemanNotification, MaterialReminder, Object, ObjectCheck, ObjectDocument, ObjectProficAccounting, ProficAccounting, Tool, User, UserDocument, WorkerNotification

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)
app.config['SECRET_KEY'] = 'AJKClasc6x5z1i2S3Kx3zcdo23'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'



@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with sync_session() as session:
            user = session.query(AdminUser).filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                flask.session['admin_id'] = user.id
                flask.session['admin_username'] = user.username
                flask.session['logged_in'] = True
                flask.session['login_time'] = datetime.now().isoformat()
                
                user.last_login = datetime.now()
                session.commit()
                
                return redirect(url_for('admin.index'))
                
    return render_template('admin/login.html')

@app.before_request
def check_login():
    if request.endpoint not in ['admin_login', 'static']:
        if not flask.session.get('logged_in'):
            return redirect(url_for('admin_login'))
        
        login_time = flask.session.get('login_time')
        if login_time:
            login_time = datetime.fromisoformat(login_time)
            time_diff = datetime.now(timezone.utc) - login_time.replace(tzinfo=timezone.utc)
            
            if time_diff.total_seconds() > 1800:
                flask.session.clear()
                return redirect(url_for('admin_login'))
            
            flask.session['login_time'] = datetime.now().isoformat()

@app.route('/logout')
def logout():
    flask.session.clear()  
    return redirect(url_for('admin_login'))

class MyAdminIndexView(AdminIndexView):
    form_base_class = SecureForm
    def is_visible(self):
        return False

admin = Admin(
    app,
    name='Учет',
    template_mode='bootstrap4',
    index_view=MyAdminIndexView(),
)


admin.add_view(UserModelView(User,sync_session,name = 'Пользователи'))
admin.add_view(ToolModelView(Tool, sync_session, name='Инструменты'))
admin.add_view(ObjectModelView(Object,sync_session,name='Объекты'))
admin.add_view(ChecksMenuView(name='Чеки', endpoint='checks_menu'))
admin.add_view(CheckModelView(Check, sync_session, name='Чеки без объекта', endpoint='check',category='Чеки'))
admin.add_view(ObjectCheckModelView(ObjectCheck, sync_session, name='Чеки по объектам', endpoint='objectcheck',category='Чеки'))
admin.add_view(MaterialReminderModelView(MaterialReminder, sync_session, name='Остатки материалов'))
admin.add_view(DocumentsMenuView(name='Документы', endpoint='doc_menu'))
admin.add_view(UserDocumentModelView(UserDocument, sync_session, name='Документы сотрудников', endpoint='userdocument'))
admin.add_view(ObjectDocumentModelView(ObjectDocument, sync_session, name='Документы объектов', endpoint='objectdocument'))
admin.add_view(AdminActionLogView(AdminActionLog, sync_session, name='История действий',endpoint='admin_logs'))
admin.add_view(NotificationsMenuView(name='Уведомления', endpoint='notifications_menu'))
admin.add_view(WorkerNotificationView(
    WorkerNotification, 
    sync_session, 
    name='Уведомления рабочих', 
    endpoint='workernotification',
    category='Уведомления'
))
admin.add_view(ForemanNotificationView(
    ForemanNotification, 
    sync_session, 
    name='Уведомления бригадиров', 
    endpoint='foremannotification',
    category='Уведомления'
))
admin.add_view(ProficAccountingModelView(ProficAccounting, sync_session, name='Учет прибыли (общие)'))
admin.add_view(ObjectProficAccountingModelView(ObjectProficAccounting, sync_session, name='Учет прибыли (по объектам)', endpoint='object_profic_accounting'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2434)