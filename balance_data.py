import os
import random
import shutil

def create_balanced_and_split_dataset(source_dir, target_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    assert train_ratio + val_ratio + test_ratio == 1.0, "比例总和必须为 1.0"

    categories = ["Cracked", "Non-cracked"]
    scenes = ["Decks", "Pavements", "Walls"]

    # 第一步：去各个子文件夹里收集所有图片的路径
    raw_data = {cat: [] for cat in categories}
    
    print("1. 开始扫描原始数据集...")
    for cat in categories:
        for scene in scenes:
            scene_cat_dir = os.path.join(source_dir, scene, cat)
            if os.path.exists(scene_cat_dir):
                images = [img for img in os.listdir(scene_cat_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
                for img in images:
                    src_path = os.path.join(scene_cat_dir, img)
                    new_name = f"{scene}_{img}" # 加上前缀防止同名覆盖
                    raw_data[cat].append((src_path, new_name))

    print(f"   - 扫描到有裂缝 (Cracked) 图片: {len(raw_data['Cracked'])} 张")
    print(f"   - 扫描到无裂缝 (Non-cracked) 图片: {len(raw_data['Non-cracked'])} 张")

    # 第二步：数量平衡（欠采样）
    min_count = min(len(raw_data['Cracked']), len(raw_data['Non-cracked']))
    print(f"\n2. 正在进行平衡处理：两种类别将各随机抽取 {min_count} 张图片...")
    
    balanced_data = {}
    for cat in categories:
        random.shuffle(raw_data[cat]) # 随机打乱
        balanced_data[cat] = raw_data[cat][:min_count] # 只取少的那一方的数量

    # 第三步：创建全新的目标文件夹结构
    print("\n3. 正在创建 data 文件夹结构...")
    for split in ['train', 'val', 'test']:
        for cat in categories:
            os.makedirs(os.path.join(target_dir, split, cat), exist_ok=True)

    # 第四步：划分并开始复制文件
    print("\n4. 开始切分并复制图片（5.6万张中筛选出的完美1:1数据集）...")
    for cat in categories:
        imgs = balanced_data[cat]
        total_imgs = len(imgs)
        
        # 计算切分点（这次修正了之前 val_point 的拼写错误）
        train_point = int(total_imgs * train_ratio)
        val_point = int(total_imgs * (train_ratio + val_ratio))

        splits = {
            'train': imgs[:train_point],
            'val': imgs[train_point:val_point],
            'test': imgs[val_point:]
        }

        for split_name, img_list in splits.items():
            dest_dir = os.path.join(target_dir, split_name, cat)
            print(f"   -> 正在复制 [{cat}] 到 [{split_name}集]，共 {len(img_list)} 张...")
            for src_path, new_name in img_list:
                shutil.copy2(src_path, os.path.join(dest_dir, new_name))

if __name__ == '__main__':
    # 依然是您电脑上的绝对路径
    SOURCE_DIRECTORY = r"D:\课内学习的地方\大二\大二下学期\AI赋能\作业部分\archive" 
    TARGET_DIRECTORY = r"D:\课内学习的地方\大二\大二下学期\AI赋能\作业部分\data"    
    
    print("================== 智能裂缝检测数据集处理系统 ==================")
    create_balanced_and_split_dataset(SOURCE_DIRECTORY, TARGET_DIRECTORY)
    print("\n🎉 🎉 🎉 完美数据集制作成功！")
    print(f"请前往目标路径查看结果: {TARGET_DIRECTORY}")