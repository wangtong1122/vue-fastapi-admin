这是 **Tortoise ORM + Aerich** 在实际项目里**非常常见**、也**很容易踩坑**的问题。我们分场景说清楚你后面应该怎么处理，以及**不要怎么做**。

---

## 一、先明确 Aerich 的“前提假设”

Aerich **强依赖一个前提**：

> 👉 **数据库当前结构 = Aerich 记录的最新 migration 状态**

这个状态是通过数据库里的表：

```sql
aerich
```

来维护的。

如果你 **之前手工建表 / 用别的工具改过表 / 直接跑 SQL**，而 **没有通过 aerich migrate + upgrade**，那就出现了 **状态不一致**。

---

## 二、常见 3 种实际场景 & 正确处理方式

---

## ✅ 场景 1：数据库是“空的”或可以随便重建（开发环境）

**这是最简单、最推荐的方式**

### ✔ 正确做法（推荐）

```bash
# 1. 删除数据库（或清空）
drop database xxx;

# 2. 重新初始化
aerich init -t your_project.settings.TORTOISE_ORM

# 3. 初始化 migration
aerich init-db
```

👉 这一步会：

* 创建所有表
* 创建 `aerich` 表
* 建立“干净”的 migration 基线

**开发环境强烈建议这样做**

---

## ⚠ 场景 2：数据库已有数据，之前不是用 Aerich 管的（生产 / 测试）

⚠️ **这是最危险、也是最常见的情况**

### ❌ 错误做法（千万别）

```bash
aerich migrate
aerich upgrade
```

很可能会：

* 重复建表
* 字段冲突
* 把已有数据搞挂

---

### ✔ 正确做法：**“对齐状态”，而不是“重建”**

核心目标一句话：

> **告诉 Aerich：现在数据库的结构，就是“最新状态”**

#### Step 1：初始化 aerich（不动表）

```bash
aerich init -t your_project.settings.TORTOISE_ORM
```

#### Step 2：生成 migration，但不真正执行

```bash
aerich migrate --name init_schema
```

此时会生成一个 migration 文件，里面通常是：

```python
async def upgrade(db):
    pass
```

#### Step 3：**手动标记为已执行（关键）**

```bash
aerich upgrade --fake
```

👉 这一步只会：

* 写 `aerich` 表
* **不会对数据库执行任何 SQL**

此时：

✅ 数据库结构
✅ Tortoise models
✅ Aerich 版本记录

三者 **状态统一**

---

### ✔ 后续就可以正常使用 Aerich 了

之后你再：

```bash
aerich migrate
aerich upgrade
```

就都是**增量变更**，不会乱来。

---

## 🔥 场景 3：已经执行过一部分 aerich，又被手改过数据库

这是**最复杂的场景**，但现实中经常发生。

### 判断标准

```sql
select * from aerich;
```

* 有记录 → Aerich 已“部分接管”
* 但表结构 ≠ models → 已失控

---

### 处理策略（推荐）

#### ✔ 方案 A（最安全）：回滚 / 重建（非生产）

```bash
aerich downgrade
# 或
清库重建
```

#### ✔ 方案 B（生产）：**手动修复 + fake**

1. **人工把数据库改回 models 结构**
2. 再跑：

   ```bash
   aerich migrate
   aerich upgrade --fake
   ```

👉 Aerich 只记录版本，不动真实表

---

## 三、团队级别最佳实践（非常重要）

### ✅ 1. 明确一条铁律

> **数据库结构只能通过 Aerich 改**

禁止：

* Navicat 手改
* 直接跑 DDL SQL
* 多人并行改表

---

### ✅ 2. CI 中强制校验

```bash
aerich migrate --check
```

如果 models 和 migration 不一致，直接失败。

---

### ✅ 3. 上线流程标准化

```bash
aerich upgrade
```

永远不手改表。

---

## 四、一句话总结（给你一个“心智模型”）

> **Aerich 管的是“变化历史”，不是“当前结构”**

如果历史缺失了，你要做的不是补历史，而是：

👉 **fake 一次，把当前结构当作历史起点**

---

如果你愿意，可以把你现在的情况贴出来（例如：

* 是否已有数据
* 是否存在 aerich 表
* 是否是生产库）

我可以给你 **精确到命令级别** 的处理方案。
