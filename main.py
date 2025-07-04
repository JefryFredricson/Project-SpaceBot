import os
from dotenv import load_dotenv
import json
import threading

import asyncio
from telebot import TeleBot

from data.users import Users

import requests
import re

def photoSender(bot, message):
    date = isDate(message.text)
    r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date[2]}-{date[1]}-{date[0]}&thumbs=False")
    if r.status_code != 200:
        print(r.status_code, r.headers)
        bot.reply_to(message, "Что-то пошло не так, возможно в другой раз")
        return
    
    nasa = json.loads(r.content)
    print(nasa)
    if nasa['media_type'] == 'image':
        if "hdurl" in nasa:
            r = requests.get(nasa['hdurl'])
        else:
            r = requests.get(nasa['url'])
            
        if r.status_code != 200:
            bot.reply_to(message, "Это не моя вина, сервис не вернул фото")
            return
    
        bot.reply_to(message, f"Лови фотоку {date[0]}-{date[1]}-{date[2]}")
        bot.send_photo(message.chat.id, photo=nasa['url'], caption = nasa['explanation'])
        
    elif nasa['media_type'] == 'video':
        pass
    else:
        bot.reply_to(message, "Это не фото, я сожалею")
        print(f"media_type {nasa['media_type']} \t {nasa['url']}")
        return
    
    


if __name__ == "__main__":
    load_dotenv()
    global NASA_API_KEY
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    
    bot = TeleBot(TOKEN)
    users = Users('users.csv')
    
    @bot.message_handler(func=lambda message: not isDate(message.text) is False, content_types=['text'])
    def echo_message(message):
        bot.send_message(message.chat.id, "Ода, это дата!")
        
        sender_p = threading.Thread(target=photoSender, args=(bot, message, ))
        sender_p.start()
        print(isDate(message.text))
    
    @bot.message_handler(func=lambda message: users.isUser(message.from_user.id) is True, content_types=['text'])
    def echo_message(message):
        print("Old лох")
        bot.send_message(message.chat.id, "Вы подписаны на бота!")
    
    
    @bot.message_handler(func=lambda message: users.isUser(message.from_user.id) is False, content_types=['text'])
    def echo_message(message):
        print("New лох")
        bot.send_message(message.chat.id, "Вы не подписаны на бота")
        
    
    bot.infinity_polling()


msg = {
    'content_type': 'text', 
    'id': 8, 
    'message_id': 8, 
    'from_user': {
        'id': 1049136912, 
        'is_bot': False, 
        'first_name': 'Александр', 
        'username': 'snow_app', 
        'last_name': None, 
        'language_code': 'ru', 
        'can_join_groups': None, 
        'can_read_all_group_messages': None, 
        'supports_inline_queries': None, 
        'is_premium': None, 'added_to_attachment_menu': None, 'can_connect_to_business': None, 
        'has_main_web_app': None
        }, 
    'date': 1746534119, 
    'chat': {
        'id': 1049136912, 'type': 'private', 'title': None, 
        'username': 'snow_app', 'first_name': 'Александр', 'last_name': None, 'is_forum': None, 
        'max_reaction_count': None, 'photo': None, 'bio': None, 'join_to_send_messages': None, 
        'join_by_request': None, 'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None, 
        'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 
        'message_auto_delete_time': None, 'has_protected_content': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 
        'linked_chat_id': None, 'location': None, 'active_usernames': None, 'emoji_status_custom_emoji_id': None, 
        'has_hidden_members': None, 'has_aggressive_anti_spam_enabled': None, 'emoji_status_expiration_date': None, 
        'available_reactions': None, 'accent_color_id': None, 'background_custom_emoji_id': None, 
        'profile_accent_color_id': None, 'profile_background_custom_emoji_id': None, 'has_visible_history': None, 
        'unrestrict_boost_count': None, 'custom_emoji_sticker_set_name': None, 'business_intro': None, 
        'business_location': None, 'business_opening_hours': None, 'personal_chat': None, 'birthdate': None, 
        'can_send_paid_media': None, 'accepted_gift_types': None}, 
    'sender_chat': None, 'is_automatic_forward': None, 
    'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 
    'author_signature': None, 'text': '[eq', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 
    'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 
    'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_members': None, 'left_chat_member': None, 
    'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 
    'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 
    'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': None, 
    'message_thread_id': None, 'is_topic_message': None, 'chat_background_set': None, 'forum_topic_created': None, 
    'forum_topic_closed': None, 'forum_topic_reopened': None, 'has_media_spoiler': None, 'forum_topic_edited': None, 
    'general_forum_topic_hidden': None, 'general_forum_topic_unhidden': None, 'write_access_allowed': None, 
    'users_shared': None, 'chat_shared': None, 'story': None, 'external_reply': None, 'quote': None, 'link_preview_options': None, 
    'giveaway_created': None, 'giveaway': None, 'giveaway_winners': None, 'giveaway_completed': None, 'forward_origin': None, 
    'boost_added': None, 'sender_boost_count': None, 'reply_to_story': None, 'sender_business_bot': None, 'business_connection_id': None, 
    'is_from_offline': None, 'effect_id': None, 'show_caption_above_media': None, 'paid_media': None, 
    'refunded_payment': None, 'proximity_alert_triggered': None, 'video_chat_scheduled': None, 
    'video_chat_started': None, 'video_chat_ended': None, 'video_chat_participants_invited': None, 
    'web_app_data': None, 'message_auto_delete_timer_changed': None, 'gift': None, 'unique_gift': None, 
    'paid_message_price_changed': None, 'paid_star_count': None, 
    'json': {
        'message_id': 8, 
        'from': {'id': 1049136912, 'is_bot': False, 'first_name': 'Александр', 'username': 'snow_app', 'language_code': 'ru'}, 
        'chat': {'id': 1049136912, 'first_name': 'Александр', 'username': 'snow_app', 'type': 'private'}, 
        'date': 1746534119, 'text': '[eq'
        }
    }
