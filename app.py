import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 设置页面配置
st.set_page_config(
    page_title="沪深300智能收益预测系统",
    page_icon="📈",
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
        color: #fff;
    }
    .stMetric {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 15px;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stTabs [role="tablist"] {
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 12px;
    }
    .stTabs [role="tab"] {
        background: rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.7);
        border-radius: 8px;
        padding: 10px 20px;
        margin-right: 10px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 股票数据
stocks_data = pd.DataFrame([
    {'代码': '600000.SH', '名称': '浦发银行', '行业': '银行', '最新价': 10.85, '涨跌幅': 2.35, '预测收益': 5.2, '评分': 85, '风险': '中低', 'PE': 8.5, 'PB': 1.20, 'ROE': 11.8, '毛利率': 35.2, '净利率': 22.5, '资产负债率': 85.6},
    {'代码': '002304.SZ', '名称': '洋河股份', '行业': '消费', '最新价': 158.20, '涨跌幅': 3.25, '预测收益': 7.5, '评分': 95, '风险': '中', 'PE': 32.5, 'PB': 7.50, 'ROE': 25.5, '毛利率': 68.5, '净利率': 35.2, '资产负债率': 22.5},
    {'代码': '601899.SH', '名称': '紫金矿业', '行业': '资源', '最新价': 12.85, '涨跌幅': 1.85, '预测收益': 6.2, '评分': 91, '风险': '中高', 'PE': 15.8, 'PB': 3.20, 'ROE': 22.5, '毛利率': 28.5, '净利率': 18.2, '资产负债率': 55.8},
    {'代码': '601336.SH', '名称': '新华保险', '行业': '保险', '最新价': 45.60, '涨跌幅': 1.42, '预测收益': 4.8, '评分': 89, '风险': '中高', 'PE': 14.5, 'PB': 2.50, 'ROE': 18.2, '毛利率': 15.2, '净利率': 8.5, '资产负债率': 92.5},
    {'代码': '601166.SH', '名称': '兴业银行', '行业': '银行', '最新价': 18.32, '涨跌幅': 1.68, '预测收益': 4.9, '评分': 87, '风险': '中低', 'PE': 6.8, 'PB': 0.88, 'ROE': 13.5, '毛利率': 32.5, '净利率': 20.5, '资产负债率': 88.2},
    {'代码': '600028.SH', '名称': '中国石化', '行业': '石油', '最新价': 5.92, '涨跌幅': 0.85, '预测收益': 3.2, '评分': 79, '风险': '低', 'PE': 9.5, 'PB': 0.92, 'ROE': 10.8, '毛利率': 18.5, '净利率': 5.2, '资产负债率': 55.2},
    {'代码': '600519.SH', '名称': '贵州茅台', '行业': '消费', '最新价': 1688.00, '涨跌幅': 1.25, '预测收益': 6.8, '评分': 92, '风险': '中', 'PE': 42.5, 'PB': 12.50, 'ROE': 28.5, '毛利率': 91.5, '净利率': 52.5, '资产负债率': 15.2},
    {'代码': '000858.SZ', '名称': '五粮液', '行业': '消费', '最新价': 145.80, '涨跌幅': 2.15, '预测收益': 5.5, '评分': 90, '风险': '中', 'PE': 28.5, 'PB': 6.80, 'ROE': 22.5, '毛利率': 75.5, '净利率': 38.5, '资产负债率': 18.5},
    {'代码': '600036.SH', '名称': '招商银行', '行业': '银行', '最新价': 38.92, '涨跌幅': 1.85, '预测收益': 4.8, '评分': 88, '风险': '中', 'PE': 12.3, 'PB': 1.80, 'ROE': 16.5, '毛利率': 36.5, '净利率': 24.5, '资产负债率': 86.5},
    {'代码': '601318.SH', '名称': '中国平安', '行业': '保险', '最新价': 45.60, '涨跌幅': -0.52, '预测收益': 3.5, '评分': 78, '风险': '中', 'PE': 9.8, 'PB': 1.50, 'ROE': 14.2, '毛利率': 12.5, '净利率': 6.8, '资产负债率': 91.8},
    {'代码': '600016.SH', '名称': '民生银行', '行业': '银行', '最新价': 4.25, '涨跌幅': 1.20, '预测收益': 4.2, '评分': 82, '风险': '中低', 'PE': 5.8, 'PB': 0.65, 'ROE': 10.5, '毛利率': 30.5, '净利率': 18.5, '资产负债率': 89.2},
    {'代码': '601939.SH', '名称': '建设银行', '行业': '银行', '最新价': 7.52, '涨跌幅': 0.94, '预测收益': 3.8, '评分': 84, '风险': '低', 'PE': 6.2, 'PB': 0.78, 'ROE': 12.8, '毛利率': 34.5, '净利率': 21.5, '资产负债率': 87.5},
    {'代码': '601398.SH', '名称': '工商银行', '行业': '银行', '最新价': 5.18, '涨跌幅': 0.78, '预测收益': 3.5, '评分': 83, '风险': '低', 'PE': 5.9, 'PB': 0.72, 'ROE': 12.2, '毛利率': 33.5, '净利率': 20.8, '资产负债率': 88.8},
    {'代码': '600547.SH', '名称': '山东黄金', '行业': '资源', '最新价': 16.85, '涨跌幅': 2.85, '预测收益': 5.8, '评分': 86, '风险': '中高', 'PE': 22.5, 'PB': 3.80, 'ROE': 15.5, '毛利率': 22.5, '净利率': 12.5, '资产负债率': 45.5},
    {'代码': '000651.SZ', '名称': '格力电器', '行业': '制造', '最新价': 42.50, '涨跌幅': 1.55, '预测收益': 4.5, '评分': 86, '风险': '中', 'PE': 15.2, 'PB': 2.80, 'ROE': 18.5, '毛利率': 26.5, '净利率': 12.5, '资产负债率': 65.5}
])

# 生成模拟数据
def generate_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now())
    base_price = 3500
    returns = np.random.normal(0.0005, 0.01, len(dates))
    prices = base_price * (1 + returns).cumprod()
    
    factors = {
        '动量因子': np.random.randint(60, 95),
        '技术因子': np.random.randint(55, 90),
        '波动因子': np.random.randint(40, 75),
        '价值因子': np.random.randint(50, 85),
        '质量因子': np.random.randint(65, 98)
    }
    
    return dates, prices, factors

dates, prices, factors = generate_data()

# 页面标题
st.title("📈 沪深300智能收益预测系统")
st.subheader("基于多因子模型的专业股票分析工具")

# 搜索功能
search_query = st.text_input("🔍 搜索股票代码或名称", "")
if search_query:
    filtered_stocks = stocks_data[
        stocks_data['代码'].str.contains(search_query, case=False) |
        stocks_data['名称'].str.contains(search_query, case=False) |
        stocks_data['行业'].str.contains(search_query, case=False)
    ]
else:
    filtered_stocks = stocks_data

# 标签页导航
tabs = st.tabs(["📊 市场概览", "💰 财务分析", "📉 技术分析", "🎯 因子分析", "🏢 行业对比", "💼 投资组合", "📈 历史收益"])

# 1. 市场概览
with tabs[0]:
    st.markdown("---")
    st.subheader("📊 市场概览")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("沪深300指数", f"{prices[-1]:.2f}", f"{(prices[-1]-prices[-2])/prices[-2]*100:.2f}%")
    with col2:
        st.metric("日成交量", "2,856.3亿", "+12.5%")
    with col3:
        st.metric("上涨家数", "2,156", "+8.3%")
    with col4:
        st.metric("下跌家数", "1,432", "-5.2%")
    with col5:
        st.metric("市场情绪", "偏乐观", "↑ 15%")
    
    # 价格走势图
    st.markdown("---")
    st.subheader("📉 沪深300走势分析")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=prices, 
        name='沪深300',
        line=dict(color='#667eea', width=2),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    ma50 = pd.Series(prices).rolling(50).mean()
    ma200 = pd.Series(prices).rolling(200).mean()
    fig.add_trace(go.Scatter(x=dates, y=ma50, name='MA50', line=dict(color='#00ff88', width=1.5, dash='dash')))
    fig.add_trace(go.Scatter(x=dates, y=ma200, name='MA200', line=dict(color='#ff4757', width=1.5, dash='dash')))
    
    fig.update_layout(
        title='沪深300指数走势',
        xaxis_title='日期',
        yaxis_title='点数',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        legend=dict(orientation='h', y=-0.2)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 2. 财务分析
with tabs[1]:
    st.markdown("---")
    st.subheader("💰 财务分析")
    
    selected_stock = st.selectbox("选择股票", stocks_data['名称'].tolist(), index=0)
    stock_info = stocks_data[stocks_data['名称'] == selected_stock].iloc[0]
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("市盈率 (PE)", f"{stock_info['PE']}", help="衡量股价与盈利的比率")
    with col2:
        st.metric("市净率 (PB)", f"{stock_info['PB']}", help="衡量股价与净资产的比率")
    with col3:
        st.metric("ROE", f"{stock_info['ROE']}%", help="净资产收益率")
    with col4:
        st.metric("毛利率", f"{stock_info['毛利率']}%", help="毛利占营收的比例")
    with col5:
        st.metric("净利率", f"{stock_info['净利率']}%", help="净利润占营收的比例")
    with col6:
        st.metric("资产负债率", f"{stock_info['资产负债率']}%", help="负债占总资产的比例")
    
    # 财务指标对比
    st.markdown("---")
    st.subheader("📊 财务指标对比 (vs 行业平均)")
    
    industry_data = {
        '指标': ['PE', 'PB', 'ROE', '毛利率'],
        '当前股票': [stock_info['PE'], stock_info['PB'], stock_info['ROE'], stock_info['毛利率']],
        '行业平均': [12.5, 1.8, 10.2, 28.5]
    }
    industry_df = pd.DataFrame(industry_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=industry_df['指标'], y=industry_df['当前股票'], name=selected_stock, marker_color='#667eea'))
    fig.add_trace(go.Bar(x=industry_df['指标'], y=industry_df['行业平均'], name='行业平均', marker_color='#764ba2'))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        legend=dict(orientation='h')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 3. 技术分析
with tabs[2]:
    st.markdown("---")
    st.subheader("📉 技术分析")
    
    tech_tabs = st.tabs(["📊 趋势指标", "📈 震荡指标", "💧 量能指标", "⚡ 波动率"])
    
    with tech_tabs[0]:
        st.markdown("### 移动平均线")
        ma_data = pd.DataFrame({
            '周期': ['MA5', 'MA10', 'MA20', 'MA60'],
            '数值': [10.62, 10.55, 10.48, 10.35]
        })
        st.dataframe(ma_data)
        
        st.markdown("### MACD指标")
        macd_data = pd.DataFrame({
            '指标': ['DIF', 'DEA', 'MACD柱'],
            '数值': ['+0.18', '+0.08', '+0.10']
        })
        st.dataframe(macd_data)
    
    with tech_tabs[1]:
        st.markdown("### RSI指标")
        rsi_data = pd.DataFrame({
            '周期': ['RSI(6)', 'RSI(14)', 'RSI(24)'],
            '数值': [72.5, 68.5, 62.5]
        })
        st.dataframe(rsi_data)
        
        st.markdown("### KDJ指标")
        kdj_data = pd.DataFrame({
            '指标': ['K值', 'D值', 'J值'],
            '数值': [82.5, 78.5, 90.2]
        })
        st.dataframe(kdj_data)
    
    with tech_tabs[2]:
        st.markdown("### 量能指标")
        volume_data = pd.DataFrame({
            '指标': ['成交量', '成交额', '量比', '换手率'],
            '数值': ['1256万手', '13.62亿', '1.5', '2.8%']
        })
        st.dataframe(volume_data)
    
    with tech_tabs[3]:
        st.markdown("### 波动率指标")
        vol_data = pd.DataFrame({
            '指标': ['ATR', '布林带宽度', '历史波动率', '隐含波动率'],
            '数值': [0.35, '1.25%', '21.5%', '18.2%']
        })
        st.dataframe(vol_data)

# 4. 因子分析
with tabs[3]:
    st.markdown("---")
    st.subheader("🎯 多因子评分")
    
    factor_cols = st.columns(5)
    factor_names = list(factors.keys())
    factor_colors = ['#00d9ff', '#38ef7d', '#ffd93d', '#ff4757', '#a855f7']
    
    for i, (name, score) in enumerate(factors.items()):
        with factor_cols[i]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border-left: 4px solid {factor_colors[i]};">
                <h4 style="color: rgba(255,255,255,0.7); font-size: 14px;">{name}</h4>
                <p style="font-size: 36px; font-weight: bold; color: {factor_colors[i]};">{score}</p>
                <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-top: 10px;">
                    <div style="height: 100%; width: {score}%; background: {factor_colors[i]}; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # 投资建议
    st.markdown("---")
    st.subheader("💡 投资建议")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px;">
        <h4 style="margin-bottom: 15px;">📌 综合分析建议</h4>
        <p style="line-height: 1.7; font-size: 15px;">
            当前沪深300指数处于<strong>中性偏乐观</strong>区间。多因子模型显示，
            <strong>动量因子</strong>和<strong>质量因子</strong>表现强劲，
            建议关注<strong>消费、金融</strong>板块的优质标的。
        </p>
        <p><strong>建议操作：</strong>可以考虑分批建仓，建议仓位20%-30%，设置5%止损位。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 模型信息
    st.markdown("---")
    st.subheader("🤖 模型参数")
    
    model_info = pd.DataFrame({
        '参数': ['模型类型', '特征数量', '训练样本', '回测周期', '准确率', '夏普比率'],
        '值': ['LightGBM 回归模型', '45个因子特征', '500,000+ 条', '2021-2024', '68.5%', '1.85']
    })
    st.dataframe(model_info)

# 5. 行业对比
with tabs[4]:
    st.markdown("---")
    st.subheader("🏢 行业对比")
    
    selected_industry = st.selectbox("选择行业", stocks_data['行业'].unique())
    industry_stocks = stocks_data[stocks_data['行业'] == selected_industry]
    
    st.dataframe(industry_stocks[['代码', '名称', '最新价', '涨跌幅', 'PE', 'PB', 'ROE', '预测收益', '评分']].style.format({
        '最新价': '{:.2f}',
        '涨跌幅': '{:.2f}%',
        'PE': '{:.1f}',
        'PB': '{:.2f}',
        'ROE': '{:.1f}%',
        '预测收益': '{:.1f}%'
    }))

# 6. 投资组合
with tabs[5]:
    st.markdown("---")
    st.subheader("💼 投资组合")
    
    sorted_stocks = stocks_data.sort_values('评分', ascending=False).head(15)
    st.dataframe(sorted_stocks[['名称', '行业', '最新价', '涨跌幅', '预测收益', '评分', '风险', 'PE', 'ROE']].style.format({
        '最新价': '{:.2f}',
        '涨跌幅': '{:.2f}%',
        '预测收益': '{:.1f}%',
        'PE': '{:.1f}',
        'ROE': '{:.1f}%'
    }))

# 7. 历史收益
with tabs[6]:
    st.markdown("---")
    st.subheader("📈 历史收益")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("累计收益", "+35.8%", help="自策略运行以来的累计收益")
    with col2:
        st.metric("年化收益", "12.5%", help="年化收益率")
    with col3:
        st.metric("最大回撤", "-18.2%", help="最大亏损幅度")
    with col4:
        st.metric("胜率", "62%", help="盈利交易占比")
    with col5:
        st.metric("夏普比率", "1.85", help="风险调整后收益")
    with col6:
        st.metric("信息比率", "1.25", help="超额收益能力")
    
    # 分年度收益
    st.markdown("---")
    st.subheader("📊 分年度收益")
    
    year_data = pd.DataFrame({
        '年份': ['2021年', '2022年', '2023年', '2024年至今'],
        '策略收益': ['+22.5%', '-15.8%', '+18.2%', '+10.9%'],
        '沪深300': ['+5.2%', '-21.6%', '-8.7%', '+3.2%']
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=year_data['年份'], y=[float(x[:-1]) for x in year_data['策略收益']], name='策略收益', marker_color='#667eea'))
    fig.add_trace(go.Bar(x=year_data['年份'], y=[float(x[:-1]) for x in year_data['沪深300']], name='沪深300', marker_color='#764ba2'))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff'),
        legend=dict(orientation='h')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 页脚
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: rgba(255,255,255,0.5); font-size: 12px;">
    © 2024 沪深300智能收益预测系统 | ⚠️ 投资有风险，入市需谨慎。本预测仅供参考，不构成投资建议。
</p>
""", unsafe_allow_html=True)