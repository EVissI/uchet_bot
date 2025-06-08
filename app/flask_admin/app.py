import asyncio
from datetime import datetime, timezone
import os
import flask
from flask import Flask, request, redirect, url_for, render_template
from app.config import setup_logger
from app.flask_admin.model_view import (CheckModelView, ObjectCheckModelView,
ObjectModelView, ToolModelView,MaterialReminderModelView,UserModelView,ChecksMenuView,
DocumentsMenuView, ObjectDocumentModelView, UserDocumentModelView)

logger = setup_logger("admin_panel")
from flask import Flask
from flask_admin import Admin,AdminIndexView
from flask_admin.form import SecureForm
from app.db.database import sync_session
from app.db.models import Check, MaterialReminder, Object, ObjectCheck, ObjectDocument, Tool, User, UserDocument

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

app.config['SECRET_KEY'] = 'AJKClasc6x5z1i2S3Kx3zcdo23'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '123' and password == '123':
            flask.session['logged_in'] = True
            flask.session['login_time'] = datetime.now()
            return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid credentials!')  
    return render_template('login.html') 

@app.before_request
def check_login():
    if not flask.session.get('logged_in') and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))
    elif flask.session.get('logged_in'):
        login_time = flask.session.get('login_time')
        if login_time:
            login_time = datetime.fromisoformat(login_time) if isinstance(login_time, str) else login_time
            time_diff = datetime.now(timezone.utc) - login_time.replace(tzinfo=timezone.utc)
            if time_diff.total_seconds() > 1800:  
                flask.session.clear()
                return redirect(url_for('login'))

            flask.session['login_time'] = datetime.now()


@app.route('/logout')
def logout():
    flask.session.clear()  
    return redirect(url_for('login'))

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
admin.add_view(CheckModelView(Check, sync_session, name='Чеки (без объекта)', endpoint='check'))
admin.add_view(ObjectCheckModelView(ObjectCheck, sync_session, name='Чеки по объектам', endpoint='objectcheck'))
admin.add_view(MaterialReminderModelView(MaterialReminder, sync_session, name='Остатки материалов'))
admin.add_view(DocumentsMenuView(name='Документы', endpoint='doc_menu'))
admin.add_view(UserDocumentModelView(UserDocument, sync_session, name='Документы сотрудников', endpoint='userdocument'))
admin.add_view(ObjectDocumentModelView(ObjectDocument, sync_session, name='Документы объектов', endpoint='objectdocument'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2434)