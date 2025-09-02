# Установка Ansible

Установка ansible осуществляется 2 способами:
- Установка через APT
- Установка через pip

Устанавливаем нужные утилиты:
```
sudo apt install software-properties-common -y
```

### Установка через APT:
```
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt update 
sudo apt install ansible -y
```

### Проверка версии:

```
root@msko-freeradius:~# ansible --version
ansible [core 2.17.13]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True
```

### Установка через pip:


Создаем виртуальное окружение и запускаем установку
```
sudo apt install python3-pip -y
root@prm-xfreeradius:~# python3 -m venv myvenv
root@prm-xfreeradius:~# source myvenv/bin/activate
(myvenv) root@prm-xfreeradius:~# pip3 install ansible-core
(myvenv) root@prm-xfreeradius:~# ansible --version
ansible [core 2.19.1]
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /root/myvenv/lib/python3.12/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /root/myvenv/bin/ansible
  python version = 3.12.3 (main, Aug 14 2025, 17:47:21) [GCC 13.3.0] (/root/myvenv/bin/python3)
  jinja version = 3.1.6
  pyyaml version = 6.0.2 (with libyaml v0.2.5)
(myvenv) root@prm-xfreeradius:~#
```



