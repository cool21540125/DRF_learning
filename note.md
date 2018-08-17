# DjangoRestFramework

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

sni1 = Snippet(id='1', code='Hello')
sni2 = Snippet(id='2', code='Hi')
sni1.save()
sni2.save()

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

    使用 serializers.ModelSerializer 取代 serializers.Serializer (兩者皆為 Form 的概念)
    而 ModelSerializer 直接給定 Meta , 
    1. 直接套用 models 定義好的 schema 來當作 metadata
    2. 預設實作了簡單版的 create() 及 update()

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



# Tutorial 2

使用 API views 來包裹 
1. `@api_view` decorator
2. APIView class

可以處理異常的請求資料 (用 `request.data` 解析 `request body` ), 錯誤會回傳 `ParseError` ; 解除強制回應成 JSON type, `JsonResponse(...)` 改成 `Response(...)`, 回應格是會依照 `content negotiation` 來作處理.

```py
# 去改 snippets/views
# page Ch2 - p2/6, p3/6
```

```py
"""
    proj.urls.py
"""
from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/', include('snippets.urls')),
]


"""
    snippets.urls.py
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```


```sh
# 可改變請求類型, 乃至於其他後端開放的 content negotiation 的 data type.
# http://localhost:8000/api/snippets.api/
# http://localhost:8000/api/snippets.json/
```



# 好用套件

- [DRF-auto API doc](https://github.com/iMakedonsky/drf-autodocs)

```sh
pip install drf_autodocs
```

```py
# settings.py
INSTALLED_APPS = [
    ...
    'drf_autodocs',
    ...
]

# project.urls.py
urlpatterns = [
    ...
    url(r'^', include('drf_autodocs.urls')),
]
```

localhost:8000/docs/

目前看不出效果=..=


# Tutorial 3

PASS



# Tutorial 4 - Authentication & Permissions

```py
# 增加到 snippets/models.py 的 Snippet
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

class Snippet(models.Model):
    # ...
    ### 多此 2 屬性
    owner = models.ForeignKey('auth.User', related_name='Snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    ### 多此方法
    def save(self, *args, **kwargs):
        """
            用 pygments 建立 highlighted HTML -> code snippet
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)
```

之後更新資料庫, 為了方便操作
1. Drop DB
2. Drop snippets/migrations
3. `python manage.py makemigrations snippets`    產生 snippets/migrations & Table:django_migrations
4. `python manage.py migrate`                   產生其他相關 tables


```py
# python manage.py shell
## 重創
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

sni1 = Snippet(id='1', code='Hello', owner_id=1)
sni2 = Snippet(id='2', code='Python Code', owner_id=1)
sni3 = Snippet(id='3', language='java', code='Java', owner_id=2)

sni1.save()
sni2.save()
sni3.save()

ser1 = SnippetSerializer(sni1)
ser2 = SnippetSerializer(sni2)
ser3 = SnippetSerializer(sni3)
```