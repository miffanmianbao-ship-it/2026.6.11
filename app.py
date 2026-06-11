import streamlit as st
from ultralytics import YOLO
from PIL import Image

# 1. 设置网页标题和说明
st.set_page_config(page_title="裂缝检测 AI", page_icon="🧱")
st.title("🧱 智能混凝土裂缝检测系统")
st.write("欢迎使用！请上传一张墙壁、桥面或路面的照片，AI 将自动为您检测是否存在裂缝。")

# 2. 加载 AI 模型 (加上缓存，避免每次上传图片都重新加载模型)
@st.cache_resource
def load_model():
    # 读取和 app.py 放在同一个文件夹下的 best.pt
    return YOLO('best.pt')

model = load_model()

# 3. 创建图片上传组件
uploaded_file = st.file_uploader("请选择一张图片上传...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 4. 在网页上显示用户上传的图片
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的原始图片', use_container_width=True)

    st.write("🧠 AI 正在进行显微镜级别的观察...")

    # 5. 让 AI 进行预测
    results = model(image)

    # 6. 解析预测结果
    names_dict = results[0].names  # 获取类别字典
    probs = results[0].probs.data.tolist()  # 获取各个类别的概率
    
    # 找到概率最大的类别
    max_index = probs.index(max(probs))
    predicted_class = names_dict[max_index]
    confidence = probs[max_index]

    # 7. 美化输出结果
    st.markdown("---")
    if predicted_class == "Cracked":
        st.error(f"⚠️ **检测结果：存在裂缝！**")
        st.write(f"AI 确信度: **{confidence*100:.2f}%**")
        st.warning("建议：请及时安排专业人员进行实地安全评估。")
    else:
        st.success(f"✅ **检测结果：完好无损 (未发现明显裂缝)。**")
        st.write(f"AI 确信度: **{confidence*100:.2f}%**")