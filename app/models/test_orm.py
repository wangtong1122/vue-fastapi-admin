from app.models import Order

if __name__ == '__main__':
    async  def create_order():
        await Tortoise.init(
            # 数据库连接,
            # 连接mysql pip install aiomysql
            db_url='mysql://root:iopagent@192.168.55.10:3306/iop_agent',
            # 指定管理的models，__main__ 🈯️当前文件的models.Model
            modules={'models': ['app.models']},
        )
        # await Order.filter(order_number="125").update(amount=200.00)
        m = await Order.all().count()
        print(m)

    from tortoise import run_async, Tortoise

    run_async(create_order())