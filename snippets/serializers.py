"""
    Tutorial 4 Auth
"""
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        Tutorial4 auth
        多個 snippets 被同一個 User 建立
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'snippets',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
        User Group
    """
    class Meta:
        model = Group
        fields = ('name',)


class SnippetSerializer(serializers.ModelSerializer):
    """
        SnippetSerializer 改成 serializers.ModelSerializer
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    class Meta:     # 改成 ModelSerializer 需要定義 Meta (資料結構吧?!)
        model = Snippet
        fields = '__all__'
