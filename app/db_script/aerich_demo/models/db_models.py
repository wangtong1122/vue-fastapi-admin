from tortoise import fields, models


class Task(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "tasks"