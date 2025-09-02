# Подготовка нового сервера и развертывания на нем 3x-ui, с последующей миграции базы данных 3x-ui на новый сервер, средствами автоматизации Ansible  


###  Иерархическая структура для данного проекта:

```
root@ansible:/etc/ansible/migration# tree
.
├── ansible.cfg
├── certbot_migration.yml
├── inventory_stable
│   ├── actual_servers.yml
│   ├── new_servers.yml
│   ├── old_servers.yml
│   └── porkbun.yml
├── migration_playbook.yml
├── part2_migration.yml
├── playbooks
│   ├── 01_prepare_system.yml
│   ├── 02_install_3xui.yml
│   ├── 03_create_user.yml
│   ├── 04_configure_ssh.yml
│   ├── 05_install_fail2ban.yml
│   ├── 06_xray_update.yml
│   ├── 07_configure_3xui.yml
│   ├── 08_install_monitoring.yml
│   ├── 09_install_backup.yml
│   └── passwords
│       ├── vpn_passwords_new-server-1.txt
│       ├── vpn_passwords_new-server-2.txt
│       ├── vpn_passwords_new-server-(n).txt
│      
└── ssh_keys
    ├── id_ed25519
    └── id_ed25519.pub
```

- ansible.cfg - главный конфигурационный файл Ansible (описывает инвентори, способ подключения по SSH, формат вывода информации, например в YAML)
- certbot_migration.yml - плейбук для установки  SSL сертификатов для домена 3 уровня через Certbot
- inventory_stable - каталог где расположены файлы описывающие хосты и другие переменные
- part2_migration.yml - данный плейубук создан для повторной  миграции баз данных 3x-ui
- migration_playbook.yml -   данный плейубук производит миграцию баз данных 3x-ui
- 01_prepare_system.yml  -   устанавливает базовые пакеты на сервере ( unzip, figlet, wget, certbot)
- 02_install_3xui.yml - устанавливает 3x-ui на новом сервере
- 03_create_user.yml - создает пользователя для нового сервера
- 04_configure_ssh.yml - настройка ssh по ключу, отключение входа через root  и установка кастомного порта для ssh
- 05_install_fail2ban.yml -  настройка фейлтубан
- 06_xray_update.yml - обновления xray ядра в 3x-ui
- 07_configure_3xui.yml - настройка 3x-ui
- 08_install_monitoring.yml - установка и настройка node_exporter
- passwords - каталог где хранятся креды от новых серверов
- ssh_keys - ssh ключ для подключения к новым серверам

