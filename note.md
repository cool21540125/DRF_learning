
```sh
pip install Django==1.11
pip install djangorestframework
pip install pylint-django
```

## DB
```sql
CREATE DATABASE IF NOT EXISTS `dj` CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER IF NOT EXISTS 'drf'@'localhost' IDENTIFIED BY 'morning';
GRANT ALL ON dj.* TO 'drf'@'localhost';
```


## start app && tables && user

```sh
python manage.py startapp quickstart
python manage.py migrate        # (初次使用) 建立 Django User 相關 Tables, 10張
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
pip install pygments
python manage.py startapp snippets
# settings.py 改 INSTALLED_APPS
# 'snippets.apps.SnippetsConfig',
```

```sql
DROP TABLE `django_migrations`;
DROP TABLE `django_admin_log`;
DROP TABLE `django_session`;
DROP TABLE `django_content_type`;
DROP TABLE `auth_user_user_permissions`;
DROP TABLE `auth_user_groups`;
DROP TABLE `auth_group_permissions`;
DROP TABLE `auth_permission`;
DROP TABLE `auth_group`;
DROP TABLE `auth_user`;
```


## snippets/models.py

```py
python manage.py makemigrations snippets        # migrate 之後, 建立 snippets/migrations/
python manage.py migrate                        # 依照 migrations 建立 Table
```


```py
# python manage.py shell

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

sni1 = Snippet(code='Hello')
sni1.save()

ser1 = SnippetSerializer(sni1)
ser2 = SnippetSerializer(sni2)

ser1.data
# {'id': 1, 'title': '', 'code': 'Hello', 'linenos': False, 'language': 'python', 'style': 'friendly'}

bb = JSONRenderer().render(ser1.data)
bb
# b'{"id":1,"title":"","code":"Hello","linenos":false,"language":"python","style":"friendly"}'

from django.utils.six import BytesIO
dd = JSONParser().parse(BytesIO(bb))
dd
# {'id': 1, 'title': '', 'code': 'Hello', 'linenos': False, 'language': 'python', 'style': 'friendly'}

s = SnippetSerializer(data=dd)
s.is_valid()
# True

s.validated_data
# OrderedDict([('title', ''), ('code', 'Hello'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])

s.save()
# <Snippet: Snippet object>

# 舊: ORM 查詢
Snippet.objects.all()
# <QuerySet [<Snippet: Snippet object>]>

# 新: 序列化查詢
ss1.data
# [OrderedDict([('id', 1), ('title', ''), ('code', 'Hello'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
```


`serializers.Serializer` 改成 `serializers.ModelSerializer`

```py
# snippets/serializers.py
class SnippetSerializer(serializers.ModelSerializer):   # 
    
    class Meta:     # 改成 ModelSerializer 需要定義 Meta (資料結構吧?!)
        model = Snippet
        fields = '__all__'

    # 其餘一樣
```

改完後重新進入 Shell
```py
# python manage.py shell
from snippets.serializers import SnippetSerializer
s= SnippetSerializer()
print(s)
# id = IntegerField(read_only=True)
# title = CharField(allow_blank=True, max_length=100, required=False)
# code = CharField(style={'base_template': 'textarea.html'})
# linenos = BooleanField(required=False)
# language = ChoiceField(choices=[('abap', 'ABAP'), ('abnf', 'ABNF'), ...], default='python')
# style = ChoiceField(choices=[('abap', 'abap'), ('algol', 'algol'), ...], default='friendly')
# created = DateTimeField(read_only=True)       # serializers.Serializer 無此欄位
```