# netbox-unacceptable-events


```bash
pip3 install netbox-unacceptable-events
```



Добавить в файле netbox/netbox/configuration.py

```
PLUGINS = [
    'ptuevents'
]
```

В командной строке
```
./manage.py migrate
```

Перезапустить сервер netbox.