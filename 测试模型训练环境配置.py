import sys

print("=== 深度学习环境体检 ===")

# 1. 检查 PyTorch 和 显卡 (CUDA)
try:
    import torch
    print(f"✅ PyTorch 已安装 (版本: {torch.__version__})")
    
    if torch.cuda.is_available():
        print(f"✅ GPU 识别成功！")
        print(f"👉 当前使用的显卡是: {torch.cuda.get_device_name(0)}")
    else:
        print(f"❌ 警告：PyTorch 无法识别到 GPU！(这说明你安装的可能是纯 CPU 版本的 PyTorch，训练会极其缓慢)")
except ImportError:
    print("❌ 警告：未安装 PyTorch！")

print("-" * 20)

# 2. 检查 YOLO 核心库 ultralytics
try:
    import ultralytics
    print(f"✅ YOLO 库 (ultralytics) 已安装 (版本: {ultralytics.__version__})")
except ImportError:
    print("❌ 警告：未安装 ultralytics 库！")