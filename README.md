# PySpark 电商数据分析项目

使用 PySpark + Spark SQL 对电商订单数据进行多维分析，涵盖 DataFrame 操作、SQL 查询、窗口函数、子查询和结果导出。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Spark | 3.5.9 | 分布式计算引擎 |
| PySpark | 3.5.9 | Python API |
| Java | 8 | 运行时环境 |
| Python | 3.12.13 | miniconda 环境 |
| WSL2 + Ubuntu | - | Linux 开发环境 |
| VSCode | - | 开发工具 |

## 项目结构

```
pyspark-practice/
├── README.md                    # 项目说明（本文件）
├── b1_read_csv.py               # B1：读取 CSV + 列名设置
├── b1_write_csv.py              # B1：结果写入 CSV
├── b2_daily_sales.py            # B2：日销售额统计（union + groupBy）
├── b2_product_top10.py          # B2：商品销量 TOP10（join）
├── b2_city_rank.py              # B2：城市消费力排名（join + groupBy）
├── b3_sql.py                    # B3：Spark SQL 基础（临时视图 + spark.sql）
├── b4_ecommerce_analysis.py     # B4：综合实战项目（主脚本）
└── output/                      # 分析结果导出
    ├── each_day_sales/          # 每日销售额趋势
    ├── sales_num_top10/         # 商品销量 TOP10
    ├── city_sales_rank/         # 城市消费力排名
    ├── product_rank/            # 各分类销量冠军（窗口函数）
    ├── user_rank/               # 用户消费金额排名（窗口函数）
    └── avg_user_sales/          # 消费超客单价用户（子查询）
```

> 数据源位于 `~/hive-ecommerce-warehouse/data/`，由 Hive 电商数仓项目生成。

## 数据集说明

### users（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | INT | 用户ID |
| user_name | STRING | 用户名 |
| gender | STRING | 性别 |
| age | INT | 年龄 |
| city | STRING | 所在城市 |
| reg_date | STRING | 注册日期 |

共 50 条记录。

### products（商品表）

| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | INT | 商品ID |
| product_name | STRING | 商品名称 |
| category | STRING | 品类 |
| price | DOUBLE | 单价 |

共 30 条记录。

### orders（订单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | INT | 订单ID |
| user_id | INT | 用户ID |
| product_id | INT | 商品ID |
| amount | INT | 购买数量 |
| price | DOUBLE | 成交单价 |
| date | STRING | 订单日期 |

3 天数据（2024-07-01 ~ 2024-07-03），每天约 60-70 条，共约 198 条。

## 技术点覆盖

| 技术点 | 说明 |
|--------|------|
| SparkSession | 创建 Spark 会话 |
| spark.read.csv | 读取 CSV 文件（inferSchema 自动推断类型）|
| toDF() | 重命名列 |
| withColumn() + lit() | 添加常量列（日期标记）|
| union() | 合并多个 DataFrame |
| createOrReplaceTempView() | 注册临时视图 |
| spark.sql() | 执行 SQL 查询 |
| JOIN | 多表关联（orders ↔ users ↔ products）|
| GROUP BY + 聚合函数 | 分组统计（SUM / COUNT）|
| HAVING + 子查询 | 筛选消费超客单价用户 |
| 窗口函数 | ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) |
| ROUND() | 浮点精度处理 |
| df.write.csv() | 结果导出为 CSV |

## 业务分析需求

| # | 需求 | 涉及表 | 技术点 |
|---|------|--------|--------|
| 1 | 每日销售额趋势 | orders | GROUP BY + ROUND |
| 2 | 商品销量 TOP10 | orders + products | JOIN + GROUP BY + LIMIT |
| 3 | 城市消费力排名 | orders + users | JOIN + GROUP BY |
| 4 | 各分类销量冠军商品 | orders + products | JOIN + 窗口函数 ROW_NUMBER() |
| 5 | 用户消费金额排名 | orders + users | JOIN + 窗口函数 ROW_NUMBER() |
| 6 | 消费超客单价用户 | orders + users | JOIN + 子查询 + HAVING |

## 运行方式

```bash
# 启动 HDFS（如需）
start-dfs.sh

# 运行主脚本
cd ~/pyspark-practice
spark-submit b4_ecommerce_analysis.py

# 查看导出结果
ls output/
```
