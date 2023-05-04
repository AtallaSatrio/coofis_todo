from django.db import models
from apps.common.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Todo(TimeStampedUUIDModel):
    class Priority(models.TextChoices):
        NORMAL = "normal", _("normal")
        URGENT = "urgent", _("urgent")

    tittle = models.CharField(verbose_name=_("tittle"), max_length=225)
    description = models.TextField(verbose_name=_("description"))
    priority = models.CharField(
        verbose_name=_("priority"),
        choices=Priority.choices,
        default=Priority.NORMAL,
        max_length=15,
    )
    creator = models.ForeignKey(
        "accounts.User",
        verbose_name=_("creator"),
        related_name="creator_todo",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "todo"
        verbose_name_plural = "todos"
        db_table = "todos_todo"

    def __str__(self):
        return self.name


class Attachment(TimeStampedUUIDModel):
    todo = models.ForeignKey(
        "todos.Todo",
        verbose_name=_("todo"),
        related_name=_("attachments"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100, verbose_name="Name", blank=True, null=True)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    file = models.FileField(
        verbose_name=_("file"), upload_to="attachments/", blank=True, null=True
    )

    class Meta:
        verbose_name = "attachment"
        verbose_name_plural = "attachments"
        db_table = "todos_attachment"

    def __str__(self):
        return self.name
