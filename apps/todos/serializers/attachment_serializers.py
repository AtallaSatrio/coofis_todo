import base64
from rest_framework import serializers
from apps.todos.models import Attachment
from django.core.files.base import ContentFile


class AttachmentSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    base64 = serializers.CharField(write_only=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Attachment
        fields = ["id", "name", "description", "file", "base64"]

    def create(self, validated_data):
        obj_todo = self.context.get("obj_todo")
        get_base64 = validated_data.get("base64")
        name = validated_data.get("name")
        description = validated_data.get("description")

        fmt, imgstr = get_base64.split(";base64,")
        file = ContentFile(base64.b64decode(imgstr))
        file_name = name.replace(" ", "_")
        obj_attachment = Attachment.objects.create(
            todo=obj_todo,
            name=file_name,
            description=description,
        )

        obj_attachment.file.save(file_name, file, save=True)

        return obj_attachment
