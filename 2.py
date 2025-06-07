import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import networkx as nx
import tempfile


st.title("Interactive Graph Customization")

# 定义话题和专家数据
topic = "怎么解决三体问题"

json_data = {
    "专家1": {
        "1": "三体问题无法通过解析方法获得通用解，需依赖数值模拟方法",
        "2": "采用高精度数值积分算法（如Runge-Kutta或辛积分）进行轨迹模拟",
        "3": "超级计算机可对特定初始条件进行有限时间高精度模拟",
        "4": "初始条件微小变化可能导致结果巨大差异，需精确测量初始状态",
        "5": "特定场景（如层级三体系统）可通过摄动理论近似简化计算"
    },
    "专家2": {
        "1": "构建LLM驱动的Agent框架求解三体问题",
        "2": "通过强化学习优化初始条件以探索稳定轨道",
        "3": "利用生成式AI对数值模拟结果进行模式识别",
        "4": "整合实时观测数据动态调整模型参数",
        "5": "多Agent协作并行模拟快速筛选目标解"
    },
    "专家3": {
        "1": "特殊条件下（如质量相等/二维平面）研究简化三体系统",
        "2": "使用符号计算和代数几何方法构造积分不变量",
        "3": "解析解仅存在于极少数特殊情况（如拉格朗日点）",
        "4": "结合AI加速符号回归发现隐藏数学关系",
        "5": "通过数学简化为数值模拟提供理论指导"
    }
}

# 图像上传并转换为 Base64
def image_to_base64(image_file):
    img = BytesIO(image_file.read())
    return base64.b64encode(img.getvalue()).decode()

# 图像上传功能
def image_upload_for_experts():
    images = {}
    for expert in json_data.keys():
        image = st.sidebar.file_uploader(f"上传 {expert} 的图像", type=["png", "jpg", "jpeg"], key=expert)
        if image is not None:
            images[expert] = image_to_base64(image)
    return images

# 转换 JSON 为图
def json2graph(json_data, topic, images, arrow_shape, arrow_color, node_color, font_size, image_size, arrow_thickness, node_shape, node_border_color, node_border_thickness, layout_type, **kwargs):
    nodes = []
    edges = []
    
    nodes.append(Node(id="Topic", label=topic, size=font_size, color=node_color, shape="dot"))
    
    # 为每个专家节点添加图像
    for expert, value in json_data.items():
        if expert in images:  # 如果该专家有上传图像
            img_base64 = images[expert]
            nodes.append(Node(id=expert, label=expert, size=image_size, shape="image", image=f"data:image/png;base64,{img_base64}", borderColor=node_border_color, borderWidth=node_border_thickness))
        else:  # 如果没有图像，则使用默认圆圈
            nodes.append(Node(id=expert, label=expert, size=font_size, color=node_color, shape=node_shape, borderColor=node_border_color, borderWidth=node_border_thickness))
        
        for key2, value2 in value.items():
            nodes.append(Node(id=f"{expert}_{key2}", label=value2, size=5, shape="dot", color=node_color))
            edges.append(Edge(source=f"{expert}_{key2}", label=" ", target=expert, arrowShape=arrow_shape, color=arrow_color, width=arrow_thickness))
        
        edges.append(Edge(source=expert, label=" ", target="Topic", arrowShape=arrow_shape, color=arrow_color, width=arrow_thickness))
    
    config = Config(width=600, height=400, directed=True, physics=True, hierarchical=(layout_type == 'hierarchical'))
    return nodes, edges, config

# 侧边栏控件：用户可交互的图形属性调整
arrow_shape = st.sidebar.selectbox("选择箭头形状", ["arrow", "triangle", "circle"], index=0)
arrow_color = st.sidebar.color_picker("选择箭头颜色", "#0000FF")
node_color = st.sidebar.color_picker("选择节点颜色", "#FF6347")
font_size = st.sidebar.slider("选择字体大小", min_value=10, max_value=30, value=15)
image_size = st.sidebar.slider("选择图像大小", min_value=50, max_value=200, value=100)

# 新增的功能
arrow_thickness = st.sidebar.slider("选择箭头粗细", min_value=1, max_value=10, value=2)
node_shape = st.sidebar.selectbox("选择节点形状", ["dot", "square", "star", "triangle"], index=0)
node_border_color = st.sidebar.color_picker("选择节点边框颜色", "#000000")
node_border_thickness = st.sidebar.slider("选择节点边框粗细", min_value=1, max_value=10, value=2)

# 布局选择
layout_type = st.sidebar.selectbox("选择图形布局", ["Force Directed", "Hierarchical"], index=0)

# 上传专家图像
images = image_upload_for_experts()

# 显示图表
with st.expander("See explanation"):
    nodes, edges, config = json2graph(json_data, topic, images, arrow_shape, arrow_color, node_color, font_size, image_size, arrow_thickness, node_shape, node_border_color, node_border_thickness, layout_type)
    agraph(nodes=nodes, edges=edges, config=config)

# 保存图形并提供下载按钮
def save_graph_as_image():
    # 创建一个图形对象
    fig, ax = plt.subplots(figsize=(8, 8))
    G = nx.Graph()

    # 添加节点和边到图中
    for node in nodes:
        G.add_node(node.id, label=node.label)
    for edge in edges:
        G.add_edge(edge.source, edge.target, color=edge.color, width=edge.width)

    # 使用 networkx 绘制图形
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=[node.size for node in nodes], font_size=font_size, node_color=[node.color for node in nodes], edge_color=[edge.color for edge in edges], width=[edge.width for edge in edges], ax=ax)
    
    # 保存图形到临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(temp_file.name)
    return temp_file.name

# 下载按钮
image_file_path = save_graph_as_image()

with open(image_file_path, "rb") as f:
    st.download_button("下载图形", f, file_name="graph_image.png", mime="image/png")
