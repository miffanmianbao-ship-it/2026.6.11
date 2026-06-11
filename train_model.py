from ultralytics import YOLO

if __name__ == '__main__':
    print("========================================")
    print("🚀 正在初始化 YOLOv8 裂缝检测模型...")
    print("========================================")

    # 1. 加载预训练模型
    # 我们使用 yolov8n-cls.pt (n代表 Nano，是最轻量、速度最快的版本，非常适合新手和网页部署)
    # 第一次运行时，代码会自动从网上下载这个只有几 MB 的基础模型
    model = YOLO('yolov8n-cls.pt')

    # 2. 告诉模型你的数据在哪里
    # 这里直接使用你整理好的完美数据集路径
    DATA_DIR = r"D:\课内学习的地方\大二\大二下学期\AI赋能\作业部分\data"

    # 3. 正式开始训练！
    results = model.train(
        data=DATA_DIR,      # 数据集路径
        epochs=10,          # 训练轮数 (让模型把所有图片反复学习 10 遍)
        imgsz=224,          # 图片缩放尺寸 (分类任务的经典尺寸)
        device=0,           # 明确指定使用你的第 0 号显卡 (RTX 4050)
        workers=4,          # 开启 4 个线程帮你搬运图片，加速训练
        project='Crack_Detection', # 训练结果保存的主文件夹名
        name='v1_training'  # 这一次训练的专属名字
    )

    print("\n🎉 训练圆满结束！你的 AI 已经学会看裂缝了！")