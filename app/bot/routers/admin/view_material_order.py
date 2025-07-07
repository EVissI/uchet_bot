from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ItemCardCallback, ObjListCallback, build_item_card_kbd, build_paginated_list_kbd, get_material_order_type_select, MaterialOrderTypeCallback
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.dao import MaterialOrderDAO, ObjectDAO, ObjectMaterialOrderDAO
from app.db.models import ObjectMaterialOrder, User
from app.config import settings

from app.db.database import async_session_maker
from app.db.schemas import MaterialOrderFilter, ObjectFilterModel, ObjectMaterialOrderFilter
material_orders_view_router = Router()

@material_orders_view_router.message(
    F.text.in_(get_all_texts("material_order_view")), UserInfo()
)
async def process_material_orders_view(message: Message, user_info: User):
    await message.answer(
        text=get_text("select_material_order_type", user_info.language),
        reply_markup=get_material_order_type_select(context='view', lang=user_info.language,)
    )

@material_orders_view_router.callback_query(
    MaterialOrderTypeCallback.filter((F.type == "object") & (F.context == "view")), UserInfo()
)
async def process_material_orders_object_type_select(callback: CallbackQuery, user_info: User):
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, filters=ObjectFilterModel())
        if not objects:
            await callback.message.answer(
                text=get_text('no_objects_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            return
    await callback.message.edit_text(
        text=get_text("select_object", user_info.language)
        , reply_markup=build_paginated_list_kbd(objects, 
                                                context='material_orders_view_object',
                                                object_type='object')
    )
@material_orders_view_router.callback_query(
    ObjListCallback.filter((F.action == "select") & (F.context == "material_orders_view_object")),
    UserInfo()
)
async def process_material_orders_object_select(callback: CallbackQuery, callback_data: ObjListCallback, user_info: User):
    page = 1
    async with async_session_maker() as session:
        orders = await ObjectMaterialOrderDAO.find_all(session, ObjectMaterialOrderFilter(object_id=callback_data.id))
        if not orders:
            await callback.message.answer(get_text("no_material_orders_found", user_info.language))
            return

        total_orders = len(orders)
        order = orders[page - 1]
        order_text = get_text(
            "material_order_card",
            user_info.language,
            id=order.id,
            description=order.description,
            delivery_date=order.delivery_date
        )

        await callback.message.edit_text(
            text=order_text,
            reply_markup=build_item_card_kbd(
                item_id=order.id,
                total_pages=total_orders,
                current_page=page,
                lang=user_info.language,
                keyboard_type="material_order_view",
                order_type='object',
                sub_info=callback_data.id
            )
        )

@material_orders_view_router.callback_query(
    ItemCardCallback.filter((F.keyboard_type == "material_order_view") and (F.action.in_(['next','prev']))),
    UserInfo()
)
async def process_material_order_card_pagination(callback: CallbackQuery, callback_data: ItemCardCallback, user_info: User):
    if callback_data.action == "next":
        page = callback_data.current_page + 1
    if callback_data.action == "prev":
        page = callback_data.current_page - 1
    async with async_session_maker() as session:
        if callback_data.order_type == "general":
            orders = await MaterialOrderDAO.find_all(session, MaterialOrderFilter(is_active=True))
        if callback_data.order_type == "object":
            orders = await ObjectMaterialOrderDAO.find_all(session, ObjectMaterialOrderFilter(is_active=True,
                                                                                              object_id=callback_data.sub_info))
        total_orders = len(orders)
        if page < 1:
            page = 1
        if page > total_orders:
            page = total_orders
        order = orders[page - 1]
        order_text = get_text(
            "material_order_card",
            user_info.language,
            id=order.id,
            description=order.description,
            delivery_date=order.delivery_date
        )
        await callback.message.edit_text(
            text=order_text,
            reply_markup=build_item_card_kbd(
                item_id=order.id,
                total_pages=total_orders,
                current_page=page,
                lang=user_info.language,
                keyboard_type="material_order_view",
                order_type=callback_data.order_type,
                sub_info=callback_data.sub_info
            )
        )


@material_orders_view_router.callback_query(
    MaterialOrderTypeCallback.filter((F.type == "general") & (F.context == "view")), UserInfo()
)
async def process_material_orders_general_type_select(callback: CallbackQuery, user_info: User):
    page = 1
    async with async_session_maker() as session:
        orders = await MaterialOrderDAO.find_all(session, MaterialOrderFilter())
        if not orders:
            await callback.message.answer(get_text("no_material_orders_found", user_info.language))
            return

        total_orders = len(orders)
        order = orders[page - 1]
        order_text = get_text(
            "material_order_card",
            user_info.language,
            id=order.id,
            description=order.description,
            delivery_date=order.delivery_date
        )

        await callback.message.edit_text(
            text=order_text,
            reply_markup=build_item_card_kbd(
                item_id=order.id,
                total_pages=total_orders,
                current_page=page,
                lang=user_info.language,
                keyboard_type="material_order_view",
                order_type='general',
            )
        )

@material_orders_view_router.callback_query(
    ItemCardCallback.filter((F.keyboard_type == "material_order_view") & (F.action == "deactivate")),
    UserInfo()
)
async def process_material_order_deactivate(callback: CallbackQuery, callback_data: ItemCardCallback, user_info: User, state):
    order_type = callback_data.order_type
    async with async_session_maker() as session:
        if order_type == "object":
            order:ObjectMaterialOrder = await ObjectMaterialOrderDAO.find_one_or_none(session, ObjectMaterialOrderFilter(id=callback_data.item_id))
            if order.message_id:
                await callback.bot.delete_message(settings.TELEGRAM_GROUP_ID_MATERIAL_ORDER, order.message_id)
            await ObjectMaterialOrderDAO.deactivate(session, callback_data.item_id)
        if order_type == "general":
            order = await MaterialOrderDAO.find_one_or_none(session, MaterialOrderFilter(id=callback_data.item_id))
            if order.message_id:
                await callback.bot.delete_message(settings.TELEGRAM_GROUP_ID_MATERIAL_ORDER, order.message_id)
            await MaterialOrderDAO.deactivate(session, callback_data.item_id)
    await callback.message.answer(get_text("material_order_deactivated", user_info.language))
    await callback.message.delete()