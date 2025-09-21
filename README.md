# 🚀 OfficialVPN Ansible

[![License: Beerware](https://img.shields.io/badge/License-Beerware-orange.svg)](https://spdx.org/licenses/Beerware.html)
[![Ansible](https://img.shields.io/badge/Ansible-2.17%2B-red.svg)](https://www.ansible.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 📖 О проекте

Автоматизация развертывания и управления инфраструктурой [Official-VPN](https://officialbot.org/) с использованием Ansible. Включает роли для настройки серверов, DNS-перезаписи и оркестрации окружений.

## 🎯 Возможности

- ✅ **Migration Playbooks**
- ✅ **Idempotent configuration**
- ✅ **Secrets management**
- ✅ **Porkbun system**
- ✅ **Backup functionality**
- ✅ **Monitoring deployment**
- ✅ **Remnanode orchestration**

## 📁 Структура проекта

``` 
├── backups/                 # Резервное копирование
├── inventories/             # Общие инвентори файлы
├── migration/               # Миграция инфраструктуры
├── porkbun-add-new/         # Добавление новых DNS записей
├── porkbun-dns/             # Управление DNS Porkbun
├── remnawave/               # Remnanode инфраструктура
├── roles/                   # Общие роли Ansible
├── samples/                 # Примеры конфигураций
├── semaphore_playbooks/     # Playbooks для Semaphore
└── zabbix-agent/           # Мониторинг Zabbix
```

## 🛠 Основные компоненты

### 🔄 **Migration System**
Полный набор плейбуков для миграции серверов:
- Подготовка системы
- Установка 3xUI
- Настройка SSH и безопасности
- Мониторинг и бэкапы

### 🌐 **Porkbun DNS Management**
Автоматизация DNS-записей:
- Создание/удаление записей
- Поиск записей по IP
- Массовая замена записей

### 📦 **Remnanode**
Оркестрация Remnanode:
- Создание нод
- Настройка Caddy
- Управление сертификатами

### 📊 **Monitoring**
Развёртывание Zabbix агентов для мониторинга инфраструктуры

### 💾 **Backups**
Система резервного копирования серверов

🔐 Безопасность

    Используем Ansible Vault для секретов
    SSH-ключи хранятся безопасно
    Контроль доступа через inventory


📄 Лицензия

Beerware License  - если мы встретимся, и тебе понравится этот код, купи мне пиво 😎
