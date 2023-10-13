from rest_framework import serializers

from products.models import Category, File, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'title', 'description', "avatar"]


class FileSerializer(serializers.ModelSerializer):
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ["id", "title", "file", "file_type"]

    def get_file_type(self, obj):
        return obj.get_file_type_display()


# class ProductSerializers(serializers.ModelSerializer):
#     categories = CategorySerializer(many=True)
#     files = FileSerializer(many=True)
#
#     class Meta:
#         model = Product
#         fields = ["title", "description", "avatar", "categories", "files"]


class ProductSerializers(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    files = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = ["title", "description", "avatar", "categories", "files", "url"]
