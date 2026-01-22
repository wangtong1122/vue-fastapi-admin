from tortoise import fields, models


class Task(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    is_completed = fields.BooleanField(default=False)

    class Meta:
        table = "tasks"