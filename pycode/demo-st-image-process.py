import streamlit as st
import numpy as np
from PIL import Image
from skimage import exposure, img_as_float, img_as_ubyte


def gamma_correction(rgb_image, gamma):
    img_array = np.array(rgb_image) # 转换为 numpy 数组
    img_float = img_as_float(img_array) # 转换为 float [0, 1] 范围 
    img_adjusted = exposure.adjust_gamma(img_float, gamma=gamma) # Gamma 校正
    img_ubyte = img_as_ubyte(img_adjusted) # 转回 uint8 [0, 255] 范围
    return Image.fromarray(img_ubyte)

st.set_page_config(page_title="图像处理", layout="wide")
st.title("🖼️ Gamma 对比度校正")

with st.sidebar:
    uploaded_file = st.file_uploader("选择一张图片上传", type=["jpg", "jpeg", "png"],
                                    help="支持 JPG, JPEG, PNG格式")

if uploaded_file is None: # 未上传图片时的提示   
    st.info("请先在侧边栏上传一张图片")
else:   
    image = Image.open(uploaded_file) # 使用 PIL 读取图片
    st.success(f"原始图像信息：宽度 {image.width} px，高度 {image.height} px，颜色模式 {image.mode}")
    (width, height) = (image.width // 4, image.height // 4)
    image = image.resize((width, height))
    if image.mode != 'RGB': # 转换为RGB，以确保格式统一
        image = image.convert('RGB')
      
    st.subheader("🎛️ 调整参数")
    gamma = st.slider("Gamma 值",min_value=0.1,max_value=3.0,value=1.0,step=0.05)   

    adjusted_image = gamma_correction(image, gamma)
    
    # 并排显示原图与调整后的图像
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"原图 (γ = 1.0)")
        st.image(image)
    
    with col2:
        st.info(f"调整后 (γ = {gamma:.2f})")
        st.image(adjusted_image)
    
