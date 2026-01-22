# 初始化配置 执行1次
aerich init -t tests.backends.mysql.TORTOISE_ORM

# Init db 执行1次
aerich init-db

#生成迁移文件
aerich migrate --name drop_column

# 执行迁移
aerich upgrade

# 回滚迁移
aerich downgrade

# 查看当前版本
aerich current

# 查看迁移历史
aerich history

# 查看未应用的迁移
aerich heads

首次创建模型：aerich init -> aerich migrate -> aerich upgrade。
修改模型：修改models.py -> aerich migrate (生成新历史) -> aerich upgrade (应用新版本)。
回退：想要回退到之前版本，使用aerich downgrade <旧版本号>

aerich -c /Users/sunset/PycharmProjects/vue-fastapi-admin/app/db_script/aerich_demo/pyproject.toml migrate --name "delete_complete"
aerich -c /Users/sunset/PycharmProjects/vue-fastapi-admin/app/db_script/aerich_demo/pyproject.toml upgrade