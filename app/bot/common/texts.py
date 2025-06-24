from app.bot.common.utils import escape_html


def get_text(text_code: str, lang: str = "ru", **kwargs) -> str:
    text = ""
    match lang:
        case "ru":
            text = TEXTS_TRANSLITE["ru"].get(text_code, text_code)
        case "uz":
            text = TEXTS_TRANSLITE["uz"].get(text_code, text_code)
        case "tg":
            text = TEXTS_TRANSLITE["tg"].get(text_code, text_code)
        case _:
            text = TEXTS_TRANSLITE["ru"].get(text_code, text_code)
    escaped_kwargs = {key: escape_html(value) for key, value in kwargs.items()}

    return text.format(**escaped_kwargs)


def get_all_texts(text_code: str) -> list[str]:
    __languages = ["ru", "uz", "tg"]
    result = []
    for lang in __languages:
        result.append(TEXTS_TRANSLITE[lang].get(text_code, text_code))
    return result


TEXTS_TRANSLITE = {
    "ru": {
        "object_has_been_deleted": "Объект удален",
        'reminder_delete_canceled': 'Удаление остатков отменено',
        'reminder_deleted': 'Остатки деактивированны',
        'reminder_not_found': 'Остатки не были найденны',
        "start": "Привет, {name}! Я бот",
        "language_select": "Выберите язык:",
        "language_ru": "Русский",
        "language_uz": "Узбекский",
        "language_tg": "Таджикский",
        "request_contact": "Пожалуйста, поделитесь своим номером телефона, с помощью кнопки ниже.",
        "username_instruction": """
Для использования бота необходимо создать юзернейм. Создайте его следуя инструкциям

<b>Как создать username в Telegram:</b>

1. Откройте настройки Telegram
2. Нажмите на "Изменить профиль"
3. Нажмите на поле "Username"
4. Придумайте и введите желаемый username
5. Нажмите галочку ✓ для сохранения

После создания username нажмите кнопку "Проверить" ниже.""",
        "check": "Проверить",
        "create_username": "Создать username",
        "has_no_username": "Следуйте инструкциям, чтобы создать юзернейм",
        "share_contact_btn": "Поделиться контактом 📱",
        "no_contact": "Используйте клавиатуру",
        "cancel": "Отмена",
        "confirm": "Подтвердить",
        "its_no_contact": "Пожалуйста используйте кнопку на клавиатуре",
        "reques_docs": "Скидывайте фотографии документов в чат. Когда загрузите все документы нажмите кнопку 'Прекратить'",
        "stop_upload_btn": "Прекратить",
        "i_got_acquainted_btn": "Я ознакомился",
        "i_got_acquainted": "Если ознакомились со всем нажмите на кнопку 'Я ознакомился'",
        "reques_fio": "Введите ФИО",
        "ru": "Русский",
        "uz": "Узбекский",
        "tg": "Таджитский",
        "photo_received": "Фото получено. Всего загружено: {count}",
        "photos_saved": "Все фотографии ({count}) успешно сохранены!",
        "no_photos": "Вы не загрузили ни одной фотографии",
        "solve_example": "Для подтверждения что вы человек, решите пример:\n{example}",
        "verification_success": "Верификация пройдена успешно! Регистрация завершена.",
        "wrong_answer": "Неверный ответ. Попробуйте решить другой пример:\n{example}",
        "not_a_number": "Пожалуйста, введите число.",
        "report_accepted": "Отчет принят",
        "report_error": "Произошла ошибка при пересылке сообщения.",
        "profile_btn": "Профиль",
        "my_objects_btn": "Мои объекты",
        "material_remainder_btn": "Остаток материалов",
        "out_object_check_btn": "Учет чеков вне объектов",
        'transfer_tool_btn': "Передача инструмента",
        "no_documents": "Для этого объекта не добавлено ни одного документа",
        "material_order_btn": "Заказ материалов",
        "info_btn": "Информация",
        "instructions": "Инструкции по использованию бота",
        "enter_tool_id": "Введите ID инструмента",
        "enter_recipient": "Введите @username или telegram_id получателя:",
        "rules": "Правила использования",
        "profile_info": (
            "👤 <b>Профиль</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "📧 Username: @{username}\n"
            "👨‍💼 ФИО: {full_name}\n"
            "📱 Телефон: {phone}\n"
            "📊 Статус: {role}"
        ),
        "tools_list_btn": "Инструменты",
        "language_select_btn": "Выбор языка",
        "rules_btn": "Правила",
        "no_tools": "За вами не закреплено ни одного инструмента",
        "tools_list_header": "🛠 <b>Список закрепленных инструментов:</b>",
        "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Описание: <i>{description}</i>",
        "no_description": "Описание отсутствует",
        "lang_has_changed": "Язык бота был изменен",
        "no_objects": "У вас нет доступных объектов",
        "objects_list_header": "🏗 <b>Ваши объекты:</b>",
        "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
        "navigation_btn": "📍 Навигация",
        "documentation_btn": "📄 Документация",
        "notify_object_btn": "📢 Оповестить объект",
        "object_photo_btn": "📸 Фото с объекта",
        "object_checks_btn": "🧾 Учет чеков",
        "no_navigation": "Навигация для этого объекта не добавлена",
        "enter_notification": "Введите сообщение для отправки всем участникам объекта",
        "notification_format": (
            "📢 <b>Уведомление с объекта {object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {sender_name}\n"
            "📧 Username: {username}\n\n"
            "💬 <b>Сообщение:</b>\n<i>{message}</i>"
        ),
        "notification_sent": "✅ Уведомление отправлено всем участникам объекта",
        "send_object_photo": "📸 Отправьте фотографию с объекта",
        "enter_photo_description": "📝 Введите описание к фотографии",
        "object_photo_format": (
            "📸 <b>Фото с объекта #{object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b>\n<i>{description}</i>"
        ),
        "photo_sent": "✅ Фото успешно отправлено",
        "send_photo_only": "❌ Пожалуйста, отправьте фотографию",
        "send_check_photo_and_description": "📸 Отправьте фото и описание чека",
        "enter_check_amount": "💰 Введите сумму чека (только цифры)",
        "invalid_amount": "❌ Неверный формат суммы. Введите число, например: 1234.56",
        "check_format": (
            "🧾 <b>Чек с объекта #{object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "💰 <b>Сумма:</b> {amount} руб."
        ),
        "check_saved": "✅ Чек успешно сохранен",
        "enter_material_order": "📝 Опишите какие материалы вам нужны",
        "enter_delivery_date": "📅 Укажите желаемую дату доставки (формат: ДД.ММ.ГГГГ)",
        "date_must_be_future": "❌ Дата доставки должна быть в будущем",
        "invalid_date": "❌ Некорректная дата",
        "invalid_date_format": (
            "❌ Неверный формат даты\n\n"
            "Используйте формат: ДД.ММ.ГГГГ\n"
            "Например: 25.05.2024"
        ),
        "material_order_format": (
            "🛍 <b>Заказ материалов</b>\n\n"
            "👤 <b>Заказчик:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Требуемые материалы:</b>\n<i>{description}</i>\n"
            "📅 <b>Желаемая дата:</b> <i>{delivery_date}</i>"
        ),
        "order_saved": "✅ Заказ материалов успешно отправлен",
        "send_material_photo": "📸 Отправьте фото материала",
        "enter_material_description": "📝 Введите описание материала",
        "enter_storage_location": "📍 Укажите место хранения материала",
        "material_remainder_format": (
            "📦 <b>Остаток материала</b>\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "📍 <b>Место хранения:</b> <i>{location}</i>"
        ),
        "material_saved": "✅ Информация о материале сохранена",
        "confirm_transfer_tool": "Подтвердите передачу инструмента:",
        "transfer_tool_forced": "Инструмент принудительно передан выбранному пользователю.",
        "transfer_tool_invalid_format": "Неверный формат команды. Используйте: /transfer_tool <ID инструмента> <получатель> <описание>",
        "transfer_tool_invalid_tool_id": "ID инструмента должно быть числом.",
        "transfer_tool_not_found": "Инструмент с указанным ID не найден.",
        "transfer_tool_format": (
            "Передача инструмента:\n"
            "Инструмент: {tool_name} (ID: {tool_id})\n"
            "Получатель: {recipient}\n"
            "Отправитель: {sender}\n"
        ),
        "transfer_tool_request_sent": "Запрос на передачу инструмента отправлен.",
        "accept_tool_btn": "получить инструмент",
        "transfer_tool_receive_prompt": "Вам передают инструмент {tool_name}. Нажмите кнопку ниже, чтобы получить его.",
        "transfer_tool_recipient_not_found": "Не удалось найти пользователя с таким именем.",
        "transfer_tool_invalid_recipient": "Получатель должен быть указан через @username или telegram_id.",
        "tool_received_confirmation": "Инструмент получен!",
        "objects_btn": "Объекты",
        "report_empty_text": "Пожалуйста, введите текст отчета после команды /report",
        "report_format": (
            "Новый отчет от {sender} ({username}):\n\n"
            "{report}"
        ),
        "report_sent_confirmation": "Ваш отчет отправлен.",
        "foreman_workers_btn": "Рабочие",
        "foreman_documentation_btn": "Документация",
        "foreman_photos_btn": "Фото с объекта",
        "foreman_handover_btn": "Сдача объекта",
        "foreman_procurement_btn": "Закупка",
        "foreman_receipts_btn": "Учет чеков",
        "foreman_material_balance_btn": "Остаток материала",
        "foreman_info_btn": "Информация",
        "foreman_tools_list_btn": "Перечень инструментов",
        "foreman_mass_mailing_btn": "Рассылка по объекту",
        "foreman_offsite_accounting_btn": "Учёт вне объекта",
        "foreman_export_xlsx_btn": "Выгрузка xlsx по объекту",
        "select_object_prompt": "Пожалуйста, выберите объект:",
        "no_objects": "У вас нет доступных объектов",
        "back_btn": "Назад",
        "no_object_members": "Для выбранного объекта нет закрепленных рабочих.",
        "worker_info_format": (
            "Телеграм ID: {telegram_id}\n"
            "Username: {username}\n"
            "ФИО: {full_name}\n"
            "Телефон: {phone}\n"
            "Статус: {status}\n"
            "Объект: {object_name}"
        ),
        "select_object_action": "Выберите действие с объектом",
        "no_object_documents": "Для данного объекта не добавлено ни одной документации",
        "document_info_format": (
            "Тип документа: {document_type}\n"
            "Закреплен за объектом: {object_name}\n"
        ),
        "enter_handover_description": "Введите описание сдачи объекта:",
        "object_not_found": "Объект не найден",
        "handover_format": (
            "🏗 <b>Сдача объекта</b>\n\n"
            "🏢 Объект: {object_name} (ID: {object_id})\n"
            "👤 Прораб: {foreman_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b>\n{description}"
        ),
        "handover_sent": "✅ Информация о сдаче объекта успешно отправлена",
        "own_expense_true_btn": "За свой счет - ✔",
        "own_expense_false_btn": "За свой счет - ❌",
        "expense_sheet_name": "Отчет по расходам",
        "date_column": "Дата",
        "description_column": "Описание",
        "amount_column": "Сумма",
        "expense_type_column": "Тип расхода",
        "user_column": "Пользователь",
        "own_expense": "За свой счет",
        "company_expense": "За счет компании",
        "total_amount": "Итого:",
        "prev_page_btn": "Предыдущая",
        "next_page_btn": "Следующая",
        "mock_data_cleared": "Все тестовые данные удалены",
        "invalid_photo_format": "Пожалуйста, отправьте фотографию",
        "no_workers_found": "Нет доступных рабочих в базе данных",
        "expense_report_caption": "Отчет по расходам\nПериод: {start_date} - {end_date}\nТип: {expense_type}",
        "no_expenses_found": "За указанный период расходов не найдено",
        "all_expenses_btn": "Все расходы",
        "own_expenses_btn": "За свой счёт",
        "company_expenses_btn": "За счет компании",
        "enter_start_date": "📅 Введите начальную дату отчетного периода (формат: ДД.ММ.ГГГГ)",
        "enter_end_date": "📅 Введите конечную дату отчетного периода (формат: ДД.ММ.ГГГГ)",
        "select_expense_type": "Выберите тип расходов для выгрузки:",
        "invalid_date_format": "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например: 25.12.2024)",
        "expense_report_caption": (
            "📊 Отчет по расходам\n"
            "📅 Период: {start_date} - {end_date}\n"
            "💰 Тип расходов: {expense_type}"
        ),
        "report_processing": "⏳ Формирование отчета...",
        "report_generation_error": "❌ Ошибка при формировании отчета",
        "all_expenses": "Все расходы",
        "own_expenses": "За свой счет",
        "company_expenses": "За счет компании",
        "excel_date_column": "Дата",
        "excel_description_column": "Описание",
        "excel_amount_column": "Сумма",
        "excel_expense_type_column": "Тип расхода",
        "excel_user_column": "Пользователь",
        "excel_total_row": "ИТОГО:",
        "excel_sheet_name": "Отчет по расходам",
        "reminder_out_btn": "Учет чеков вне объектов",
        "tools_list_caption": "📊 Отчет по инструментам\n💼 Тип: {tool_status}",
        "select_tool_status": "Выберите тип инструментов для выгрузки:",
        "all_tools": "Все инструменты",
        "in_work_tools": "Инструменты в работе",
        "free_tools": "Свободные инструменты",
        "repair_tools": "Инструменты в ремонте",
        "no_tools_found": "❌ Инструменты не найдены",
        "excel_tool_name": "Наименование",
        "excel_tool_description": "Описание",
        "excel_tool_status": "Статус",
        "excel_tool_user": "Закреплен за",
        "excel_tool_date": "Дата назначения",
        "excel_tools_sheet_name": "Перечень инструментов",
        "no_users_found": "❌ Пользователи не найдены",
        "no_objects_found": "❌ Объекты не найдены",
        "no_members_found": "❌ На объекте нет участников",
        "select_object_for_notification": "📋 Выберите объект для рассылки уведомления:",
        "enter_notification_text": "📝 Введите текст уведомления для рассылки:",
        "sending_notifications_status": "📤 Отправка уведомлений... {sent}/{total}",
        "notifications_sent_status": "✅ Рассылка завершена\n\n📊 Всего: {total}\n✅ Успешно: {success}\n❌ Не доставлено: {failed}",
        "admin_notify_all_users_inline_btn": "📢 Всем пользователям",
        "admin_notify_object_inline_btn": "🏗 По объекту",
        "admin_notify_all_user_w8_message": "📝 Введите текст для рассылки всем пользователям:",
        "transfer_tool_force_format": (
            "🔄 Принудительная передача инструмента\n"
            "🛠 Инструмент: {tool_name} (ID: {tool_id})\n"
            "👤 Получатель: {recipient}\n"
            "👨‍💼 Администратор: {admin}\n"
            "📝 Описание: {description}"
        ),
        "transfer_tool_force_complete": "✅ Инструмент принудительно передан",
        "transfer_tool_force_received": "🔄 Администратор {admin} передал вам инструмент: {tool_name}",
        "transfer_tool_admin_format": (
            "Формат команды:\n"
            "/transfer_tool <инструмент_ID> <получатель> <описание>\n"
            "Для принудительной передачи (только админы):\n"
            "/transfer_tool <инструмент_ID> <получатель> -f <описание>"
        ),
        "admin_notify": "Выберите тип рассылки:",
        "create_object_name": "📝 Введите название объекта:",
        "operation_cancelled": "❌ Операция отменена",
        'user_has_no_tools': 'За пользователем не закрепленны инструменты',
        "caption_required": "❌ Необходимо добавить описание к фото в подписи",
        "select_document_type": "Выберите тип документа:",
        "doc_type_estimate": "📊 Смета",
        "doc_type_technical": "📋 Техническое задание", 
        "doc_type_contacts": "📞 Контакты заказчика",
        "create_object_success": "✅ Объект успешно создан",
        "notification_sent_to_all": "✅ Уведомление отправлено всем пользователям",
        "create_object_no_documents": "❌ Документы не были загружены",
        "create_object_description": "📝 Введите описание объекта:",
        "pagination_error": "❌ Ошибка при обновлении страницы",
        "objects_list": "📋 Список объектов:",
        "object_name": "Объект: {name}",
        "updated_success": "✅ Данные успешно обновлены",
        "error_occurred": "❌ Произошла ошибка",
        "document_upload_complete": "✅ Загрузка документов завершена",
        "document_type_selected": "✅ Тип документа выбран",
        "document_saved": "✅ Документ сохранен",
        "upload_more_documents": "📤 Загрузите следующий документ или нажмите 'Завершить'",
        "foreman_panel": "👨‍💼 Панель прораба",
        "object_members_header": "👥 Участники объекта:",
        "member_item_format": (
            "👤 {full_name}\n"
            "📱 {phone}\n"
            "📧 @{username}"
        ),
        "admin_panel": "👨‍💼 Панель администратора",
        "object_control": "🏗 Управление объектами",
        "user_control": "👥 Управление пользователями",
        "create_object_btn": "Создать объект",
        "edit_object_btn": "✏️ Редактировать объект",
        "delete_object_btn": "Удалить объект",
        "access_denied": "❌ Доступ запрещен",
        "invalid_input": "❌ Неверный ввод",
        "action_cancelled": "❌ Действие отменено",
        "try_again": "🔄 Попробуйте снова",
        "processing": "⏳ Обработка...",
        "saving_data": "💾 Сохранение данных...",
        "loading_data": "📥 Загрузка данных...",
        "tool_status_active": "✅ В работе",
        "tool_status_free": "🆓 Свободен",
        "tool_status_repair": "🔧 В ремонте",
        "tool_transfer_success": "✅ Инструмент успешно передан",
        "object_active": "✅ Активен",
        "object_completed": "🏁 Завершен",
        "object_suspended": "⏸ Приостановлен",
        "confirm_action": "Подтвердите действие:",
        "confirm_delete": "❗️ Подтвердите удаление",
        "confirm_cancel": "❗️ Подтвердите отмену",
        "tmc_template_instruction": (
            "📝 Инструкция по заполнению:\n\n"
            "1. Наименование* - название инструмента\n"
            "2. Количество* - число единиц\n"
            "3. Описание - дополнительная информация\n"
            "4. Статус - свободный/занят/в ремонте\n"
            "5. File ID - ID фото инструмента\n\n"
            "* - обязательные поля"
        ),
        "tmc_template_sheet": "Шаблон инструментов",
        "excel_tool_quantity": "Количество*", 
        "excel_tool_file_id": "File ID фото",
        "tmc_enter_name": "📝 Введите наименование инструмента",
        "tmc_enter_quantity": "🔢 Введите количество инструментов",
        "tmc_enter_file": "🔢 Загрузите картинку инструмента",
        "tmc_enter_description": "📝 Введите описание инструмента (необязательно)",
        "tmc_upload_complete": "✅ Добавлено инструментов: {name} x{count}",
        "tmc_file_error": "❌ Ошибка при обработке файла",
        "excel_tool_id": "ID инструмента",
        "excel_recipient_username": "Id пользователя или юзернейм",
        "tmc_invalid_quantity": "❌ Количество должно быть положительным числом",
        "tmc_save_error": "❌ Ошибка при сохранении инструментов",
        "materials_sheet_name": "Остатки материалов",
        "excel_material_id": "ID",
        "excel_material_description": "Описание",
        "excel_material_location": "Место хранения",
        "no_materials_found": "❌ Материалы не найдены",
        "materials_export_complete": "✅ Выгружено материалов: {count}",
        "materials_export_error": "❌ Ошибка при выгрузке материалов",
        "material_card_format": (
            "📦 Материал #{id}\n\n"
            "📝 Описание: {description}\n"
            "📍 Место хранения: {location}\n"
        ),
        "send_photo_for_file_id": "📸 Отправьте фото для получения File ID",
        "file_id_generated": "✅ File ID сгенерирован:\n{file_id}",
        "file_id_generation_error": "❌ Ошибка при генерации File ID",
        "stop_btn": "⛔️ Прекратить",
        "generate_file_id_btn": "🆔 Получить File ID",
        "materials_excel_btn": "📊 Выгрузить остатки",
        "bulk_transfer_btn": "📦 Массовая передача",
        "template_error": "❌ Ошибка при создании шаблона",
        "template_instruction": "📝 Заполните шаблон согласно инструкции и загрузите обратно",
        "bulk_transfer_instruction": "📝 Инструкция по массовой передаче инструментов",
        "bulk_transfer_report": (
            "📊 Отчет о передаче:\n\n"
            "✅ Успешно:\n{success}\n\n"
            "❌ Ошибки:\n{failed}"
        ),
        "bulk_transfer_no_file": "❌ Файл не загружен",
        "bulk_transfer_complete": "✅ Передача инструментов завершена",
        "check_out_object_format": (
            "🧾 <b>Чек вне объекта</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "💰 <b>Сумма:</b> {amount} руб."
        ),
        "choose_reminder": (
            "📦 <b>Информация о материале:</b>\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "📍 <b>Место хранения:</b> <i>{storage_location}</i>\n"
        ),
        "send_file": "📤 Отправьте файл",
        "file_processing": "⏳ Обработка файла...",
        "file_error": "❌ Ошибка при обработке файла",
        "enter_new_photo": "📸 Отправьте новое фото",
        "reminder_photo_updated": "✅ Фото материала обновлено",
        "reminder_description_updated": "✅ Описание материала обновлено",
        "reminder_location_updated": "✅ Место хранения обновлено",
        "excel_bulk_transfer_sheet": "Массовая передача",
        "excel_bulk_transfer_tool_id": "ID инструмента*",
        "excel_bulk_transfer_recipient": "Получатель*",
        "excel_bulk_transfer_description": "Описание",
        "invalid_recipient": "❌ Неверно указан получатель",
        "invalid_tool_id": "❌ Неверный ID инструмента",
        "tool_not_found": "❌ Инструмент не найден",
        "recipient_not_found": "❌ Получатель не найден",
        "success_transfer": "✅ Успешно передано",
        "out_object_check_saved": "✅ Чек сохранен и отправлен в группу",
        "profic_accounting_btn": "Учет прибыли",
        "select_object_for_profic": "📋 Выберите объект для учета:",
        "select_payment_type": "💳 Выберите тип операции:",
        "enter_payment_amount": "💰 Введите сумму:",
        "enter_payment_purpose": "📝 Введите назначение платежа:",
        "invalid_amount": "❌ Неверный формат суммы. Введите число, например: 1234.56",
        "profic_saved": "✅ {type} на сумму {amount} руб. добавлен",
        "profic_save_error": "❌ Ошибка при сохранении операции",
        "reminder_out_object_btn": "Остатки вне объекта",
        "instrument_control_btn": "Управление инструментами",
        "material_remainder_control_btn": "Управление остатками материала",
        "reminder_btn": "Остатки",
        "object_control_btn": "Управление объектами",
        "notify_btn": "Уведомления",
        "cancel_btn": "❌ Отмена",
        "add_worker_to_object_btn": "Добавить рабочего",
        "bulk_transfer_btn": "Массовая передача",
        "user_tools_list_btn": "Список инструментов",
        "change_reminder_btn": "✏️ Изменить остатки",
        "deactivate_reminder_btn": "❌ Деактивировать остатки",
        "create_material_reminder_btn": "➕ Создать остатки",
        "excel_view_btn": "📊 Excel выгрузка",
        "change_deactivate_btn": "✏️ Изменить/Деактивировать",
        "add_worker_to_object_text": "📋 Выберите объект, куда нужно добавить рабочего:",
        "add_worker_to_object_w8_ids": (
            "🏗 Объект: <b>{object_name}</b>\n\n"
            "📝 Введите Telegram ID рабочих через запятую (например: 123456789, 987654321)"
        ),
        "no_valid_user_ids": "❌ Не найдено корректных Telegram ID",
        "no_valid_users_found": "❌ Не найдено пользователей с указанными ID",
        "members_added_successfully": (
            "📊 Результат добавления рабочих:\n\n"
            "✅ Успешно добавлено: {success_count}\n"
            "❌ Не добавлено: {failed_count}\n\n"
            "❗️ Причины отказа:\n"
            "{failed_reasons}"
        ),
        "enter_new_description": "📝 Введите новое описание",
        "reminder_deactivated": "✅ Напоминание деактивировано",
        "reminder_updated": "✅ Напоминание обновлено",
        "object_control_title": "🏗 Управление объектами",
        "object_deleted": "✅ Объект удален",
        "object_updated": "✅ Данные объекта обновлены",
        "added_to_object_notification": (
            "👋 Вас добавили на новый объект!\n\n"
            "🏗 <b>Объект:</b> {object_name}\n"
            "ℹ️ Теперь вы можете видеть этот объект в разделе 'Мои объекты'"
        ),
        "create_object_documents": "📸 Загрузите фотографии документов по объекту.\n\nКогда загрузите все документы, нажмите 'Прекратить'",
        "create_object_document_has_received": "✅ Документ получен. Продолжайте загрузку или нажмите 'Прекратить'",
        "create_object_document_no_received": "❌ Пожалуйста, отправьте фотографию документа",
        "doc_type_select": "🔍 Выберите тип документа:",
        "doc_type_контакты заказчика": "📞 Контакты заказчика",
        "doc_type_смета": "📊 Смета",
        "doc_type_техническое задание": "📋 Техническое задание",
        "doc_type_other": "📄 Другое",
        "create_object_uploading": "📤 Загрузка документов...",
        "create_object_saving": "💾 Сохранение объекта...",
        "create_object_complete": "✅ Объект успешно создан",
        "create_object_error": "❌ Ошибка при создании объекта",
        "continue_btn": "➡️ Продолжить",
        "stop_upload_btn": "🛑 Прекратить загрузку",
        "upload_without_docs_btn": "📄 Создать без документов",
        "no_users_tg_id": "❌ Укажите ID пользователя: /user_tools_xlsx <user_id>",
        "tg_id_must_be_number": "❌ ID пользователя должен быть числом",
        "create_object_w8_documents": "🗂 Загрузите документы по объекту или нажмите 'Создать без документов'",
        "upload_document_first": "❌ Сначала загрузите документ",
        "tmc_upload_btn": "TMC",
        "tmc_upload_instruction": "📝 Загрузите заполненный файл Excel с инструментами",
        "invalid_file_type": "❌ Неверный формат файла. Загрузите файл Excel (.xlsx)",
        "tools_export_btn": "Экспорт инструментов",
        "enter_reminder_description": "📝 Введите описание материала/инструмента",
        "enter_reminder_location": "📍 Введите место хранения",
        "reminder_created": "✅ Напоминание создано",
        "object_data_header": "🏗 Информация об объекте:",
        "object_data_format": (
            "📝 Название: {name}\n"
            "ℹ️ Описание: {description}\n"
            "📅 Создан: {created_at}\n"
            "👤 Создатель: {creator}"
        ),
        "handover_confirmation": "❓ Подтвердите сдачу объекта",
        "handover_cancelled": "❌ Сдача объекта отменена",
        "notification_to_user": "📬 Новое уведомление от {sender}",
        "notification_failed": "❌ Ошибка отправки уведомления",
        "page_info": "Страница {current} из {total}",
        "no_more_pages": "❌ Больше страниц нет",
        "back_to_menu": "◀️ Вернуться в меню",
        "operation_in_progress": "⏳ Операция выполняется...",
        "data_not_found": "❌ Данные не найдены",
        "setup_complete": "✅ Настройка завершена",
        "setup_cancelled": "❌ Настройка отменена",
        "document_delete_confirm": "❓ Подтвердите удаление документа",
        "document_deleted": "✅ Документ удален",
        "document_download_error": "❌ Ошибка при скачивании документа",
        "tmc_upload_start": "📤 Выберите способ добавления инструментов:",
        "tmc_upload_stopped": "✅ Загрузка инструментов остановлена",
        "tmc_invalid_file": "❌ Некорректный файл",
        "no_valid_tools": "❌ В файле нет корректных данных об инструментах",
        "tmc_bulk_upload_complete": "✅ Загружено инструментов: {success}\n❌ Ошибок: {errors}",
        "return_to_tools_control": "🔄 Возврат к управлению инструментами",
        "tmc_manual_btn": "✍️ Ручной ввод",
        "tmc_template_btn": "📄 Скачать шаблон",
        "download_template_btn": "📥 Скачать шаблон",
        "start_transfer_btn": "🔄 Начать передачу",
        "tool_status_all": "🔍 Все инструменты",
        "yes_btn": "✅ Да",
        "no_btn": "❌ Нет",
        "accounting_type_income": "📈 Поступление",
        "accounting_type_expense": "📉 Расход",
        "change_description_material_reminder_btn": "✏️ Изменить описание",
        "change_photo_material_reminder_btn": "📸 Изменить фото",
        "change_storage_location_material_reminder_btn": "📍 Изменить место хранения",
        'user_tools_list': 'Список инструментов закрепленных за {full_name}',
        "excel_material_file_id": "File ID фото",
        "finance_report_btn": "Финансовый отчет",
        "report_by_objects_btn": "📊 По объектам",
        "report_no_objects_btn": "📋 Вне объектов",
        "this_month_btn": "📅 За последние 30 дней",
        "all_time_btn": "📆 За все время",
        "custom_period_btn": "⚙️ Указать период",
        "select_report_type": "Выберите тип отчета:",
        "select_period": "Выберите период отчета:",
        "enter_period": "Введите период в формате ДД.ММ.ГГГГ-ДД.ММ.ГГГГ\nНапример: 01.01.2025-09.06.2025",
        "invalid_period_format": "❌ Неверный формат периода. Попробуйте еще раз.",
        "generating_report": "⏳ Формирую отчет...",
        "report_ready": "✅ Отчет готов!",
        "export_error": "❌ Ошибка при формировании отчета",
        "select_object": "Выберите объект:",
        "financial_report": "Финансовый отчет",
        "financial_report_title": "Финансовый отчет по операциям",
        "date_column": "Дата",
        "transaction_type": "Тип операции",
        "object_column": "Объект",
        "description_column": "Описание",
        "amount_column": "Сумма",
        "user_column": "Пользователь",
        "check_expense": "Расход по чеку",
        "total_income": "Итого доходы:",
        "total_expense": "Итого расходы:",
        "total_profit": "Итого прибыль:",
        "general_accounting_btn": "Общий учёт",
        "object_accounting_btn": "Учёт по объекту",
        "choose_accounting_mode": "Выберите режим учёта:",
    },
    "uz": {
            "reminder_delete_canceled": "Qoldiqlarni o'chirish bekor qilindi",
    "reminder_deleted": "Qoldiqlar faolsizlantirildi",
    "reminder_not_found": "Qoldiqlar topilmadi",
    "start": "Salom, {name}! Men botman",
    "language_select": "Tilni tanlang:",
    "language_ru": "Ruscha",
    "language_uz": "O'zbek",
    "language_tg": "Tojikcha",
    "request_contact": "Iltimos, pastdagi tugma orqali telefon raqamingizni ulashing.",
    "username_instruction": """
Botdan foydalanish uchun foydalanuvchi nomi yaratishingiz kerak. Ko'rsatmalarga rioya qiling

<b>Telegram-da foydalanuvchi nomini qanday yaratish mumkin:</b>

1. Telegram sozlamalarini oching
2. "Profilni tahrirlash" tugmasini bosing
3. "Foydalanuvchi nomi" maydonini bosing
4. Xohlagan foydalanuvchi nomingizni kiriting
5. Saqlash uchun ✓ belgisini bosing

Foydalanuvchi nomini yaratgandan so'ng pastdagi "Tekshirish" tugmasini bosing.""",
    "check": "Tekshirish",
    "create_username": "Foydalanuvchi nomi yaratish",
    "has_no_username": "Foydalanuvchi nomi yaratish uchun ko'rsatmalarga amal qiling",
    "share_contact_btn": "Kontaktni ulashish 📱",
    "no_contact": "Klaviaturadan foydalaning",
    "cancel": "Bekor qilish",
    "confirm": "Tasdiqlash",
    "its_no_contact": "Iltimos, klaviaturadagi tugmadan foydalaning",
    "reques_docs": "Hujjat rasmlarini chatga yuboring. Barcha hujjatlarni yuklagan bo'lsangiz 'To'xtatish' tugmasini bosing",
    "stop_upload_btn": "To'xtatish",
    "i_got_acquainted_btn": "Men tanishdim",
    "i_got_acquainted": "Barcha ma'lumotlar bilan tanishgan bo'lsangiz 'Men tanishdim' tugmasini bosing",
    "reques_fio": "FIO kiriting",
    "ru": "Ruscha",
    "uz": "o'zbek",
    "tg": "Tojikcha",
    "photo_received": "Rasm qabul qilindi. Jami yuklandi: {count}",
    "photos_saved": "Barcha rasmlar ({count}) muvaffaqiyatli saqlandi!",
    "no_photos": "Siz hech qanday rasm yuklamadingiz",
    "solve_example": "Inson ekanligingizni tasdiqlash uchun misolni yeching:\n{example}",
    "verification_success": "Tekshirish muvaffaqiyatli yakunlandi! Ro'yxatdan o'tish tugallandi.",
    "wrong_answer": "Noto'g'ri javob. Boshqa misolni yeching:\n{example}",
    "not_a_number": "Iltimos, raqam kiriting.",
    "report_accepted": "Hisobot qabul qilindi",
    "report_error": "Xabarni yuborishda xatolik yuz berdi.",
    "profile_btn": "Profil",
    "my_objects_btn": "Mening obyektlarim",
    "material_remainder_btn": "Material qoldiqlari",
    "material_order_btn": "Material buyurtmasi",
    "info_btn": "Ma'lumot",
    "instructions": "Botdan foydalanish bo'yicha ko'rsatmalar",
    "rules": "Foydalanish qoidalari",
    "profile_info": (
        "👤 <b>Profil</b>\n\n"
        "🆔 Telegram ID: <code>{telegram_id}</code>\n"
        "📧 Foydalanuvchi nomi: @{username}\n"
        "👨‍💼 FIO: {full_name}\n"
        "📱 Telefon: {phone}\n"
        "📊 Status: {role}"
    ),
    "tools_list_btn": "Asboblar",
    "language_select_btn": "Til tanlash",
    "rules_btn": "Qoidalar",
    "no_tools": "Sizga hech qanday asbob biriktirilmagan",
    "tools_list_header": "🛠 <b>Biriktirilgan asboblar ro'yxati:</b>",
    "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Tavsif: <i>{description}</i>",
    "no_description": "Tavsif mavjud emas",
        "lang_has_changed": "Bot tili o'zgartirildi",
    "no_objects": "Sizda mavjud obyektlar yo'q",
    "objects_list_header": "🏗 <b>Sizning obyektlaringiz:</b>",
    "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
    "navigation_btn": "📍 Navigatsiya",
    "documentation_btn": "📄 Hujjatlar",
    "notify_object_btn": "📢 Obyektni xabardor qilish",
    "object_photo_btn": "📸 Obyektdan foto",
    "object_checks_btn": "🧾 Cheklar hisobi",
    "no_navigation": "Bu obyekt uchun navigatsiya qo'shilmagan",
    "enter_notification": "Obyekt ishtirokchilariga yuborish uchun xabarni kiriting",
    "notification_format": (
        "📢 <b>{object_id} obyektidan xabarnoma</b>\n\n"
        "👤 <b>Yuboruvchi:</b> {sender_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "💬 <b>Xabar:</b>\n<i>{message}</i>"
    ),
    "notification_sent": "✅ Xabarnoma obyektning barcha ishtirokchilariga yuborildi",
    "send_object_photo": "📸 Obyektdan foto yuboring",
    "enter_photo_description": "📝 Fotoga izoh kiriting",
    "object_photo_format": (
        "📸 <b>#{object_id} obyektdan foto</b>\n\n"
        "👤 <b>Yuboruvchi:</b> {worker_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "📝 <b>Izoh:</b>\n<i>{description}</i>"
    ),
    "photo_sent": "✅ Foto muvaffaqiyatli yuborildi",
    "send_photo_only": "❌ Iltimos, faqat foto yuboring",
    "send_check_photo_and_description": "📸 Chek fotosi va izohini yuboring",
    "enter_check_amount": "💰 Chek summasini kiriting (faqat raqamlar)",
    "invalid_amount": "❌ Summa formati noto'g'ri. Misol: 1234.56",
    "check_format": (
        "🧾 <b>#{object_id} obyektdan chek</b>\n\n"
        "👤 <b>Yuboruvchi:</b> {worker_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "📝 <b>Izoh:</b> <i>{description}</i>\n"
        "💰 <b>Summa:</b> {amount} so'm"
    ),
    "check_saved": "✅ Chek muvaffaqiyatli saqlandi",
    "enter_material_order": "📝 Kerakli materiallarni tavsiflang",
    "enter_delivery_date": "📅 Yetkazib berish sanasini ko'rsating (format: KK.OO.YYYY)",
    "date_must_be_future": "❌ Yetkazib berish sanasi kelajakda bo'lishi kerak",
    "invalid_date": "❌ Noto'g'ri sana",
    "invalid_date_format": (
        "❌ Sana formati noto'g'ri\n\n"
        "Format: KK.OO.YYYY\n"
        "Misol: 25.05.2024"
    ),
    "material_order_format": (
        "🛍 <b>Material buyurtmasi</b>\n\n"
        "👤 <b>Buyurtmachi:</b> {worker_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "📝 <b>Kerakli materiallar:</b>\n<i>{description}</i>\n"
        "📅 <b>Yetkazib berish sanasi:</b> <i>{delivery_date}</i>"
    ),
    "order_saved": "✅ Material buyurtmasi muvaffaqiyatli yuborildi",
    "send_material_photo": "📸 Material fotosini yuboring",
    "enter_material_description": "📝 Material tavsifini kiriting",
    "enter_storage_location": "📍 Saqlash joyini ko'rsating",
    "material_remainder_format": (
        "📦 <b>Material qoldig'i</b>\n\n"
        "📝 <b>Tavsif:</b> <i>{description}</i>\n"
        "📍 <b>Saqlash joyi:</b> <i>{location}</i>"
    ),
    "material_saved": "✅ Material haqidagi ma'lumot saqlandi",
    "transfer_tool_invalid_format": "Buyruq formati noto'g'ri. Foydalaning: /transfer_tool <asbob_ID> <oluvchi> <izoh>",
    "transfer_tool_invalid_tool_id": "Asbob ID raqam bo'lishi kerak",
    "transfer_tool_not_found": "Ko'rsatilgan ID bilan asbob topilmadi",
    "transfer_tool_format": (
        "Asbob uzatish:\n"
        "Asbob: {tool_name} (ID: {tool_id})\n"
        "Oluvchi: {recipient}\n"
        "Yuboruvchi: {sender}\n"
    ),
    "transfer_tool_request_sent": "Asbobni uzatish so'rovi yuborildi",
    "accept_tool_btn": "asbobni qabul qilish",
    "transfer_tool_receive_prompt": "Sizga {tool_name} asbobi uzatilmoqda. Qabul qilish uchun quyidagi tugmani bosing",
    "transfer_tool_recipient_not_found": "Bunday nomli foydalanuvchi topilmadi",
    "transfer_tool_invalid_recipient": "Oluvchi @username yoki telegram_id orqali ko'rsatilishi kerak",
    "tool_received_confirmation": "Asbob qabul qilindi!",
    "objects_btn": "Obyektlar",
    "report_empty_text": "Iltimos, /report buyrug'idan keyin hisobot matnini kiriting",
    "report_format": (
        "Yangi hisobot {sender}dan ({username}):\n\n"
        "{report}"
    ),
    "report_sent_confirmation": "Hisobotingiz yuborildi",
    "foreman_workers_btn": "Ishchilar",
    "foreman_documentation_btn": "Hujjatlar",
    "foreman_photos_btn": "Obyektdan fotolar",
    "foreman_handover_btn": "Obyektni topshirish",
    "foreman_procurement_btn": "Xarid",
    "foreman_receipts_btn": "Cheklar hisobi",
    "foreman_material_balance_btn": "Material balansi",
    "foreman_info_btn": "Ma'lumot",
    "foreman_tools_list_btn": "Asboblar ro'yxati",
    "foreman_mass_mailing_btn": "Obyekt bo'yicha tarqatma",
    "foreman_offsite_accounting_btn": "Obyektdan tashqari hisob",
    "foreman_export_xlsx_btn": "Obyekt bo'yicha xlsx eksport",
    "select_object_prompt": "Iltimos, ishchilar ro'yxatini ko'rish uchun obyektni tanlang",
    "back_btn": "Orqaga",
    "no_object_members": "Tanlangan obyektga biriktirilgan ishchilar yo'q",
    "worker_info_format": (
        "Telegram ID: {telegram_id}\n"
        "Foydalanuvchi nomi: {username}\n"
        "FIO: {full_name}\n"
        "Telefon: {phone}\n"
        "Status: {status}\n"
        "Obyekt: {object_name}"
    ),
    "select_object_action": "Obyekt bilan amalni tanlang",
    "no_object_documents": "Bu obyekt uchun hech qanday hujjat qo'shilmagan",
    "document_info_format": (
        "Hujjat turi: {document_type}\n"
        "Obyektga biriktirilgan: {object_name}\n"
    ),
    "enter_handover_description": "Obyektni topshirish tavsifini kiriting:",
    "object_not_found": "Obyekt topilmadi",
    "handover_format": (
        "🏗 <b>Obyektni topshirish</b>\n\n"
        "🏢 Obyekt: {object_name} (ID: {object_id})\n"
        "👤 Prоrab: {foreman_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "📝 <b>Tavsif:</b>\n{description}"
    ),
    "handover_sent": "✅ Obyektni topshirish haqidagi ma'lumot muvaffaqiyatli yuborildi",
    "own_expense_true_btn": "O'z hisobidan - ✔",
    "own_expense_false_btn": "O'z hisobidan - ❌",
    "expense_sheet_name": "Xarajatlar hisoboti",
    "date_column": "Sana",
    "description_column": "Tavsif",
    "amount_column": "Summa",
    "expense_type_column": "Xarajat turi",
    "user_column": "Foydalanuvchi",
    "own_expense": "O'z hisobidan",
    "company_expense": "Kompaniya hisobidan",
    "total_amount": "Jami:",
    "prev_page_btn": "Oldingi",
    "next_page_btn": "Keyingi",
    "mock_data_cleared": "Barcha sinov ma'lumotlari o'chirildi",
    "invalid_photo_format": "Iltimos, foto yuboring",
    "no_workers_found": "Ma'lumotlar bazasida mavjud ishchilar yo'q",
    "expense_report_caption": "Xarajatlar hisoboti\nDavr: {start_date} - {end_date}\nTur: {expense_type}",
    "no_expenses_found": "Ko'rsatilgan davr uchun xarajatlar topilmadi",
    "all_expenses_btn": "Barcha xarajatlar",
    "own_expenses_btn": "O'z hisobidan",
    "company_expenses_btn": "Kompaniya hisobidan",
    "enter_start_date": "📅 Hisobot davrining boshlanish sanasini kiriting (format: KK.OO.YYYY)",
    "enter_end_date": "📅 Hisobot davrining tugash sanasini kiriting (format: KK.OO.YYYY)",
    "select_expense_type": "Eksport uchun xarajat turini tanlang:",
    "invalid_date_format": "❌ Sana formati noto'g'ri. Format: KK.OO.YYYY (misol: 25.12.2024)",
    "expense_report_caption": (
        "📊 Xarajatlar hisoboti\n"
        "📅 Davr: {start_date} - {end_date}\n"
        "💰 Xarajat turi: {expense_type}"
    ),
    "report_processing": "⏳ Hisobot tayyorlanmoqda...",
    "report_generation_error": "❌ Hisobot tayyorlashda xatolik yuz berdi",
    "all_expenses": "Barcha xarajatlar",
    "own_expenses": "O'z hisobidan",
    "company_expenses": "Kompaniya hisobidan",
        "tmc_template_instruction": (
        "📝 Ko'rsatmalar:\n\n"
        "1. Nomi* - asbob nomi\n"
        "2. Soni* - birliklar soni\n"
        "3. Tavsif - qo'shimcha ma'lumot\n"
        "4. Holati - bo'sh/band/ta'mirda\n"
        "5. File ID - asbob fotosi ID\n\n"
        "* - majburiy maydonlar"
    ),
    "tmc_template_sheet": "Asboblar shabloni",
    "excel_tool_quantity": "Soni*",
    "excel_tool_file_id": "Foto File ID",
    "tmc_enter_name": "📝 Asbob nomini kiriting",
    "tmc_enter_quantity": "🔢 Asboblar sonini kiriting",
    "tmc_enter_description": "📝 Asbob tavsifini kiriting (ixtiyoriy)",
    "tmc_upload_complete": "✅ Qo'shildi: {name} x{count}",
    "tmc_file_error": "❌ Faylni qayta ishlashda xatolik yuz berdi",
    "tmc_invalid_quantity": "❌ Son musbat bo'lishi kerak",
    "tmc_save_error": "❌ Asboblarni saqlashda xatolik yuz berdi",
    "materials_sheet_name": "Material qoldiqlari",
    "excel_material_id": "ID",
    "excel_material_description": "Tavsif",
    "excel_material_location": "Saqlash joyi",
    "no_materials_found": "❌ Materiallar topilmadi",
    "materials_export_complete": "✅ Eksport qilingan materiallar: {count}",
    "materials_export_error": "❌ Materiallarni eksport qilishda xatolik yuz berdi",
    "material_card_format": (
        "📦 Material #{id}\n\n"
        "📝 Tavsif: {description}\n"
        "📍 Saqlash joyi: {location}\n"
    ),
    "send_photo_for_file_id": "📸 File ID olish uchun rasm yuboring",
    "file_id_generated": "✅ File ID yaratildi:\n{file_id}",
    "file_id_generation_error": "❌ File ID yaratishda xatolik yuz berdi",
    "stop_btn": "⛔️ To'xtatish",
    "generate_file_id_btn": "🆔 File ID olish",
    "materials_excel_btn": "📊 Qoldiqlarni eksport qilish",
    "bulk_transfer_btn": "📦 Ommaviy o'tkazish",
    "template_error": "❌ Shablon yaratishda xatolik yuz berdi",
    "template_instruction": "📝 Shablonni ko'rsatmalarga muvofiq to'ldiring va qayta yuklang",
    "bulk_transfer_instruction": "📝 Asboblarni ommaviy o'tkazish bo'yicha ko'rsatmalar",
    "bulk_transfer_report": (
        "📊 O'tkazish hisoboti:\n\n"
        "✅ Muvaffaqiyatli:\n{success}\n\n"
        "❌ Xatolar:\n{failed}"
    ),
    "bulk_transfer_no_file": "❌ Fayl yuklanmagan",
    "bulk_transfer_complete": "✅ Asboblarni o'tkazish yakunlandi",
    "check_out_object_format": (
        "🧾 <b>Obyektdan tashqari chek</b>\n\n"
        "👤 <b>Yuboruvchi:</b> {worker_name}\n"
        "📧 Foydalanuvchi nomi: {username}\n\n"
        "📝 <b>Tavsif:</b> <i>{description}</i>\n"
        "💰 <b>Summa:</b> {amount} so'm"
    ),
    "send_file": "📤 Fayl yuboring",
    "file_processing": "⏳ Fayl qayta ishlanmoqda...",
    "file_error": "❌ Faylni qayta ishlashda xatolik yuz berdi",
    "enter_new_photo": "📸 Yangi rasm yuboring",
    "reminder_photo_updated": "✅ Material rasmi yangilandi",
    "reminder_description_updated": "✅ Material tavsifi yangilandi",
    "reminder_location_updated": "✅ Saqlash joyi yangilandi",
    "excel_bulk_transfer_sheet": "Ommaviy o'tkazish",
    "excel_bulk_transfer_tool_id": "Asbob ID*",
    "excel_bulk_transfer_recipient": "Oluvchi*",
    "excel_bulk_transfer_description": "Tavsif",
    "invalid_recipient": "❌ Oluvchi noto'g'ri ko'rsatilgan",
    "invalid_tool_id": "❌ Asbob ID noto'g'ri",
    "tool_not_found": "❌ Asbob topilmadi",
    "recipient_not_found": "❌ Oluvchi topilmadi",
    "success_transfer": "✅ Muvaffaqiyatli o'tkazildi",
    "out_object_check_saved": "✅ Chek saqlandi va guruhga yuborildi",
    "profic_accounting_btn": "Foyda hisobi",
    "select_object_for_profic": "📋 Hisob uchun obyektni tanlang:",
    "select_payment_type": "💳 Operatsiya turini tanlang:",
    "enter_payment_amount": "💰 Summani kiriting:",
    "enter_payment_purpose": "📝 To'lov maqsadini kiriting:",
    "profic_saved": "✅ {type} {amount} so'm miqdorida qo'shildi",
    "profic_save_error": "❌ Operatsiyani saqlashda xatolik yuz berdi",
    "reminder_out_object_btn": "Obyektdan tashqari qoldiqlar",
    "instrument_control_btn": "Asboblarni boshqarish",
    "material_remainder_control_btn": "Material qoldiqlarini boshqarish",
    "reminder_btn": "Qoldiqlar",
    "object_control_btn": "Obyektlarni boshqarish",
    "notify_btn": "Xabarnomalar",
    "cancel_btn": "❌ Bekor qilish",
    "add_worker_to_object_btn": "Ishchi qo'shish",
    "user_tools_list_btn": "Asboblar ro'yxati",
    "change_reminder_btn": "✏️ Qoldiqlarni o'zgartirish",
    "deactivate_reminder_btn": "❌ Qoldiqlarni faolsizlantirish",
    "create_material_reminder_btn": "➕ Qoldiqlarni yaratish",
    "excel_view_btn": "📊 Excel ko'rinishi",
    "change_deactivate_btn": "✏️ O'zgartirish/Faolsizlantirish",
    "tmc_upload_start": "📤 Asboblarni qo'shish usulini tanlang:",
    "tmc_manual_btn": "✍️ Qo'lda kiritish",
    "tmc_template_btn": "📄 Shablonni yuklash",
    "download_template_btn": "📥 Shablonni yuklash",
    "start_transfer_btn": "🔄 O'tkazishni boshlash",
    "tool_status_all": "🔍 Barcha asboblar",
    "yes_btn": "✅ Ha",
    "no_btn": "❌ Yo'q",
    "accounting_type_income": "📈 Kirim",
    "accounting_type_expense": "📉 Chiqim",
    "change_description_material_reminder_btn": "✏️ Tavsifni o'zgartirish",
    "change_photo_material_reminder_btn": "📸 Rasmni o'zgartirish",
    "change_storage_location_material_reminder_btn": "📍 Saqlash joyini o'zgartirish",
    "user_tools_list": "{full_name}ga biriktirilgan asboblar ro'yxati",
    "excel_material_file_id": "Foto File ID",
    "finance_report_btn": "Moliyaviy hisobot",
    "report_by_objects_btn": "📊 Obyektlar bo'yicha",
    "report_no_objects_btn": "📋 Obyektsiz",
    "this_month_btn": "📅 Oxirgi 30 kun",
    "all_time_btn": "📆 Barcha vaqt",
    "custom_period_btn": "⚙️ Davrni belgilash",
    "select_report_type": "Hisobot turini tanlang:",
    "select_period": "Hisobot davrini tanlang:",
    "enter_period": "Davrni KK.OO.YYYY-KK.OO.YYYY formatida kiriting\nMasalan: 01.01.2025-09.06.2025",
    "invalid_period_format": "❌ Davr formati noto'g'ri. Qayta urinib ko'ring.",
    "generating_report": "⏳ Hisobot tayyorlanmoqda...",
    "report_ready": "✅ Hisobot tayyor!",
    "export_error": "❌ Hisobotni tayyorlashda xatolik yuz berdi",
    "select_object": "Obyektni tanlang:",
    "financial_report": "Moliyaviy hisobot",
    "financial_report_title": "Operatsiyalar bo'yicha moliyaviy hisobot",
    "date_column": "Sana",
    "transaction_type": "Operatsiya turi",
    "object_column": "Obyekt",
    "description_column": "Tavsif",
    "amount_column": "Summa",
    "user_column": "Foydalanuvchi",
    "check_expense": "Chek bo'yicha xarajat",
    "total_income": "Jami kirimlar:",
    "total_expense": "Jami chiqimlar:",
    "total_profit": "Jami foyda:",
    "access_denied": "❌ Kirish taqiqlangan",
    "action_cancelled": "❌ Harakat bekor qilindi",
    "add_worker_to_object_text": "📋 Ishchi qo'shish kerak bo'lgan obyektni tanlang:",
    "add_worker_to_object_w8_ids": (
        "🏗 Obyekt: <b>{object_name}</b>\n\n"
        "📝 Ishchilarning Telegram ID larini vergul orqali kiriting (masalan: 123456789, 987654321)"
    ),
    "added_to_object_notification": (
        "👋 Siz yangi obyektga qo'shildingiz!\n\n"
        "🏗 <b>Obyekt:</b> {object_name}\n"
        "ℹ️ Endi siz bu obyektni 'Mening obyektlarim' bo'limida ko'rishingiz mumkin"
    ),
    "admin_notify": "Xabar turini tanlang:",
    "admin_notify_all_user_w8_message": "📝 Barcha foydalanuvchilarga yuborish uchun matnni kiriting:",
    "admin_notify_all_users_inline_btn": "📢 Barcha foydalanuvchilarga",
    "admin_notify_object_inline_btn": "🏗 Obyekt bo'yicha",
    "admin_panel": "👨‍💼 Administrator paneli",
    "all_tools": "Barcha asboblar",
    "back_to_menu": "◀️ Menyuga qaytish",
    "caption_required": "❌ Rasmga tavsif qo'shish kerak",
    "choose_reminder": (
        "📦 <b>Material haqida ma'lumot:</b>\n\n"
        "📝 <b>Tavsif:</b> <i>{description}</i>\n"
        "📍 <b>Saqlash joyi:</b> <i>{storage_location}</i>\n"
    ),
    "confirm_action": "Harakatni tasdiqlang:",
    "confirm_cancel": "❗️ Bekor qilishni tasdiqlang",
    "confirm_delete": "❗️ O'chirishni tasdiqlang",
    "continue_btn": "➡️ Davom etish",
    "create_object_btn": "Obyekt yaratish",
    "create_object_complete": "✅ Obyekt muvaffaqiyatli yaratildi",
    "create_object_description": "📝 Obyekt tavsifini kiriting:",
    "create_object_document_has_received": "✅ Hujjat qabul qilindi. Yuklashni davom ettiring yoki 'To'xtatish' tugmasini bosing",
    "create_object_document_no_received": "❌ Iltimos, hujjat rasmini yuboring",
    "create_object_documents": "📸 Obyekt hujjatlarini yuklang.\n\nBarcha hujjatlarni yuklaganingizdan so'ng 'To'xtatish' tugmasini bosing",
    "create_object_error": "❌ Obyekt yaratishda xatolik yuz berdi",
    "create_object_name": "📝 Obyekt nomini kiriting:",
    "create_object_no_documents": "❌ Hujjatlar yuklanmadi",
    "create_object_saving": "💾 Obyekt saqlanmoqda...",
    "create_object_success": "✅ Obyekt muvaffaqiyatli yaratildi",
    "create_object_uploading": "📤 Hujjatlar yuklanmoqda...",
    "create_object_w8_documents": "🗂 Obyekt hujjatlarini yuklang yoki 'Hujjatlarsiz yaratish' tugmasini bosing",
    "data_not_found": "❌ Ma'lumotlar topilmadi",
    "delete_object_btn": "Obyektni o'chirish",
    "doc_type_contacts": "📞 Buyurtmachi kontaktlari",
    "doc_type_estimate": "📊 Smeta",
    "doc_type_other": "📄 Boshqa",
    "doc_type_select": "🔍 Hujjat turini tanlang:",
    "doc_type_technical": "📋 Texnik topshiriq",
    "doc_type_контакты заказчика": "📞 Buyurtmachi kontaktlari",
    "doc_type_смета": "📊 Smeta",
    "doc_type_техническое задание": "📋 Texnik topshiriq",
    "document_delete_confirm": "❓ Hujjatni o'chirishni tasdiqlaysizmi?",
    "document_deleted": "✅ Hujjat o'chirildi",
    "document_download_error": "❌ Hujjatni yuklashda xatolik yuz berdi",
    "document_saved": "✅ Hujjat saqlandi",
    "document_type_selected": "✅ Hujjat turi tanlandi",
    "document_upload_complete": "✅ Hujjatlarni yuklash yakunlandi",
    "edit_object_btn": "✏️ Obyektni tahrirlash",
    "enter_new_description": "📝 Yangi tavsifni kiriting",
    "enter_notification_text": "📝 Xabar matnini kiriting:",
    "enter_reminder_description": "📝 Material/asbob tavsifini kiriting",
    "enter_reminder_location": "📍 Saqlash joyini kiriting",
    "error_occurred": "❌ Xatolik yuz berdi",
    "excel_amount_column": "Summa",
    "excel_date_column": "Sana",
    "excel_description_column": "Tavsif",
    "excel_expense_type_column": "Xarajat turi",
    "excel_sheet_name": "Xarajatlar hisoboti",
    "excel_tool_date": "Tayinlash sanasi",
    "excel_tool_description": "Tavsif",
    "excel_tool_name": "Nomi",
    "excel_tool_status": "Holati",
    "excel_tool_user": "Biriktirilgan",
    "excel_tools_sheet_name": "Asboblar ro'yxati",
    "excel_total_row": "JAMI:",
    "excel_user_column": "Foydalanuvchi",
    "foreman_panel": "👨‍💼 Prоrab paneli",
    "free_tools": "Bo'sh asboblar",
    "handover_cancelled": "❌ Obyektni topshirish bekor qilindi",
    "handover_confirmation": "❓ Obyektni topshirishni tasdiqlang",
    "in_work_tools": "Ishdagi asboblar",
    "invalid_file_type": "❌ Fayl formati noto'g'ri. Excel (.xlsx) faylini yuklang",
    "invalid_input": "❌ Noto'g'ri kiritish",
    "loading_data": "📥 Ma'lumotlar yuklanmoqda...",
    "member_item_format": (
        "👤 {full_name}\n"
        "📱 {phone}\n"
        "📧 @{username}"
    ),
    "members_added_successfully": (
        "📊 Ishchilarni qo'shish natijasi:\n\n"
        "✅ Muvaffaqiyatli qo'shildi: {success_count}\n"
        "❌ Qo'shilmadi: {failed_count}\n\n"
        "❗️ Rad etish sabablari:\n"
        "{failed_reasons}"
    ),
    "no_members_found": "❌ Obyektda ishtirokchilar yo'q",
    "no_more_pages": "❌ Boshqa sahifalar yo'q",
    "no_objects_found": "❌ Obyektlar topilmadi",
    "no_tools_found": "❌ Asboblar topilmadi",
    "no_users_found": "❌ Foydalanuvchilar topilmadi",
    "no_users_tg_id": "❌ Foydalanuvchi ID sini ko'rsating: /user_tools_xlsx <user_id>",
    "no_valid_tools": "❌ Faylda asboblar haqida to'g'ri ma'lumotlar yo'q",
    "no_valid_user_ids": "❌ To'g'ri Telegram ID lar topilmadi",
    "no_valid_users_found": "❌ Ko'rsatilgan ID lar bo'yicha foydalanuvchilar topilmadi",
    "notification_failed": "❌ Xabarni yuborishda xatolik yuz berdi",
    "notification_sent_to_all": "✅ Xabar barcha foydalanuvchilarga yuborildi",
    "notification_to_user": "📬 {sender}dan yangi xabar",
    "notifications_sent_status": "✅ Yuborish yakunlandi\n\n📊 Jami: {total}\n✅ Muvaffaqiyatli: {success}\n❌ Yetib bormadi: {failed}",
    "object_active": "✅ Faol",
    "object_completed": "🏁 Yakunlangan",
    "object_control": "🏗 Obyektlarni boshqarish",
    "object_control_title": "🏗 Obyektlarni boshqarish",
    "object_data_format": (
        "📝 Nomi: {name}\n"
        "ℹ️ Tavsif: {description}\n"
        "📅 Yaratildi: {created_at}\n"
        "👤 Yaratuvchi: {creator}"
    ),
    "object_data_header": "🏗 Obyekt haqida ma'lumot:",
    "object_deleted": "✅ Obyekt o'chirildi",
    "object_members_header": "👥 Obyekt ishtirokchilari:",
    "object_name": "Obyekt: {name}",
    "object_suspended": "⏸ To'xtatilgan",
    "object_updated": "✅ Obyekt ma'lumotlari yangilandi",
    "objects_list": "📋 Obyektlar ro'yxati:",
    "operation_cancelled": "❌ Operatsiya bekor qilindi",
    "operation_in_progress": "⏳ Operatsiya bajarilmoqda...",
    "page_info": "Sahifa {current} / {total}",
    "pagination_error": "❌ Sahifani yangilashda xatolik",
    "processing": "⏳ Qayta ishlanmoqda...",
    "reminder_created": "✅ Eslatma yaratildi",
    "reminder_deactivated": "✅ Eslatma faolsizlantirildi",
    "reminder_out_btn": "Obyektdan tashqari cheklar hisobi",
    "reminder_updated": "✅ Eslatma yangilandi",
    "repair_tools": "Ta'mirdagi asboblar",
    "return_to_tools_control": "🔄 Asboblarni boshqarishga qaytish",
    "saving_data": "💾 Ma'lumotlar saqlanmoqda...",
    "select_document_type": "Hujjat turini tanlang:",
    "select_object_for_notification": "📋 Xabar yuborish uchun obyektni tanlang:",
    "select_tool_status": "Eksport uchun asboblar turini tanlang:",
    "sending_notifications_status": "📤 Xabarlar yuborilmoqda... {sent}/{total}",
    "setup_cancelled": "❌ Sozlash bekor qilindi",
    "setup_complete": "✅ Sozlash yakunlandi",
    "tg_id_must_be_number": "❌ Foydalanuvchi ID si raqam bo'lishi kerak",
    "tmc_bulk_upload_complete": "✅ Yuklandi: asboblar: {success}\n❌ Xatolar: {errors}",
    "tmc_invalid_file": "❌ Noto'g'ri fayl",
    "tmc_upload_btn": "TMC",
    "tmc_upload_instruction": "📝 To'ldirilgan Excel faylini asboblar bilan yuklang",
    "tmc_upload_stopped": "✅ Asboblarni yuklash to'xtatildi",
    "tool_status_active": "✅ Ishda",
    "tool_status_free": "🆓 Bo'sh",
    "tool_status_repair": "🔧 Ta'mirda",
    "tool_transfer_success": "✅ Asbob muvaffaqiyatli uzatildi",
    "tools_export_btn": "Asboblarni eksport qilish",
    "tools_list_caption": "📊 Asboblar hisoboti\n💼 Turi: {tool_status}",
    "transfer_tool_admin_format": (
        "Buyruq formati:\n"
        "/transfer_tool <asbob_ID> <oluvchi> <tavsif>\n"
        "Majburiy uzatish uchun (faqat adminlar):\n"
        "/transfer_tool <asbob_ID> <oluvchi> -f <tavsif>"
    ),
    "transfer_tool_force_complete": "✅ Asbob majburan uzatildi",
    "transfer_tool_force_format": (
        "🔄 Asbobni majburiy uzatish\n"
        "🛠 Asbob: {tool_name} (ID: {tool_id})\n"
        "👤 Oluvchi: {recipient}\n"
        "👨‍💼 Administrator: {admin}\n"
        "📝 Tavsif: {description}"
    ),
    "transfer_tool_force_received": "🔄 Administrator {admin} sizga {tool_name} asbobini uzatdi",
    "try_again": "🔄 Qayta urinib ko'ring",
    "updated_success": "✅ Ma'lumotlar muvaffaqiyatli yangilandi",
    "upload_document_first": "❌ Avval hujjatni yuklang",
    "upload_more_documents": "📤 Keyingi hujjatni yuklang yoki 'Yakunlash' tugmasini bosing",
    "upload_without_docs_btn": "📄 Hujjatlarsiz yaratish",
    "user_control": "👥 Foydalanuvchilarni boshqarish"
    },
    "tg": {
         "reminder_delete_canceled": "Бекор кардани нест кардани бақияҳо",
    "reminder_deleted": "Бақияҳо ғайрифаъол карда шуданд",
    "reminder_not_found": "Бақияҳо ёфт нашуданд",
    "start": "Салом, {name}! Ман бот ҳастам",
    "language_select": "Забонро интихоб кунед:",
    "language_ru": "Русӣ",
    "language_uz": "Узбек",
    "language_tg": "Тоҷикӣ",
    "request_contact": "Лутфан, рақами телефони худро тавассути тугмаи зерин мубодила кунед.",
    "username_instruction": """
Барои истифодаи бот шумо бояд номи корбарӣ созед. Дастурҳоро пайравӣ кунед

<b>Чӣ тавр дар Telegram номи корбарӣ сохтан мумкин аст:</b>

1. Танзимоти Telegram-ро кушоед
2. "Тағйир додани профил"-ро пахш кунед
3. Дар майдони "Номи корбарӣ" пахш кунед
4. Номи корбарии дилхоҳро дохил кунед
5. Барои нигоҳ доштан аломати ✓-ро пахш кунед

Пас аз сохтани номи корбарӣ, тугмаи "Санҷидан"-ро дар поён пахш кунед.""",
    "check": "Санҷидан",
    "create_username": "Сохтани номи корбарӣ",
    "has_no_username": "Барои сохтани номи корбарӣ дастурҳоро пайравӣ кунед",
    "share_contact_btn": "Мубодилаи тамос 📱",
    "no_contact": "Аз клавиатура истифода баред",
    "cancel": "Бекор кардан",
    "confirm": "Тасдиқ кардан",
    "its_no_contact": "Лутфан, аз тугмаи дар клавиатура истифода баред",
    "reques_docs": "Расмҳои ҳуҷҷатҳоро ба чат фиристед. Вақте ки ҳамаи ҳуҷҷатҳоро бор кардед, тугмаи 'Қатъ'-ро пахш кунед.",
    "stop_upload_btn": "Қатъ",
    "i_got_acquainted_btn": "Ман шинос шудам",
    "i_got_acquainted": "Агар бо ҳама чиз шинос шудед, тугмаи 'Ман шинос шудам'-ро пахш кунед",
    "reques_fio": "ФИО-ро дохил кунед",
    "ru": "Русӣ",
    "uz": "Узбек",
    "tg": "Тоҷикӣ",
    "photo_received": "Расм қабул шуд. Ҳамагӣ бор карда шуд: {count}",
    "photos_saved": "Ҳамаи расмҳо ({count}) бомуваффақият нигоҳ дошта шуданд!",
    "no_photos": "Шумо ягон расм бор накардед",
    "solve_example": "Барои тасдиқи он, ки шумо инсон ҳастед, мисолро ҳал кунед:\n{example}",
    "verification_success": "Тасдиқ бомуваффақият анҷом ёфт! Бақайдгирӣ анҷом ёфт.",
    "wrong_answer": "Ҷавоби нодуруст. Мисоли дигарро ҳал кунед:\n{example}",
    "not_a_number": "Лутфан, рақамро дохил кунед.",
    "report_accepted": "Ҳисобот қабул карда шуд",
    "report_error": "Ҳангоми фиристодани паём хато рух дод.",
    "profile_btn": "Профил",
    "my_objects_btn": "Объектҳои ман",
    "material_remainder_btn": "Бақияи масолеҳ",
    "material_order_btn": "Фармоиши масолеҳ",
    "info_btn": "Маълумот",
    "instructions": "Дастурҳо оид ба истифодаи бот",
    "rules": "Қоидаҳои истифода",
    "profile_info": (
        "👤 <b>Профил</b>\n\n"
        "🆔 Telegram ID: <code>{telegram_id}</code>\n"
        "📧 Номи корбарӣ: @{username}\n"
        "👨‍💼 ФИО: {full_name}\n"
        "📱 Телефон: {phone}\n"
        "📊 Мақом: {role}"
    ),
    "tools_list_btn": "Асбобҳо",
    "language_select_btn": "Интихоби забон",
    "rules_btn": "Қоидаҳо",
    "no_tools": "Ба шумо ягон асбоб вобаста карда нашудааст",
    "tools_list_header": "🛠 <b>Рӯйхати асбобҳои вобасташуда:</b>",
    "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Тавсиф: <i>{description}</i>",
    "no_description": "Тавсиф вуҷуд надорад",
    "lang_has_changed": "Забони бот тағйир дода шуд",
    "no_objects": "Шумо объектҳои дастрас надоред",
    "objects_list_header": "🏗 <b>Объектҳои шумо:</b>",
    "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
    "navigation_btn": "📍 Навигатсия",
    "documentation_btn": "📄 Ҳуҷҷатҳо",
    "notify_object_btn": "📢 Огоҳ кардани объект",
    "object_photo_btn": "📸 Расм аз объект",
    "object_checks_btn": "🧾 Баҳисобгирии чекҳо",
    "no_navigation": "Барои ин объект навигатсия илова нашудааст",
    "enter_notification": "Паёмро барои фиристодан ба ҳамаи иштирокчиёни объект дохил кунед",
    "notification_format": (
        "📢 <b>Огоҳинома аз объекти {object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {sender_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "💬 <b>Паём:</b>\n<i>{message}</i>"
    ),
    "notification_sent": "✅ Огоҳинома ба ҳамаи иштирокчиёни объект фиристода шуд",
    "send_object_photo": "📸 Расмро аз объект фиристед",
    "enter_photo_description": "📝 Тавсифи расмро дохил кунед",
    "object_photo_format": (
        "📸 <b>Расм аз объекти #{object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b>\n<i>{description}</i>"
    ),
    "photo_sent": "✅ Расм бомуваффақият фиристода шуд",
    "send_photo_only": "❌ Лутфан, танҳо расмро фиристед",
    "send_check_photo_and_description": "📸 Расм ва тавсифи чекро фиристед",
    "enter_check_amount": "💰 Маблағи чекро дохил кунед (танҳо рақамҳо)",
    "invalid_amount": "❌ Формати маблағ нодуруст аст. Масалан: 1234.56",
    "check_format": (
        "🧾 <b>Чек аз объекти #{object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "💰 <b>Маблағ:</b> {amount} сомонӣ"
    ),
    "check_saved": "✅ Чек бомуваффақият нигоҳ дошта шуд",
    "enter_material_order": "📝 Масолеҳи лозимиро тавсиф кунед",
    "enter_delivery_date": "📅 Санаи дилхоҳи расониданро нишон диҳед (формат: РР.ММ.СССС)",
    "date_must_be_future": "❌ Санаи расонидан бояд дар оянда бошад",
    "invalid_date": "❌ Санаи нодуруст",
    "invalid_date_format": (
        "❌ Формати санаи нодуруст\n\n"
        "Формат: РР.ММ.СССС\n"
        "Масалан: 25.05.2024"
    ),
    "material_order_format": (
        "🛍 <b>Фармоиши масолеҳ</b>\n\n"
        "👤 <b>Фармоишгар:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Масолеҳи лозима:</b>\n<i>{description}</i>\n"
        "📅 <b>Санаи дилхоҳ:</b> <i>{delivery_date}</i>"
    ),
    "order_saved": "✅ Фармоиши масолеҳ бомуваффақият фиристода шуд",
    "send_material_photo": "📸 Расми масолеҳро фиристед",
    "enter_material_description": "📝 Тавсифи масолеҳро дохил кунед",
    "enter_storage_location": "📍 Ҷойи нигоҳдории масолеҳро нишон диҳед",
    "material_remainder_format": (
        "📦 <b>Бақияи масолеҳ</b>\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "📍 <b>Ҷойи нигоҳдорӣ:</b> <i>{location}</i>"
    ),
    "material_saved": "✅ Маълумот дар бораи масолеҳ нигоҳ дошта шуд",
    "transfer_tool_invalid_format": "Формати фармон нодуруст аст. Истифода баред: /transfer_tool <ID асбоб> <гиранда> <тавсиф>",
    "transfer_tool_invalid_tool_id": "ID асбоб бояд рақам бошад.",
    "transfer_tool_not_found": "Асбоб бо ID нишондодашуда ёфт нашуд.",
    "transfer_tool_format": (
        "Интиқоли асбоб:\n"
        "Асбоб: {tool_name} (ID: {tool_id})\n"
        "Гиранда: {recipient}\n"
        "Фиристанда: {sender}\n"
    ),
    "transfer_tool_request_sent": "Дархост барои интиқоли асбоб фиристода шуд.",
    "accept_tool_btn": "қабул кардани асбоб",
    "transfer_tool_receive_prompt": "Ба шумо асбоби {tool_name} мефиристанд. Барои гирифтан тугмаи зеринро пахш кунед.",
    "transfer_tool_recipient_not_found": "Корбар бо чунин ном ёфт нашуд.",
    "transfer_tool_invalid_recipient": "Гиранда бояд тавассути @username ё telegram_id нишон дода шавад.",
    "tool_received_confirmation": "Асбоб қабул карда шуд!",
    "objects_btn": "Объектҳо",
    "report_empty_text": "Лутфан, матни ҳисоботро пас аз фармони /report дохил кунед",
    "report_format": (
        "Ҳисоботи нав аз {sender} ({username}):\n\n"
        "{report}"
    ),
    "report_sent_confirmation": "Ҳисоботи шумо фиристода шуд.",
    "foreman_workers_btn": "Коргарон",
    "foreman_documentation_btn": "Ҳуҷҷатҳо",
    "foreman_photos_btn": "Расмҳо аз объект",
    "foreman_handover_btn": "Супоридани объект",
    "foreman_procurement_btn": "Харид",
    "foreman_receipts_btn": "Баҳисобгирии чекҳо",
    "foreman_material_balance_btn": "Тавозуни масолеҳ",
    "foreman_info_btn": "Маълумот",
    "foreman_tools_list_btn": "Рӯйхати асбобҳо",
    "foreman_mass_mailing_btn": "Паёмҳои оммавӣ аз рӯи объект",
    "foreman_offsite_accounting_btn": "Баҳисобгирии берун аз объект",
    "foreman_export_xlsx_btn": "Содироти xlsx аз рӯи объект",
    "select_object_prompt": "Лутфан, объектро барои дидани рӯйхати коргарон интихоб кунед",
    "back_btn": "Бозгашт",
    "no_object_members": "Барои объекти интихобшуда коргарон вобаста карда нашудаанд",
    "worker_info_format": (
        "Telegram ID: {telegram_id}\n"
        "Номи корбарӣ: {username}\n"
        "ФИО: {full_name}\n"
        "Телефон: {phone}\n"
        "Мақом: {status}\n"
        "Объект: {object_name}"
    ),
    "select_object_action": "Амали объектро интихоб кунед",
    "no_object_documents": "Барои ин объект ягон ҳуҷҷат илова нашудааст",
    "document_info_format": (
        "Намуди ҳуҷҷат: {document_type}\n"
        "Ба объект вобаста: {object_name}\n"
    ),
    "enter_handover_description": "Тавсифи супоридани объектро дохил кунед:",
    "object_not_found": "Объект ёфт нашуд",
    "handover_format": (
        "🏗 <b>Супоридани объект</b>\n\n"
        "🏢 Объект: {object_name} (ID: {object_id})\n"
        "👤 Прораб: {foreman_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b>\n{description}"
    ),
    "handover_sent": "✅ Маълумот дар бораи супоридани объект бомуваффақият фиристода шуд",
    "own_expense_true_btn": "Аз ҳисоби худ - ✔",
    "own_expense_false_btn": "Аз ҳисоби худ - ❌",
    "expense_sheet_name": "Ҳисоботи хароҷот",
    "date_column": "Сана",
    "description_column": "Тавсиф",
    "amount_column": "Маблағ",
    "expense_type_column": "Намуди хароҷот",
    "user_column": "Корбар",
    "own_expense": "Аз ҳисоби худ",
    "company_expense": "Аз ҳисоби ширкат",
    "total_amount": "Ҳамагӣ:",
    "prev_page_btn": "Саҳифаи қаблӣ",
    "next_page_btn": "Саҳифаи навбатӣ",
    "mock_data_cleared": "Ҳамаи маълумоти санҷишӣ нест карда шуд",
    "invalid_photo_format": "Лутфан, расмро фиристед",
    "no_workers_found": "Коргарони дастрас дар пойгоҳи додаҳо нестанд",
    "expense_report_caption": "Ҳисоботи хароҷот\nДавра: {start_date} - {end_date}\nНамуд: {expense_type}",
    "no_expenses_found": "Барои давраи нишондодашуда хароҷот ёфт нашуд",
    "all_expenses_btn": "Ҳамаи хароҷот",
    "own_expenses_btn": "Аз ҳисоби худ",
    "company_expenses_btn": "Аз ҳисоби ширкат",
    "enter_start_date": "📅 Санаи оғози давраи ҳисоботиро дохил кунед (формат: РР.ММ.СССС)",
    "enter_end_date": "📅 Санаи охири давраи ҳисоботиро дохил кунед (формат: РР.ММ.СССС)",
    "select_expense_type": "Намуди хароҷотро барои содирот интихоб кунед:",
    "invalid_date_format": "❌ Формати сана нодуруст аст. Масалан: 25.12.2024",
    "expense_report_caption": (
        "📊 Ҳисоботи хароҷот\n"
        "📅 Давра: {start_date} - {end_date}\n"
        "💰 Намуди хароҷот: {expense_type}"
    ),
    "report_processing": "⏳ Таҳияи ҳисобот...",
    "report_generation_error": "❌ Ҳангоми таҳияи ҳисобот хато рух дод",
    "all_expenses": "Ҳамаи хароҷот",
    "own_expenses": "Аз ҳисоби худ",
    "company_expenses": "Аз ҳисоби ширкат",
    "excel_date_column": "Сана",
    "excel_description_column": "Тавсиф",
    "excel_amount_column": "Маблағ",
    "excel_expense_type_column": "Намуди хароҷот",
    "excel_user_column": "Корбар",
    "excel_total_row": "ҲАМАГӢ:",
    "excel_sheet_name": "Ҳисоботи хароҷот",
    "reminder_out_btn": "Баҳисобгирии чекҳои берун аз объектҳо",
    "tools_list_caption": "📊 Ҳисоботи асбобҳо\n💼 Намуд: {tool_status}",
    "select_tool_status": "Намуди асбобҳоро барои содирот интихоб кунед:",
    "all_tools": "Ҳамаи асбобҳо",
    "in_work_tools": "Асбобҳои дар кор",
    "free_tools": "Асбобҳои озод",
    "repair_tools": "Асбобҳои дар таъмир",
    "no_tools_found": "❌ Асбобҳо ёфт нашуданд",
    "excel_tool_name": "Номгӯй",
    "excel_tool_description": "Тавсиф",
    "excel_tool_status": "Ҳолат",
    "excel_tool_user": "Вобаста ба",
    "excel_tool_date": "Санаи таъин",
    "excel_tools_sheet_name": "Рӯйхати асбобҳо",
    "no_users_found": "❌ Корбарон ёфт нашуданд",
    "no_objects_found": "❌ Объектҳо ёфт нашуданд",
    "no_members_found": "❌ Дар объект иштирокчиён нестанд",
    "select_object_for_notification": "📋 Объектро барои фиристодани огоҳинома интихоб кунед:",
    "enter_notification_text": "📝 Матни огоҳиномаро барои фиристодан дохил кунед:",
    "sending_notifications_status": "📤 Фиристода истодааст... {sent}/{total}",
    "notifications_sent_status": "✅ Фиристодан анҷом ёфт\n\n📊 Ҳамагӣ: {total}\n✅ Бомуваффақият: {success}\n❌ Нарасида: {failed}",
    "admin_notify_all_users_inline_btn": "📢 Ба ҳамаи корбарон",
    "admin_notify_object_inline_btn": "🏗 Аз рӯи объект",
    "admin_notify_all_user_w8_message": "📝 Матнро барои фиристодан ба ҳамаи корбарон дохил кунед:",
    "transfer_tool_force_format": (
        "🔄 Интиқоли маҷбурии асбоб\n"
        "🛠 Асбоб: {tool_name} (ID: {tool_id})\n"
        "👤 Гиранда: {recipient}\n"
        "👨‍💼 Маъмур: {admin}\n"
        "📝 Тавсиф: {description}"
    ),
    "transfer_tool_force_complete": "✅ Асбоб маҷбуран интиқол дода шуд",
    "transfer_tool_force_received": "🔄 Маъмур {admin} ба шумо асбоби {tool_name}-ро интиқол дод",
    "transfer_tool_admin_format": (
        "Формати фармон:\n"
        "/transfer_tool <ID_асбоб> <гиранда> <тавсиф>\n"
        "Барои интиқоли маҷбурӣ (танҳо барои маъмурон):\n"
        "/transfer_tool <ID_асбоб> <гиранда> -f <тавсиф>"
    ),
    "admin_notify": "Намуди фиристоданро интихоб кунед:",
    "create_object_name": "📝 Номи объектро дохил кунед:",
    "operation_cancelled": "❌ Амалиёт бекор карда шуд",
    "caption_required": "❌ Ба расм тавсиф илова кардан лозим аст",
    "select_document_type": "Намуди ҳуҷҷатро интихоб кунед:",
    "doc_type_estimate": "📊 Смета",
    "doc_type_technical": "📋 Супориши техникӣ",
    "doc_type_contacts": "📞 Тамосҳои фармоишгар",
    "create_object_success": "✅ Объект бомуваффақият сохта шуд",
    "notification_sent_to_all": "✅ Огоҳинома ба ҳамаи корбарон фиристода шуд",
    "create_object_no_documents": "❌ Ҳуҷҷатҳо бор карда нашуданд",
    "create_object_description": "📝 Тавсифи объектро дохил кунед:",
    "pagination_error": "❌ Хато ҳангоми навсозии саҳифа",
    "objects_list": "📋 Рӯйхати объектҳо:",
    "object_name": "Объект: {name}",
    "updated_success": "✅ Маълумот бомуваффақият навсозӣ карда шуд",
    "error_occurred": "❌ Хато рух дод",
    "document_upload_complete": "✅ Боркунии ҳуҷҷатҳо анҷом ёфт",
    "document_type_selected": "✅ Намуди ҳуҷҷат интихоб шуд",
    "document_saved": "✅ Ҳуҷҷат нигоҳ дошта шуд",
    "upload_more_documents": "📤 Ҳуҷҷати навбатиро бор кунед ё 'Анҷом'-ро пахш кунед",
    "foreman_panel": "👨‍💼 Панели прораб",
    "object_members_header": "👥 Иштирокчиёни объект:",
    "member_item_format": (
        "👤 {full_name}\n"
        "📱 {phone}\n"
        "📧 @{username}"
    ),
    "admin_panel": "👨‍💼 Панели маъмур",
    "object_control": "🏗 Идоракунии объектҳо",
    "user_control": "👥 Идоракунии корбарон",
    "create_object_btn": "Сохтани объект",
    "edit_object_btn": "✏️ Таҳрири объект",
    "delete_object_btn": "Нест кардани объект",
    "access_denied": "❌ Дастрасӣ манъ аст",
    "invalid_input": "❌ Вуруди нодуруст",
    "action_cancelled": "❌ Амал бекор карда шуд",
    "try_again": "🔄 Боз кӯшиш кунед",
    "processing": "⏳ Коркард...",
    "saving_data": "💾 Нигоҳдории маълумот...",
    "loading_data": "📥 Боркунии маълумот...",
    "tool_status_active": "✅ Дар кор",
    "tool_status_free": "🆓 Озод",
    "tool_status_repair": "🔧 Дар таъмир",
    "tool_transfer_success": "✅ Асбоб бомуваффақият интиқол дода шуд",
    "object_active": "✅ Фаъол",
    "object_completed": "🏁 Анҷомёфта",
    "object_suspended": "⏸ Боздошташуда",
    "confirm_action": "Амалро тасдиқ кунед:",
    "confirm_delete": "❗️ Нест карданро тасдиқ кунед",
    "confirm_cancel": "❗️ Бекор карданро тасдиқ кунед",
     "tmc_template_instruction": (
    "📝 Дастурамал оид ба пур кардан:\n\n"
    "1. Ном* - номи асбоб\n"
    "2. Миқдор* - шумораи воҳидҳо\n"
    "3. Тавсиф - маълумоти иловагӣ\n"
    "4. Ҳолат - озод/банд/дар таъмир\n"
    "5. File ID - ID расми асбоб\n\n"
    "* - майдонҳои ҳатмӣ"
    ),
    "tmc_template_sheet": "Шаблони асбобҳо",
    "excel_tool_quantity": "Миқдор*",
    "excel_tool_file_id": "File ID расм",
    "tmc_enter_name": "📝 Номи асбобро дохил кунед",
    "tmc_enter_quantity": "🔢 Миқдори асбобҳоро дохил кунед",
    "tmc_enter_description": "📝 Тавсифи асбобро дохил кунед (ихтиёрӣ)",
    "tmc_upload_complete": "✅ Илова карда шуд: {name} x{count}",
    "tmc_file_error": "❌ Ҳангоми коркарди файл хато рух дод",
    "tmc_invalid_quantity": "❌ Миқдор бояд адади мусбат бошад",
    "tmc_save_error": "❌ Ҳангоми нигоҳдории асбобҳо хато рух дод",
    "materials_sheet_name": "Бақияҳои масолеҳ",
    "excel_material_id": "ID",
    "excel_material_description": "Тавсиф",
    "excel_material_location": "Ҷойи нигоҳдорӣ",
    "no_materials_found": "❌ Масолеҳ ёфт нашуд",
    "materials_export_complete": "✅ Содироти масолеҳ: {count}",
    "materials_export_error": "❌ Ҳангоми содироти масолеҳ хато рух дод",
    "material_card_format": (
        "📦 Масолеҳ #{id}\n\n"
        "📝 Тавсиф: {description}\n"
        "📍 Ҷойи нигоҳдорӣ: {location}\n"
    ),
    "send_photo_for_file_id": "📸 Барои гирифтани File ID расм фиристед",
    "file_id_generated": "✅ File ID сохта шуд:\n{file_id}",
    "file_id_generation_error": "❌ Ҳангоми сохтани File ID хато рух дод",
    "stop_btn": "⛔️ Қатъ",
    "generate_file_id_btn": "🆔 Гирифтани File ID",
    "materials_excel_btn": "📊 Содироти бақияҳо",
    "bulk_transfer_btn": "📦 Интиқоли оммавӣ",
    "template_error": "❌ Ҳангоми сохтани шаблон хато рух дод",
    "template_instruction": "📝 Шаблонро мувофиқи дастурамал пур кунед ва дубора бор кунед",
    "bulk_transfer_instruction": "📝 Дастурамал оид ба интиқоли оммавии асбобҳо",
    "bulk_transfer_report": (
        "📊 Ҳисобот оид ба интиқол:\n\n"
        "✅ Бомуваффақият:\n{success}\n\n"
        "❌ Хатоҳо:\n{failed}"
    ),
    "bulk_transfer_no_file": "❌ Файл бор карда нашудааст",
    "bulk_transfer_complete": "✅ Интиқоли асбобҳо анҷом ёфт",
    "check_out_object_format": (
        "🧾 <b>Чек берун аз объект</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "💰 <b>Маблағ:</b> {amount} сомонӣ"
    ),
    "send_file": "📤 Файлро фиристед",
    "file_processing": "⏳ Коркарди файл...",
    "file_error": "❌ Ҳангоми коркарди файл хато рух дод",
    "enter_new_photo": "📸 Расми навро фиристед",
    "reminder_photo_updated": "✅ Расми масолеҳ нав карда шуд",
    "reminder_description_updated": "✅ Тавсифи масолеҳ нав карда шуд",
    "reminder_location_updated": "✅ Ҷойи нигоҳдорӣ нав карда шуд",
    "excel_bulk_transfer_sheet": "Интиқоли оммавӣ",
    "excel_bulk_transfer_tool_id": "ID асбоб*",
    "excel_bulk_transfer_recipient": "Гиранда*",
    "excel_bulk_transfer_description": "Тавсиф",
    "invalid_recipient": "❌ Гиранда нодуруст нишон дода шудааст",
    "invalid_tool_id": "❌ ID асбоб нодуруст аст",
    "tool_not_found": "❌ Асбоб ёфт нашуд",
    "recipient_not_found": "❌ Гиранда ёфт нашуд",
    "success_transfer": "✅ Бомуваффақият интиқол дода шуд",
    "out_object_check_saved": "✅ Чек нигоҳ дошта ва ба гурӯҳ фиристода шуд",
    "profic_accounting_btn": "Баҳисобгирии фоида",
    "select_object_for_profic": "📋 Барои баҳисобгирӣ объектро интихоб кунед:",
    "select_payment_type": "💳 Намуди амалиётро интихоб кунед:",
    "enter_payment_amount": "💰 Маблағро дохил кунед:",
    "enter_payment_purpose": "📝 Мақсади пардохтро дохил кунед:",
    "profic_saved": "✅ {type} ба маблағи {amount} сомонӣ илова карда шуд",
    "profic_save_error": "❌ Ҳангоми нигоҳдории амалиёт хато рух дод",
    "reminder_out_object_btn": "Бақияҳои берун аз объект",
    "instrument_control_btn": "Идоракунии асбобҳо",
    "material_remainder_control_btn": "Идоракунии бақияҳои масолеҳ",
    "reminder_btn": "Бақияҳо",
    "object_control_btn": "Идоракунии объектҳо",
    "notify_btn": "Огоҳиномаҳо",
    "cancel_btn": "❌ Бекор кардан",
    "add_worker_to_object_btn": "Илова кардани коргар",
    "bulk_transfer_btn": "Интиқоли оммавӣ",
    "user_tools_list_btn": "Рӯйхати асбобҳо",
    "change_reminder_btn": "✏️ Тағйир додани бақияҳо",
    "deactivate_reminder_btn": "❌ Ғайрифаъол кардани бақияҳо",
    "create_material_reminder_btn": "➕ Сохтани бақияҳо",
    "excel_view_btn": "📊 Намоиши Excel",
    "change_deactivate_btn": "✏️ Тағйир додан/Ғайрифаъол кардан",
    "tmc_upload_start": "📤 Усули илова кардани асбобҳоро интихоб кунед:",
    "tmc_manual_btn": "✍️ Воридоти дастӣ",
    "tmc_template_btn": "📄 Боргирии шаблон",
    "download_template_btn": "📥 Боргирии шаблон",
    "start_transfer_btn": "🔄 Оғози интиқол",
    "tool_status_all": "🔍 Ҳамаи асбобҳо",
    "yes_btn": "✅ Ҳа",
    "no_btn": "❌ Не",
    "accounting_type_income": "📈 Даромад",
    "accounting_type_expense": "📉 Хароҷот",
    "change_description_material_reminder_btn": "✏️ Тағйири тавсиф",
    "change_photo_material_reminder_btn": "📸 Тағйири расм",
    "change_storage_location_material_reminder_btn": "📍 Тағйири ҷойи нигоҳдорӣ",
    "user_tools_list": "Рӯйхати асбобҳои ба {full_name} вобасташуда",
    "excel_material_file_id": "File ID расм",
    "finance_report_btn": "Ҳисоботи молиявӣ",
    "report_by_objects_btn": "📊 Аз рӯи объектҳо",
    "report_no_objects_btn": "📋 Бе объект",
    "this_month_btn": "📅 30 рӯзи охир",
    "all_time_btn": "📆 Ҳамаи вақт",
    "custom_period_btn": "⚙️ Муайян кардани давра",
    "select_report_type": "Намуди ҳисоботро интихоб кунед:",
    "select_period": "Давраи ҳисоботро интихоб кунед:",
    "enter_period": "Давраро дохил кунед (дар шакли РР.ММ.СССС-РР.ММ.СССС)\nМасалан: 01.01.2025-09.06.2025",
    "invalid_period_format": "❌ Шакли давра нодуруст аст. Аз нав кӯшиш кунед.",
    "generating_report": "⏳ Ҳисобот тайёр мешавад...",
    "report_ready": "✅ Ҳисобот тайёр аст!",
    "export_error": "❌ Ҳангоми тайёр кардани ҳисобот хато рух дод",
    "select_object": "Объектро интихоб кунед:",
    "financial_report": "Ҳисоботи молиявӣ",
    "financial_report_title": "Ҳисоботи молиявӣ аз рӯи амалиётҳо",
    "date_column": "Сана",
    "transaction_type": "Намуди амалиёт",
    "object_column": "Объект",
    "description_column": "Тавсиф",
    "amount_column": "Маблағ",
    "user_column": "Истифодабаранда",
    "check_expense": "Хароҷоти чек",
    "total_income": "Даромади умумӣ:",
    "total_expense": "Хароҷоти умумӣ:",
    "total_profit": "Фоидаи умумӣ:",
    "add_worker_to_object_text": "📋 Объектеро, ки ба он коргар илова кардан лозим аст, интихоб кунед:", 
    "add_worker_to_object_w8_ids": (
        "🏗 Объект: <b>{object_name}</b>\n\n"
        "📝 Telegram ID-и коргаронро тавассути вергул дохил кунед (масалан: 123456789, 987654321)"
    ),
    "added_to_object_notification": (
        "👋 Шумо ба объекти нав илова карда шудед!\n\n"
        "🏗 <b>Объект:</b> {object_name}\n"
        "ℹ️ Акнун шумо метавонед ин объектро дар қисмати 'Объектҳои ман' бинед"
    ),
    "back_to_menu": "◀️ Бозгашт ба меню",
    "choose_reminder": (
        "📦 <b>Маълумот дар бораи масолеҳ:</b>\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "📍 <b>Ҷойи нигоҳдорӣ:</b> <i>{storage_location}</i>\n"
    ),
    "continue_btn": "➡️ Давом додан",
    "create_object_complete": "✅ Объект бомуваффақият сохта шуд",
    "create_object_document_has_received": "✅ Ҳуҷҷат қабул шуд. Боркуниро давом диҳед ё 'Қатъ'-ро пахш кунед",
    "create_object_document_no_received": "❌ Лутфан, расми ҳуҷҷатро фиристед",
    "create_object_documents": "📸 Расмҳои ҳуҷҷатҳои объектро бор кунед.\n\nВақте ки ҳамаи ҳуҷҷатҳоро бор кардед, 'Қатъ'-ро пахш кунед",
    "create_object_error": "❌ Ҳангоми сохтани объект хато рух дод",
    "create_object_saving": "💾 Нигоҳдории объект...",
    "create_object_uploading": "📤 Боркунии ҳуҷҷатҳо...",
    "create_object_w8_documents": "🗂 Ҳуҷҷатҳои объектро бор кунед ё 'Бе ҳуҷҷатҳо сохтан'-ро пахш кунед",
    "data_not_found": "❌ Маълумот ёфт нашуд",
    "doc_type_other": "📄 Дигар",
    "doc_type_select": "🔍 Намуди ҳуҷҷатро интихоб кунед:",
    "doc_type_контакты заказчика": "📞 Тамосҳои фармоишгар",
    "doc_type_смета": "📊 Смета",
    "doc_type_техническое задание": "📋 Супориши техникӣ",
    "document_delete_confirm": "❓ Нест кардани ҳуҷҷатро тасдиқ кунед",
    "document_deleted": "✅ Ҳуҷҷат нест карда шуд",
    "document_download_error": "❌ Ҳангоми боргирии ҳуҷҷат хато рух дод",
    "enter_new_description": "📝 Тавсифи навро дохил кунед",
    "enter_reminder_description": "📝 Тавсифи масолеҳ/асбобро дохил кунед",
    "enter_reminder_location": "📍 Ҷойи нигоҳдориро дохил кунед",
    "handover_cancelled": "❌ Супоридани объект бекор карда шуд",
    "handover_confirmation": "❓ Супоридани объектро тасдиқ кунед",
    "invalid_file_type": "❌ Формати файл нодуруст аст. Файли Excel (.xlsx) бор кунед",
    "members_added_successfully": (
        "📊 Натиҷаи илова кардани коргарон:\n\n"
        "✅ Бомуваффақият илова шуд: {success_count}\n"
        "❌ Илова нашуд: {failed_count}\n\n"
        "❗️ Сабабҳои рад кардан:\n"
        "{failed_reasons}"
    ),
    "no_more_pages": "❌ Дигар саҳифаҳо нестанд",
    "no_users_tg_id": "❌ ID-и корбарро нишон диҳед: /user_tools_xlsx <user_id>",
    "no_valid_tools": "❌ Дар файл маълумоти дуруст дар бораи асбобҳо нест",
    "no_valid_user_ids": "❌ ID-ҳои дурусти Telegram ёфт нашуданд",
    "no_valid_users_found": "❌ Корбарон бо ID-ҳои нишондодашуда ёфт нашуданд",
    "notification_failed": "❌ Ҳангоми фиристодани огоҳинома хато рух дод",
    "notification_to_user": "📬 Огоҳиномаи нав аз {sender}",
    "object_control_title": "🏗 Идоракунии объектҳо",
    "object_data_format": (
        "📝 Ном: {name}\n"
        "ℹ️ Тавсиф: {description}\n"
        "📅 Сохта шуд: {created_at}\n"
        "👤 Созанда: {creator}"
    ),
    "object_data_header": "🏗 Маълумот дар бораи объект:",
    "object_deleted": "✅ Объект нест карда шуд",
    "object_updated": "✅ Маълумоти объект нав карда шуд",
    "operation_in_progress": "⏳ Амалиёт иҷро шуда истодааст...",
    "page_info": "Саҳифаи {current} аз {total}",
    "reminder_created": "✅ Ёдоварӣ сохта шуд",
    "reminder_deactivated": "✅ Ёдоварӣ ғайрифаъол карда шуд",
    "reminder_updated": "✅ Ёдоварӣ нав карда шуд",
    "return_to_tools_control": "🔄 Бозгашт ба идоракунии асбобҳо",
    "setup_cancelled": "❌ Танзимот бекор карда шуд",
    "setup_complete": "✅ Танзимот анҷом ёфт",
    "tg_id_must_be_number": "❌ ID-и корбар бояд рақам бошад",
    "tmc_bulk_upload_complete": "✅ Бор карда шуд: асбобҳо: {success}\n❌ Хатоҳо: {errors}",
    "tmc_invalid_file": "❌ Файли нодуруст",
    "tmc_upload_btn": "TMC",
    "tmc_upload_instruction": "📝 Файли пуркардашудаи Excel-ро бо асбобҳо бор кунед",
    "tmc_upload_stopped": "✅ Боркунии асбобҳо қатъ карда шуд",
    "tools_export_btn": "Содироти асбобҳо",
    "upload_document_first": "❌ Аввал ҳуҷҷатро бор кунед",
    "upload_without_docs_btn": "📄 Бе ҳуҷҷатҳо сохтан"
    },
}

if __name__ == "__main__":
    ru_keys = set(TEXTS_TRANSLITE["ru"].keys())
    uz_keys = set(TEXTS_TRANSLITE["uz"].keys())
    tg_keys = set(TEXTS_TRANSLITE["tg"].keys())
    
    # Находим ключи, которых нет в узбекском переводе
    missing_in_uz = ru_keys - uz_keys
    # Находим ключи, которых нет в таджикском переводе
    missing_in_tg = ru_keys - tg_keys
    
    print("Количество ключей:")
    print(f"Русский: {len(ru_keys)}")
    print(f"Узбекский: {len(uz_keys)}")
    print(f"Таджикский: {len(tg_keys)}")
    
    print("\nОтсутствующие ключи в узбекском переводе:")
    for key in sorted(missing_in_uz):
        print(f"- {key}")
        
    print("\nОтсутствующие ключи в таджикском переводе:")
    for key in sorted(missing_in_tg):
        print(f"- {key}")