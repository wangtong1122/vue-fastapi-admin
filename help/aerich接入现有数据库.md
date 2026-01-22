这是一个**标准但很容易做错**的问题 👍
核心一句话先给你：

> **Aerich 接入已有数据库 = 建立“基线迁移（baseline）”，而不是重建数据库**

下面我按 **可直接照做的步骤** 给你一套 **安全、可落地** 的方案。

---

## 一、接入现有数据库的正确思路（先立规则）

Aerich 的目标不是“分析数据库结构”，而是：

> **以当前 Tortoise models 为准，把它当作数据库的“既定事实”**

所以你要做的是：

* ✅ 数据库：保持不变
* ✅ models：写成**和当前数据库完全一致**
* ✅ Aerich：**从这一刻开始接管变更**

---

## 二、标准接入步骤（生产可用）

### 🟢 Step 0：确认前提（非常重要）

在继续之前，必须满足：

* 数据库 **已经存在**
* 表结构 **稳定**
* 你已经写好了 **Tortoise ORM models**
* **models 与数据库结构一一对应**

👉 如果 models 和数据库不一致，**先改 models，不要动数据库**

---

### 🟢 Step 1：安装 & 初始化 Aerich（不动数据库）

```bash
pip install aerich
```

```bash
aerich init -t your_project.settings.TORTOISE_ORM
```

只会生成：

```text
migrations/
aerich.ini
```

❌ 不会建表
❌ 不会改数据库

---

### 🟢 Step 2：生成“基线迁移文件”

```bash
aerich migrate --name init_schema
```

此时：

* Aerich 会对比 models
* 生成一个 migration 文件
* **upgrade() 里通常是 pass**

示例：

```python
async def upgrade(db):
    pass

async def downgrade(db):
    pass
```

👉 这是正确现象

---

### 🟢 Step 3：fake 执行迁移（关键一步）

```bash
aerich upgrade --fake
```

这一步做了什么？

* ✅ 创建 `aerich` 表（如果没有）
* ✅ 写入当前 migration 版本
* ❌ **不执行任何 DDL**

📌 **数据库结构 0 变化**

---

### 🟢 Step 4：验证接入是否成功

#### 1️⃣ 查看 aerich 表

```sql
select * from aerich;
```

能看到：

```text
version | app | content
```

#### 2️⃣ 再试一次 migrate

```bash
aerich migrate
```

结果应该是：

```text
No changes detected
```

🎉 说明 Aerich 已正确接管

---

## 三、从这一刻开始，你就可以正常用了

以后每一次表结构变更，流程统一为：

```bash
# 改 models
aerich migrate
aerich upgrade
```

---

## 四、常见踩坑 & 必须避免的错误

### ❌ 1. 用 init-db 接入已有库

```bash
aerich init-db  # ❌ 会尝试建表
```

**已有数据库严禁使用**

---

### ❌ 2. migrate 后直接 upgrade（没 fake）

```bash
aerich migrate
aerich upgrade  # ❌ 可能重复建表
```

👉 **首次一定要 --fake**

---

### ❌ 3. models 和数据库不一致就强行接入

后果：

* 后续 migrate 会生成大量错误 DDL
* 生产事故高风险

---

## 五、团队级最佳实践（强烈建议）

### ✅ 1. 给这次接入打 tag

```bash
migrations/
 └── models/
     └── 0001_init_schema.py
```

明确这是 **baseline**

---

### ✅ 2. 接入当天禁止结构变更

* 不改 models
* 不改数据库
* 只做一次对齐

---

### ✅ 3. 生产库永远用 fake

* **只有第一次 fake**
* 后面真实 upgrade

---

## 六、一句话总结（你可以记住这个）

> **Aerich 接入已有数据库，本质是：**
>
> 👉 *“承认现在的数据库就是最终态，并从今天开始记录变化”*

---

如果你愿意，你可以把下面信息贴出来，我可以帮你**精确到每一步命令**：

* 用的数据库（MySQL / PostgreSQL）
* 是否已有 `aerich` 表
* 是否是生产环境
* models 是否完全对齐数据库

我可以直接给你一套 **0 风险接入方案**。
