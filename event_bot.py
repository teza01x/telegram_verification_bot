import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from sql_scripts import *
from functions import *
from dictionary_for_bot import *
from googlesheet import *

bot = AsyncTeleBot(token)


@bot.message_handler(commands=['start', 'menu'])
async def start(message):
    ## User Panel, Start Menu /start
    user_id = message.chat.id
    user = message.from_user
    username = user.username
    if not user_exists(user_id):
        try:
            add_user(user_id, username)
            add_user_app(user_id, username)
        except Exception as e:
            print("Error {}".format(e))

    button_list1 = [
        types.InlineKeyboardButton(btn['apply'], callback_data="apply_request"),
    ]
    reply_markup = types.InlineKeyboardMarkup([button_list1])

    old_menu = check_start_menu_id(user_id)
    if old_menu:
        try:
            await bot.delete_message(message.chat.id, old_menu)
        except telebot.apihelper.ApiException:
            pass

    menu_message = await bot.send_message(message.chat.id, dct["start"], reply_markup=reply_markup)
    menu_id = menu_message.message_id
    add_start_menu_id(user_id, menu_id)


# command /key kyliej@gmail.com 123, gives user with email kyliej@gmail.com key with number 123
@bot.message_handler(commands=['key'])
async def set_key(message):
    user_id = message.chat.id
    with open('admin_id.txt', 'r') as file:
        admin_id = file.readline()
    if int(admin_id) == user_id:
        email, key = await clean_text(message.text, '/key')
        set_user_key(email, key)
        await bot.send_message(user_id, dct['set_key'].format(email, key))
        _values = get_verification_user_data()
        update_values(table_id, "A2:F1000", "USER_ENTERED", _values)


# /n, short of notification, mass notification for all verificated users
@bot.message_handler(commands=['n'])
async def mass_notification(message):
    user_id = message.chat.id
    with open('admin_id.txt', 'r') as file:
        admin_id = file.readline()
    if int(admin_id) == user_id:
        lst = notification_for_ver_users()
        notification = await clean_text_notification(message.text, '/n')
        for id in lst:
            await bot.send_message(id, notification)


# command /admin vasiliy@gmail.com, gives user with email (example: vasiliy@gmail.com) admin rights
@bot.message_handler(commands=['admin'])
async def mass_notification(message):
    pass

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    ## User Panel, "Start Verification" Button, Questionnaire Menu
    if call.data == "apply_request":
        user_id = call.message.chat.id
        if check_verification(user_id) == 1:
            key = check_user_key(user_id)
            if key != 0 or key != None:
                button_list1 = [
                    types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list1])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=dct['verification_complete_key'].format(key), reply_markup=reply_markup)
            else:
                button_list1 = [
                    types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list1])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=dct['verification_complete'], reply_markup=reply_markup)
        else:
            if check_app_status(user_id) == 2:
                button_list2 = [
                    types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                ]

                reply_markup2 = types.InlineKeyboardMarkup([button_list2])

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=dct["wait"],
                                            reply_markup=reply_markup2)
            else:
                status_update(user_id, 0)
                user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
                if check_referal_code(user_id) != 0:
                    button_list1 = [
                        types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                        types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
                    ]
                    button_list2 = [
                        types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                        types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
                    ]
                    button_list3 = [
                        types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
                    ]
                    button_list4 = [
                        types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                    ]
                    button_list5 = [
                        types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
                    ]
                    reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
                else:
                    button_list1 = [
                        types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                        types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
                    ]
                    button_list2 = [
                        types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                        types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
                    ]
                    button_list3 = [
                        types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
                    ]
                    button_list4 = [
                        types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
                    ]
                    button_list5 = [
                        types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
                    ]
                    reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)

    ## Custom Panel, Name Button
    elif call.data == "user_name":
        user_id = call.message.chat.id
        status_update(user_id, 1)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['re_name'], reply_markup=reply_markup)

    ## User Panel, Email Button
    elif call.data == "user_email":
        user_id = call.message.chat.id
        status_update(user_id, 2)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['re_mail'], reply_markup=reply_markup)

    ## Custom Panel, Instagram Button
    elif call.data == "user_insta":
        user_id = call.message.chat.id
        status_update(user_id, 3)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['re_insta'], reply_markup=reply_markup)

    ## User Panel, Phone Button
    elif call.data == "user_phone":
        user_id = call.message.chat.id
        status_update(user_id, 4)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['re_phone'], reply_markup=reply_markup)


    ## User panel, "Referral code" button
    elif call.data == "user_referal":
        user_id = call.message.chat.id
        status_update(user_id, 5)
        button_list1 = [
            types.InlineKeyboardButton(btn['cancel'], callback_data="cancel"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct['re_code'], reply_markup=reply_markup)


    ## User panel, Back button during editing, Questionnaire menu
    elif call.data == "cancel":
        user_id = call.message.chat.id
        status_update(user_id, 0)

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))

        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['profile'].format(user_name, user_email, user_insta, user_phone,
                                                                   check_referal_code(user_id)),
                                        reply_markup=reply_markup)
        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=dct['profile'].format(user_name, user_email, user_insta, user_phone,
                                                                   ' (Необязательно)'), reply_markup=reply_markup)

    ## User panel, return to start menu
    elif call.data == "start":
        user_id = call.message.chat.id
        status_update(user_id, 0)
        button_list1 = [
            types.InlineKeyboardButton(btn['apply'], callback_data="apply_request"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list1])

        menu_message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["start"],
                                    reply_markup=reply_markup)
        menu_id = menu_message.message_id
        add_start_menu_id(user_id, menu_id)

    ## User panel, submitting an application for consideration
    elif call.data == "send_apply":
        user_id = call.message.chat.id
        user_name, user_email, user_insta, user_phone = get_user_info(user_id)
        user_send_app(user_id, user_name, user_email, user_insta, user_phone, 1)

        button_list1 = [
            types.InlineKeyboardButton(btn['accept_app'], callback_data="accept"),
            types.InlineKeyboardButton(btn['decline_app'], callback_data="decline"),
        ]

        reply_markup1 = types.InlineKeyboardMarkup([button_list1])

        button_list2 = [
            types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
        ]

        reply_markup2 = types.InlineKeyboardMarkup([button_list2])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["wait"],
                                    reply_markup=reply_markup2)

        referal_code = check_referal_code(user_id)
        inv_inst = get_inviter_inst_by_key(referal_code)
        with open('admin_id.txt', 'r') as file:
            admin_id = file.readline()
        if inv_inst != None:
            message = await bot.send_message(admin_id, dct["users_apply_rec"].format(user_name, user_email, user_insta, user_phone, inv_inst[0]), reply_markup=reply_markup1)
            change_app_status(user_id, 2)
            message_id = message.message_id
            user_message_id(user_id, message_id)
        else:
            message = await bot.send_message(admin_id, dct["users_apply"].format(user_name, user_email, user_insta, user_phone), reply_markup=reply_markup1)
            change_app_status(user_id, 2)
            message_id = message.message_id
            user_message_id(user_id, message_id)

    ## Admin panel, application acceptance
    elif call.data == "accept":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)
        user_name, user_email, user_insta, user_phone = get_user_info(user_id)
        change_app_status(user_id, 4)
        verification_status(user_id, 1)

        username = get_username(message_id)
        link_to_chat = 'https://t.me/' + username

        button_list1 = [
            types.InlineKeyboardButton(btn['contact'], url=link_to_chat),
        ]


        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_accepted"].format(user_name, user_email, user_insta, user_phone),
                                    reply_markup=reply_markup)
        await bot.send_message(user_id, dct['once_congrat_verif'])
        _values = get_verification_user_data()
        update_values(table_id, "A2:F1000", "USER_ENTERED", _values)

    ## Admin panel, cancellation of the application
    elif call.data == "decline":
        message_id = call.message.message_id
        user_id = get_user_id(message_id)
        user_name, user_email, user_insta, user_phone = get_user_info(user_id)
        change_app_status(user_id, 3)

        message_id = call.message.message_id
        username = get_username(message_id)
        link_to_chat = 'https://t.me/' + username

        button_list1 = [
            types.InlineKeyboardButton(btn['contact'], url=link_to_chat),
        ]

        reply_markup = types.InlineKeyboardMarkup([button_list1])

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=dct["users_apply_declined"].format(user_name, user_email, user_insta,user_phone),
                                    reply_markup=reply_markup)
        await bot.send_message(user_id, dct['once_refusal_verif'])


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    user_id = message.chat.id
    if status_check(user_id) == 1:
        user_name = message.text
        name_entry(user_id, user_name)
        status_update(user_id, 0)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except telebot.apihelper.ApiException:
                pass

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

    elif status_check(user_id) == 2:
        user_mail = message.text
        mail_entry(user_id, user_mail)
        status_update(user_id, 0)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except telebot.apihelper.ApiException:
                pass

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

    elif status_check(user_id) == 3:
        user_inst = message.text
        insta_entry(user_id, user_inst)
        status_update(user_id, 0)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except telebot.apihelper.ApiException:
                pass

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)


    elif status_check(user_id) == 4:
        user_phn = message.text
        phone_entry(user_id, user_phn)
        status_update(user_id, 0)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except telebot.apihelper.ApiException:
                pass

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)


    elif status_check(user_id) == 5:
        user_referal_code = message.text
        set_referal_code(user_id, int(user_referal_code))
        status_update(user_id, 0)

        old_menu = check_start_menu_id(user_id)
        if old_menu:
            try:
                await bot.delete_message(message.chat.id, old_menu)
            except telebot.apihelper.ApiException:
                pass

        user_name, user_email, user_insta, user_phone = await data_clean(get_user_info(user_id))
        if check_referal_code(user_id) != 0:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, check_referal_code(user_id)), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)

        else:
            button_list1 = [
                types.InlineKeyboardButton(btn['name'], callback_data="user_name"),
                types.InlineKeyboardButton(btn['email'], callback_data="user_email"),
            ]
            button_list2 = [
                types.InlineKeyboardButton(btn['insta'], callback_data="user_insta"),
                types.InlineKeyboardButton(btn['phone'], callback_data="user_phone"),
            ]
            button_list3 = [
                types.InlineKeyboardButton(btn['referal'], callback_data="user_referal"),
            ]
            button_list4 = [
                types.InlineKeyboardButton(btn['start_menu'], callback_data="start"),
            ]
            button_list5 = [
                types.InlineKeyboardButton(btn['complete_apply'], callback_data="send_apply"),
            ]
            reply_markup = types.InlineKeyboardMarkup(
                [button_list1, button_list2, button_list3, button_list4, button_list5])

            menu_message = await bot.send_message(message.chat.id, text=dct['profile'].format(user_name, user_email, user_insta, user_phone, ' (Необязательно)'), reply_markup=reply_markup)
            menu_id = menu_message.message_id
            add_start_menu_id(user_id, menu_id)


async def main():
    while True:
        try:
            await bot.infinity_polling()
        except Exception as e:
            await print(f"⚠️ Bot has been crashed. Error: {str(e)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()