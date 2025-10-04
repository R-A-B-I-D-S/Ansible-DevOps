#!/usr/bin/env python3
"""
Semaphore Webhook Server для Telegram уведомлений
Принимает webhook'и от Semaphore и отправляет красивые сообщения в Telegram
"""

import json
import os
import sys
import requests
import argparse
from datetime import datetime
from flask import Flask, request, jsonify
from typing import Dict, Any

app = Flask(__name__)

class TelegramNotifier:
    def __init__(self, config_file: str):
        """Загрузка конфигурации"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.bot_token = self.config['telegram_bot_token']
        self.chat_id = self.config['telegram_chat_id']
        self.topic_id = self.config.get('telegram_topic_id')
        
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    
    def send_message(self, message: str) -> bool:
        """Отправка сообщения в Telegram"""
        try:
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            # Добавляем topic_id если указан (для супергрупп)
            if self.topic_id:
                data['message_thread_id'] = self.topic_id
            
            response = requests.post(self.api_url, data=data, timeout=30)
            response.raise_for_status()
            
            print("✅ Сообщение отправлено в Telegram")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка отправки в Telegram: {e}")
            return False
    
    def parse_semaphore_data(self, data: Dict[Any, Any]) -> Dict[str, Any]:
        """Парсинг данных от Semaphore"""
        result = {
            'task_name': data.get('task', {}).get('template', {}).get('name', 'Unknown Task'),
            'status': data.get('task', {}).get('status', 'unknown'),
            'user': data.get('task', {}).get('user', {}).get('name', 'Unknown User'),
            'created_at': data.get('task', {}).get('created_at', ''),
            'started_at': data.get('task', {}).get('started_at', ''),
            'ended_at': data.get('task', {}).get('ended_at', ''),
            'project_name': data.get('project', {}).get('name', 'Unknown Project'),
            'output': data.get('task', {}).get('output', ''),
            'errors': []
        }
        
        # Парсинг вывода для извлечения информации о серверах
        if result['output']:
            result['servers'] = self.parse_ansible_output(result['output'])
        else:
            result['servers'] = {}
        
        return result
    
    def parse_ansible_output(self, output: str) -> Dict[str, Dict]:
        """Парсинг вывода Ansible для извлечения информации о серверах"""
        servers = {}
        lines = output.split('\n')
        current_server = None
        
        for line in lines:
            line = line.strip()
            
            # Определение сервера
            if 'PLAY [' in line and ']' in line:
                server_match = line.split('[')[1].split(']')[0]
                current_server = server_match
                servers[current_server] = {
                    'status': 'unknown',
                    'tasks': [],
                    'errors': []
                }
                continue
            
            # Определение статуса задач
            if current_server and ('ok=' in line or 'changed=' in line or 'failed=' in line):
                if 'failed=' in line and 'failed=0' not in line:
                    servers[current_server]['status'] = 'failed'
                elif servers[current_server]['status'] != 'failed':
                    servers[current_server]['status'] = 'success'
        
        return servers
    
    def format_message(self, parsed_data: Dict[str, Any]) -> str:
        """Форматирование сообщения для Telegram"""
        # Определение статуса и эмодзи
        if parsed_data['status'] == 'success':
            status_emoji = "✅"
            status_text = "УСПЕШНО"
        elif parsed_data['status'] == 'error':
            status_emoji = "❌"
            status_text = "С ОШИБКАМИ"
        else:
            status_emoji = "⚠️"
            status_text = "НЕИЗВЕСТНО"
        
        # Форматирование времени
        try:
            if parsed_data['started_at'] and parsed_data['ended_at']:
                start_time = datetime.fromisoformat(parsed_data['started_at'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(parsed_data['ended_at'].replace('Z', '+00:00'))
                duration = end_time - start_time
                duration_str = f"{duration.seconds // 60}m {duration.seconds % 60}s"
            else:
                duration_str = "Неизвестно"
        except:
            duration_str = "Неизвестно"
        
        # Заголовок
        message_lines = [
            f"<b>{status_emoji} {parsed_data['task_name'].upper()} - {status_text}</b>",
            f"🕐 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"👤 <b>Пользователь:</b> {parsed_data['user']}",
            f"📁 <b>Проект:</b> {parsed_data['project_name']}",
            f"⏱️ <b>Длительность:</b> {duration_str}",
            ""
        ]
        
        # Детали по серверам
        if parsed_data['servers']:
            message_lines.append("<b>📋 Детали по серверам:</b>")
            
            successful_count = 0
            failed_count = 0
            
            for server_name, server_data in parsed_data['servers'].items():
                if server_data['status'] == 'success':
                    server_emoji = "✅"
                    successful_count += 1
                elif server_data['status'] == 'failed':
                    server_emoji = "❌"
                    failed_count += 1
                else:
                    server_emoji = "⚠️"
                
                message_lines.append(f"{server_emoji} <b>{server_name}</b>")
            
            # Статистика
            total_servers = len(parsed_data['servers'])
            message_lines.append("")
            message_lines.append(f"📊 <b>Статистика:</b> {successful_count}/{total_servers} серверов")
            
            if failed_count > 0:
                message_lines.append(f"❌ <b>Ошибок:</b> {failed_count}")
        
        # Подпись
        message_lines.append("")
        message_lines.append("<i>🤖 Semaphore Webhook Bot</i>")
        
        return "\n".join(message_lines)

# Глобальный экземпляр нотификатора
notifier = None

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик webhook'а от Semaphore"""
    try:
        # Проверка токена аутентификации
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Получение данных
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        print(f"📨 Получен webhook от Semaphore: {data.get('task', {}).get('template', {}).get('name', 'Unknown')}")
        
        # Парсинг и отправка уведомления
        parsed_data = notifier.parse_semaphore_data(data)
        message = notifier.format_message(parsed_data)
        
        # Отправка в Telegram
        success = notifier.send_message(message)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Notification sent'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send notification'}), 500
            
    except Exception as e:
        print(f"❌ Ошибка обработки webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервера"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/test', methods=['POST'])
def test():
    """Тестовая отправка сообщения"""
    try:
        test_message = f"""🤖 <b>ТЕСТОВОЕ СООБЩЕНИЕ</b>
🕐 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
✅ Webhook сервер работает корректно!

<i>🤖 Semaphore Webhook Bot</i>"""
        
        success = notifier.send_message(test_message)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Test message sent'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send test message'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description="Semaphore Webhook Server для Telegram")
    parser.add_argument("--config", required=True, help="Путь к файлу конфигурации")
    parser.add_argument("--host", default="0.0.0.0", help="Хост для привязки")
    parser.add_argument("--port", type=int, default=5000, help="Порт для привязки")
    parser.add_argument("--debug", action="store_true", help="Режим отладки")
    
    args = parser.parse_args()
    
    # Проверка существования конфигурации
    if not os.path.exists(args.config):
        print(f"❌ Файл конфигурации не найден: {args.config}")
        sys.exit(1)
    
    # Инициализация нотификатора
    global notifier
    try:
        notifier = TelegramNotifier(args.config)
        print("✅ Конфигурация загружена")
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации: {e}")
        sys.exit(1)
    
    # Запуск сервера
    print(f"🚀 Запуск webhook сервера на {args.host}:{args.port}")
    print(f"📡 Webhook URL: http://{args.host}:{args.port}/webhook")
    print(f"❤️ Health check: http://{args.host}:{args.port}/health")
    print(f"🧪 Test endpoint: http://{args.host}:{args.port}/test")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
