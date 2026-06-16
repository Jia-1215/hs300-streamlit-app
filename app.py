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
</style>
""", unsafe_allow_html=True)

# 模拟数据
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
    
    stock_data = pd.DataFrame({
        '代码': ['000001', '000002', '600000', '600519', '000858'],
        '名称': ['平安银行', '万科A', '浦发银行', '贵州茅台', '五粮液'],
        '最新价': [12.58, 15.32, 8.95, 1685.00, 145.60],
        '涨跌幅': [2.35, -1.20, 0.85, 3.20, -0.55],
        '预测评分': [85, 72, 68, 92, 88],
        '目标价': [14.20, 16.80, 9.80, 1850.00, 165.00]
    })
    
    return dates, prices, factors, stock_data

dates, prices, factors, stock_data = generate_data()

# 页面标题
st.title("📈 沪深300智能收益预测系统")
st.subheader("基于多因子模型的专业股票分析工具")

# 主要指标卡片
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

# 添加均线
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

# 多因子分析
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

# 成分股分析
st.markdown("---")
st.subheader("📋 成分股精选")

st.dataframe(stock_data.style.format({
    '最新价': '{:.2f}',
    '涨跌幅': '{:.2f}%',
    '目标价': '{:.2f}'
}).applymap(lambda x: f'color: #00ff88' if isinstance(x, float) and x > 0 else ('color: #ff4757' if isinstance(x, float) and x < 0 else 'color: #fff'), subset=['涨跌幅']))

# 风险评估
st.markdown("---")
st.subheader("⚠️ 风险评估")

risk_score = np.random.randint(40, 70)
risk_level = "中等" if 40 <= risk_score < 70 else "低" if risk_score < 40 else "高"
risk_color = "#ffd93d" if 40 <= risk_score < 70 else "#00ff88" if risk_score < 40 else "#ff4757"

st.markdown(f"""
<div style="background: rgba(255,255,255,0.03); padding: 25px; border-radius: 12px;">
    <h4 style="color: #667eea; margin-bottom: 15px;">综合风险指数</h4>
    <div style="display: flex; align-items: center; gap: 20px;">
        <div style="flex: 1;">
            <div style="height: 12px; background: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden;">
                <div style="height: 100%; width: {risk_score}%; background: linear-gradient(90deg, {risk_color}, {'#f39c12' if risk_level == '中等' else '#38ef7d' if risk_level == '低' else '#eb3349'}); border-radius: 6px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: rgba(255,255,255,0.5);">
                <span>低风险</span>
                <span>中等风险</span>
                <span>高风险</span>
            </div>
        </div>
        <div style="text-align: right;">
            <p style="font-size: 48px; font-weight: bold; color: {risk_color};">{risk_score}</p>
            <p style="color: rgba(255,255,255,0.7);">风险等级: {risk_level}</p>
        </div>
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
    <div style="display: flex; gap: 15px; margin-top: 20px;">
        <button style="padding: 12px 30px; background: #00ff88; color: #1a1a2e; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">
            📊 查看详细报告
        </button>
        <button style="padding: 12px 30px; background: rgba(255,255,255,0.2); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">
            🔔 设置提醒
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: rgba(255,255,255,0.5); font-size: 12px;">
    © 2024 沪深300智能收益预测系统 | 数据仅供参考，不构成投资建议
</p>
""", unsafe_allow_html=True)