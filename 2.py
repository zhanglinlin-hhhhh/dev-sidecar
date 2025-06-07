import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import base64
from io import BytesIO


st.title("Interactive Graph Customization")

# 定义话题和专家数据
topic = "怎么解决三体问题"

json_data = {
    "专家1": {
        "1": "三体问题无法通过解析方法获得通用解，需依赖数值模拟方法",
        "2": "采用高精度数值积分算法（如Runge-Kutta或辛积分）进行轨迹模拟",
    },
    "专家2": {
        "1": "构建LLM驱动的Agent框架求解三体问题",
        "2": "通过强化学习优化初始条件以探索稳定轨道",
    },
    "专家3": {
        "1": "特殊条件下（如质量相等/二维平面）研究简化三体系统",
        "2": "使用符号计算和代数几何方法构造积分不变量",
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
def json2graph(json_data, topic, images):
    nodes = []
    edges = []
    
    nodes.append(Node(id="Topic", label=topic, size=25, shape="dot"))
    
    # 为每个专家节点添加图像
    for expert, value in json_data.items():
        if expert in images:  # 如果该专家有上传图像
            img_base64 = images[expert]
            nodes.append(Node(id=expert, label=expert, size=50, shape="image", image=f"data:image/png;base64,{img_base64}"))
        else:  # 如果没有图像，则使用默认圆圈
            nodes.append(Node(id=expert, label=expert, size=50, shape="dot"))
        
        for key2, value2 in value.items():
            nodes.append(Node(id=f"{expert}_{key2}", label=value2, size=5, shape="dot"))
            edges.append(Edge(source=f"{expert}_{key2}", label=" ", target=expert))
        
        edges.append(Edge(source=expert, label=" ", target="Topic"))
    
    config = Config(width=600, height=400, directed=True, physics=True, hierarchical=False)
    return nodes, edges, config

# 上传专家图像
images = image_upload_for_experts()

# 显示图表
with st.expander("See explanation"):
    nodes, edges, config = json2graph(json_data, topic, images)
    agraph(nodes=nodes, edges=edges, config=config)
