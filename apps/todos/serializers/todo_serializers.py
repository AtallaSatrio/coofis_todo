from datetime import timezone
from rest_framework import serializers
from apps.todos.models import Todo, Attachment
from apps.todos.serializers import attachment_serializers


class TodoSerializers(serializers.ModelSerializer):
    attachments = attachment_serializers.AttachmentSerializers(
        many=True, required=False
    )
    hf_attachments = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )

    class Meta:
        model = Todo
        fields = [
            "id",
            "tittle",
            "description",
            "priority",
            "hf_attachments",
            "attachments",
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        hf_attachments = validated_data.pop("hf_attachments")
        attachments = validated_data.pop("attachments")

        validated_data["creator"] = user

        obj_todo = Todo.objects.create(**validated_data)

        if hf_attachments:
            Attachment.objects.filter(id__in=hf_attachments).update(todo=obj_todo)
        if attachments:
            serializers = attachment_serializers.AttachmentSerializers(
                data=attachments, many=True, context={"obj_todo": obj_todo}
            )
            serializers.is_valid()
            serializers.save()

        return obj_todo

    def update(self, instance, validated_data):
        # get_hf_attachments = validated_data.get("hf_attachments")
        # get_attachments = validated_data.get("attachments")
        # hf_attachments = (
        #     validated_data.pop("hf_attachments") if get_hf_attachments else None
        # )
        # attachments = validated_data.pop("attachments") if get_attachments else None
        tittle = validated_data.get("title")
        description = validated_data.get("description")
        priority = validated_data.get("priority")
        get_hf_attachments = validated_data.get("hf_attachments")
        get_attachments = validated_data.get("attachments")
        hf_attachments = (
            validated_data.pop("hf_attachments") if get_hf_attachments else None
        )
        attachments = validated_data.pop("attachments") if get_attachments else None

        # instance = super(TodoSerializers, self).update(instance, validated_data)

        todo_instance = Todo.objects.filter(id=instance.id).first()
        todo_instance.title = tittle
        todo_instance.description = description
        todo_instance.priority = priority
        todo_instance.save()

        if hf_attachments:
            attach_old = Attachment.objects.filter(todo=todo_instance)
            attach_now = attach_old.exclude(id__in=hf_attachments)
            attach_now.delete()
            Attachment.objects.filter(id__in=hf_attachments).update(todo=todo_instance)

        if attachments:
            serializers = attachment_serializers.AttachmentSerializers(
                data=attachments, many=True, context={"obj_todo": todo_instance}
            )
            serializers.is_valid()
            serializers.save()

        return todo_instance


class TodoListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ["id", "tittle", "description", "priority", "created_at"]

    def get_created_at(self, obj):
        date = timezone.localtime(obj.created_at)
        formatted_date = date.strftime("%d %B %Y %H:%M:%S")
        return formatted_date


class TodoDestroySerializer(serializers.Serializer):
    id_todos = serializers.ListField(child=serializers.CharField(max_length=100))

    def destroy(self, validated_data):
        get_id_todos = validated_data.get("id_todos")
        Todo.objects.filter(id__in=get_id_todos).update(is_delete=True)
