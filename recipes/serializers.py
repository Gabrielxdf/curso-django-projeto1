from django.contrib.auth.models import User
from rest_framework import serializers

from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name'
    )
    category = serializers.StringRelatedField()  # calls the __str__ method
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    tag_objects = TagSerializer(
        many=True, source='tags'
    )

    def any_method_name(self, recipe):  # get_field_name or method_name param

        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
