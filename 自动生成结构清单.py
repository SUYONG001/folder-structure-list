import os
import sys
from pathlib import Path

# ==================== 核心全自动配置区域 ====================
# 【动态识别机制】自动获取当前运行脚本所在的绝对路径，彻底告别手动改路径
TARGET_DIR = Path(__file__).resolve().parent

# 【智能动态命名机制】自动捕获当前文件夹名称，生成唯一的专属清单文件名
# 彻底解决千篇一律和重名覆盖问题。例如：丢进「KEY」，就会生成「KEY_结构清单.txt」
OUTPUT_FILE = f"{TARGET_DIR.name}_结构清单.txt"

# 最大扫描深度：默认 3 层。如果需要更深，可以自行调大
MAX_DEPTH = 100                        

# 【视觉装订线配置区】在此处一键切换您最喜欢的首尾识别线样式
# 样式 1（原版经典型）："========================================="
# 样式 2（现代硬核型）："=================================================="
# 样式 3（技术文档型）："─────────────────────────────────────────────────────────────"
BORDER_STYLE = "========================================="
# ============================================================

def get_dir_size(path):
    """深度递归计算整个文件夹的真实总容量"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except PermissionError:
        pass
    return total

def format_size(bytes_size):
    """将字节智能转换为最直观的 KB/MB/GB/TB 单位"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def generate_perfect_size_tree(dir_path, prefix="", depth=0):
    if depth > MAX_DEPTH:
        return []
    
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return []
        
    try:
        # 【全动态防污染机制】除了系统垃圾，还要动态屏蔽“脚本自身”和“本次动态生成的专属txt”
        # 确保不论文件名怎么变，资产树都能100%纯净隐身
        ignored_names = {
            'thumbs.db', 'desktop.ini', '.git', '.ds_store', '$recycle.bin',
            Path(__file__).name.lower(), OUTPUT_FILE.lower()
        }
        items = [
            p for p in dir_path.iterdir() 
            if p.name.lower() not in ignored_names and not p.name.startswith('.')
        ]
        # 智能排序：文件夹在上，文件在下
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return []

    lines = []
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└─ " if is_last else "├─ "
        
        if item.is_file():
            size_str = format_size(item.stat().st_size)
        else:
            size_str = format_size(get_dir_size(item))
            
        lines.append(f"{prefix}{connector}{item.name} ({size_str})")
        
        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(generate_perfect_size_tree(item, next_prefix, depth + 1))
            
    return lines

if __name__ == "__main__":
    print(f"==================================================")
    print(f"▶ 动态路径识别成功！当前目标根目录为:\n  {TARGET_DIR}")
    print(f"▶ 专属清单文件名已绑定:\n  {OUTPUT_FILE}")
    print(f"==================================================")
    print(f"正在进行全量体积审计与目录树构建，请稍候...")
    
    tree_content = generate_perfect_size_tree(TARGET_DIR)
    root_size = format_size(get_dir_size(TARGET_DIR))
    
    # 将输出文件绝对对齐到脚本同级路径
    output_path = TARGET_DIR / OUTPUT_FILE
    
    with open(output_path, "w", encoding="utf-8") as f:
        # 1. 写入页眉装订线
        f.write(f"{BORDER_STYLE}\n")
        
        # 2. 写入根目录名称与全盘总大小
        f.write(f"{TARGET_DIR.name}/ ({root_size})\n")
        
        # 3. 写入内部子项树形骨架
        if tree_content:
            f.write("\n".join(tree_content) + "\n")
            
        # 4. 写入页脚装订线
        f.write(f"{BORDER_STYLE}\n")
        
    print(f"\n[OK] 审计完毕！专属命名且带装订线的清单已无痕生成。")
    print(f"▶ 存储路径: {output_path}")
    print(f"==================================================")