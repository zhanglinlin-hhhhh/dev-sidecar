import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config


st.title("Test graph")

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

# 图像上传功能
def image_upload_for_experts():
    images = {}
    for expert in json_data.keys():
        image = st.file_uploader(f"上传 {expert} 的图像", type=["png", "jpg", "jpeg"], key=expert)
        if image is not None:
            images[expert] = image
    return images

# 转换 JSON 为图
def json2graph(json_data, topic, images, **kwargs):
    nodes = []
    edges = []
    
    nodes.append(Node(id="Topic", label=topic, size=25, shape="dot"))
    
    # 为每个专家节点添加图像
    for expert, value in json_data.items():
        if expert in images:  # 如果该专家有上传图像
            img = images[expert]
            nodes.append(Node(id=expert, label=expert, size=15, shape="image", image=img))
        else:  # 如果没有图像，则使用默认圆圈
            nodes.append(Node(id=expert, label=expert, size=15, shape="dot"))
        
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
