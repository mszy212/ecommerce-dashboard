# 电商数据分析仪表盘

基于 **PySpark 数据仓库 + Streamlit + Plotly** 的电商数据 BI 看板。

数据源自 PySpark 离线数仓项目（ODS → DWD → DWS → ADS 四层分层建模），
本仪表盘直接消费数仓产出的 Parquet 数据，实现在线交互式分析。

## 在线访问

> 部署后在此填写 Streamlit Cloud 链接

## 功能模块

### 全局指标卡

| 指标 | 说明 |
| --- | --- |
| 总销售额 | 全量订单金额汇总 |
| 总订单量 | 去重订单数 |
| 总用户数 | 去重用户数 |
| 总城市数 | 覆盖城市数量 |
| 平均客单价 | 总销售额 / 总订单量 |

### 分析标签页（每个标签页带独立筛选器）

| 标签页 | 分析内容 | 图表 | 筛选器 |
| --- | --- | --- | --- |
| 每日销售 | 每日销售额趋势 | 折线图 | 日期范围 |
| 品类销售 | 各品类销售表现 | 柱状图 | 品类多选 |
| 城市销售 | 城市销售排行 | 柱状图 | 城市多选 |
| 产品销售 | 商品销售排行 | 柱状图 | 商品多选 |
| 用户销售 | 用户消费排行 | 柱状图 | 用户多选 |
| 订单用户明细 | 明细宽表查询 | 数据表 | — |

## 技术栈

- **数据仓库**：PySpark（ODS / DWD / DWS / ADS 四层）
- **存储格式**：Parquet（列式存储）
- **可视化框架**：Streamlit（页面与交互）
- **图表库**：Plotly Express（交互式图表，支持悬停取值与缩放）

## 项目结构

```
ecommerce-dashboard/
├── app.py                     # 仪表盘主程序
├── requirements.txt           # 依赖清单
├── README.md
├── .streamlit/
│   └── config.toml            # 主题配置（深色）
└── warehouse/                 # 数仓数据（Parquet）
    ├── ads/                   # 应用层：5 张汇总结果表
    │   ├── each_day_sales/
    │   ├── category_top1/
    │   ├── city_sales_top10/
    │   ├── product_sales_top10/
    │   └── users_sales_top10/
    └── dwd/                   # 明细层：订单用户商品宽表
        └── dwd_orders_detail/
```

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开 http://localhost:8501 即可访问。

## 实现要点

- **数仓分层消费**：排行榜类指标取自 ADS 层预聚合结果，总量类指标（订单量、用户数）取自 DWD 明细宽表，避免 TOP10 截断导致的统计偏差
- **筛选器局部化**：筛选组件置于各自标签页内部，避免与当前分析维度无关的筛选器干扰页面
- **日期类型处理**：`order_date` 字符串转 datetime 用于范围筛选，再格式化为字符串用于图表横轴，规避时间刻度显示问题
- **金额单位处理**：图表与指标卡统一使用「万元」单位，解决大额数字显示截断与坐标轴单位混用问题
- **空筛选防呆**：筛选结果为空时给出友好提示，避免图表空白报错

## 相关项目

- [pyspark-practice](https://github.com/mszy212/pyspark-practice) — PySpark DataFrame API 与 Spark SQL 练习
- [pyspark-data-warehouse](https://github.com/mszy212/pyspark-data-warehouse) — PySpark 数仓分层建模（ODS/DWD/DWS/ADS）
