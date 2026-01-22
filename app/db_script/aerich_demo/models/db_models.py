from tortoise import fields, models


class Task(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255, null=True)
    is_done = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"