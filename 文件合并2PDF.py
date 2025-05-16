import os
from PIL import Image
import argparse # 导入 argparse
import sys # 导入 sys

# 创建参数解析器
parser = argparse.ArgumentParser(description="将图片序列合并到PDF文件。")
parser.add_argument("--input_dir", required=True, help="包含图片文件的输入目录")
parser.add_argument("--output_pdf", required=True, help="输出的PDF文件路径")
args = parser.parse_args()

# 从命令行参数获取图片目录和输出路径
img_dir = args.input_dir
output_pdf = args.output_pdf

# 检查输入目录是否存在
if not os.path.isdir(img_dir):
    print(f"错误: 输入目录 '{img_dir}' 不存在。", file=sys.stderr)
    sys.exit(1) # 使用非零退出码表示失败

# 获取所有图片文件，按文件名排序
# 仅处理 .png, .jpg, .jpeg 文件
img_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and os.path.isfile(os.path.join(img_dir, f))])

if not img_files:
    print(f"警告: 在目录 '{img_dir}' 中未找到任何图片文件 (.png, .jpg, .jpeg)。", file=sys.stderr)
    sys.exit(0) # 没有文件，但不是错误

# 确保输出目录存在
output_dir = os.path.dirname(output_pdf)
if output_dir and not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
        print(f"信息: 已创建输出目录 '{output_dir}'")
    except OSError as e:
        print(f"错误: 无法创建输出目录 '{output_dir}': {e}", file=sys.stderr)
        sys.exit(1)

print(f"信息: 在目录 '{img_dir}' 中找到 {len(img_files)} 个图片文件。")
print(f"信息: 尝试合并到 PDF 文件: {output_pdf}")

try:
    # 打开所有图片并转换为 RGB 模式（确保兼容 PDF）
    # 使用上下文管理器 with 确保文件正确关闭
    imgs = []
    for f in img_files:
        img_path = os.path.join(img_dir, f)
        try:
            img = Image.open(img_path).convert('RGB')
            imgs.append(img)
        except Exception as img_err:
            print(f"警告: 无法打开或处理图片文件 '{f}': {img_err}", file=sys.stderr)
            # 可以选择跳过此文件，或根据需求退出

    if not imgs:
        print("错误: 没有成功加载任何图片文件，无法生成PDF。", file=sys.stderr)
        sys.exit(1)


    # 保存为PDF
    # 将第一张图片保存为主体，后续图片追加
    imgs[0].save(output_pdf, save_all=True, append_images=imgs[1:])
    print(f"成功: 图片已合并并生成PDF文件: {output_pdf}")
    sys.exit(0) # 正常退出

except Exception as e:
    print(f"错误: 生成PDF过程中发生意外错误: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr) # 打印详细错误信息
    sys.exit(1) # 表示失败
