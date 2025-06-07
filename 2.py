import streamlit as st

st.title("Streamlit Sidebar Test")

# 侧边栏控件：选择箭头形状
arrow_shape = st.sidebar.selectbox("选择箭头形状", ["arrow", "triangle", "circle"], index=0)

# 侧边栏控件：选择箭头颜色
arrow_color = st.sidebar.color_picker("选择箭头颜色", "#0000FF")

# 侧边栏控件：选择节点颜色
node_color = st.sidebar.color_picker("选择节点颜色", "#FF6347")

# 侧边栏控件：选择字体大小
font_size = st.sidebar.slider("选择字体大小", min_value=10, max_value=30, value=15)

# 显示选择结果
st.write(f"箭头形状: {arrow_shape}")
st.write(f"箭头颜色: {arrow_color}")
st.write(f"节点颜色: {node_color}")
st.write(f"字体大小: {font_size}")

