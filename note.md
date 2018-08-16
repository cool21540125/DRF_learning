
## DB
```sql
CREATE DATABASE IF NOT EXISTS `dj` CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER IF NOT EXISTS 'drf'@'localhost' IDENTIFIED BY 'morning';
GRANT ALL ON dj.* TO 'drf'@'localhost';
```


## start app && tables && user
```sh
python manage.py startapp quickstart
python manage.py migrate        # 建立 Django User 相關 Tables, 10張
python manage.py createsuperuser --email admin@example.com --username admin
# admin:password123
```


## quickstart/serializers.py
```py
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
```


## quickstart/views.py
```py
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
```


```sh
curl -H 'Accept: application/json; indent=4' -uadmin:password123 http://127.0.0.1:8000/users/
```


# Ch1

## project
```sh
python manage.py startapp snippets
# settings.py 改 INSTALLED_APPS
# 'snippets.apps.SnippetsConfig',
```


## snippets/models.py
```py

```
