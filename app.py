# 导入库
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="电商数据分析仪表盘",
    layout="wide"
)
#设置页面标题
st.title('电商数据分析仪表盘')

#读取ads所有数据
each_day_df       = pd.read_parquet("warehouse/ads/each_day_sales")
category_top1_df  = pd.read_parquet("warehouse/ads/category_top1")
city_sales_top10_df     = pd.read_parquet("warehouse/ads/city_sales_top10")
product_sales_top10_df  = pd.read_parquet("warehouse/ads/product_sales_top10")
user_sales_top10_df     = pd.read_parquet("warehouse/ads/users_sales_top10")
df_order_users_products = pd.read_parquet("warehouse/dwd/dwd_orders_detail")


# 数据处理
sum_sales_amount = each_day_df['sales_amount'].sum()
wan_sales_amount = sum_sales_amount / 10000
# 指标卡
col1,col2,col3,col4,col5 = st.columns(5)
with col1:
    st.metric('总金额', f"¥{wan_sales_amount:,.0f}万")
with col2:
    st.metric('总订单数',f'{df_order_users_products["order_id"].nunique():,.0f}单')
with col3:
    st.metric('总用户数',f'{df_order_users_products["user_id"].nunique():,.0f}人')
with col4:
    st.metric('总城市数',f'{df_order_users_products["city"].nunique():,.0f}个')
with col5:
    st.metric('平均客单价',f'¥{each_day_df["sales_amount"].sum() / df_order_users_products["order_id"].nunique():,.0f}')

#用标签卡把页面分成五块
tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs(["每日销售", "品类销售", "城市销售", "产品销售", "用户销售","订单用户明细"]) 
with tab1:
    # 二级标题
    st.subheader("每日销售数据") 
    
    # 数据处理 类型的转换
    each_day_df['order_date'] = pd.to_datetime(each_day_df['order_date'])
    each_day_df["order_date_str"] = each_day_df["order_date"].dt.strftime("%Y-%m-%d")

    # 日期范围筛选
    min_date = each_day_df['order_date'].min()
    max_date = each_day_df['order_date'].max()
    data_range = st.date_input("选择日期范围", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    st.write('销售额单位：万元')
    # 根据日期范围过滤数据
    filtered_df = each_day_df[(each_day_df['order_date'] >= pd.to_datetime(data_range[0])) & 
    (each_day_df['order_date'] <= pd.to_datetime(data_range[1]))]
    # 显示图表和数据
    
    if filtered_df.empty:
        st.warning("当前筛选条件下暂无数据！")
    else:
        df_show6 = filtered_df.rename(columns={'order_date':'日期','sales_amount':'销售额'})
        df_show6['销售额'] = df_show6['销售额']/10000
        fig = px.line(df_show6, x="日期", y="销售额")
        df_show6 = df_show6[['日期','销售额']]
        st.plotly_chart(fig)
        st.dataframe(df_show6,hide_index=True)

with tab2:
    # 筛选
    select_category = st.multiselect('选择品类', 
    category_top1_df['category'].unique(), 
    category_top1_df['category'].unique())
    # 匹配对象
    filter_category_df = category_top1_df[category_top1_df['category'].isin(select_category)]
    st.subheader("品类销售数据")
    if filter_category_df.empty:
        st.warning("当前筛选条件下暂无数据！")
    else:
        df_show2 = filter_category_df.rename(columns={'category': '品类', 'sales_qty': '销售数量','product_name': '产品名称','rn': '当前本类排名'})
        fig = px.bar(df_show2, x="品类", y="销售数量")
        st.plotly_chart(fig)
        st.dataframe(df_show2,hide_index=True)

with tab3:
    st.subheader("城市销售数据")
    # 条件筛选 默认温州
    select_city = st.multiselect('选择城市', 
    city_sales_top10_df['city'].unique(), 
    city_sales_top10_df['city'].unique())
    # 匹配对象
    filter_city_sales_df = city_sales_top10_df[city_sales_top10_df['city'].isin(select_city)]
    # 显示图表和数据
    df_show3 = filter_city_sales_df.rename(columns={'city': '城市', 'sales_amount': '销售额','order_date': '订单日期'})
    fig = px.bar(df_show3, x="城市", y="销售额")
    if filter_city_sales_df.empty:
        st.warning("当前筛选条件下暂无数据！")
    else:
        st.plotly_chart(fig)
    st.dataframe(df_show3,hide_index=True)

with tab4:
    # 筛选
    select_product = st.multiselect('选择产品', 
    product_sales_top10_df['product_name'].unique(), 
    product_sales_top10_df['product_name'].unique())
    # 匹配对象
    filter_product_sales_df = product_sales_top10_df[product_sales_top10_df['product_name'].isin(select_product)]
    st.subheader("产品销售数据")
    df_show4 = filter_product_sales_df.rename(columns={'product_name': '产品名称', 'sales_qty': '销售数量','category': '品类','product_id': '产品ID'})
    fig = px.bar(df_show4, x="产品名称", y="销售数量")
    if filter_product_sales_df.empty:
        st.warning("当前筛选条件下暂无数据！")
    else:
        st.plotly_chart(fig)
    st.dataframe(df_show4,hide_index=True)

with tab5:
    # 筛选
    select_user = st.multiselect('选择用户', 
    user_sales_top10_df['user_name'].unique(), 
    user_sales_top10_df['user_name'].unique())
    # 匹配对象
    filter_user_sales_df = user_sales_top10_df[user_sales_top10_df['user_name'].isin(select_user)]
    st.subheader("用户销售数据")
    if filter_user_sales_df.empty:
        st.warning("当前筛选条件下暂无数据！")
    else:
    # 数据处理 更改列名 
        df_show5 = filter_user_sales_df.rename(columns={'user_name': '用户名称', 'sales_amount': '销售金额','user_id': '用户ID'})
        fig = px.bar(df_show5, x="用户名称", y="销售金额")
        st.plotly_chart(fig)
        st.dataframe(df_show5   ,hide_index=True)
with tab6:
    st.subheader('订单用户明细')
    # 数据处理 更改列名 
    df_show6 = df_order_users_products.rename(columns={'order_id': '订单ID', 'user_id': '用户ID', 'product_id': '产品ID','quantity': '数量', 'order_price': '价格', 'order_date': '订单日期',
    'product_name': '产品名称', 'category': '品类', 'city': '城市', 'total_amount': '销售金额'
    ,'user_name': '用户名称','age' : '年龄','gender' : '性别'})
# 显示订单用户明细数据      
    st.dataframe(df_show6,hide_index=True)

# 运行脚本
# streamlit run e1_app.py
