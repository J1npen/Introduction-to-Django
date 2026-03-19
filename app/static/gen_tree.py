import os

IGNORE_DIRS = {"venv", "__pycache__", ".git"}

def generate_tree(path=".", depth=2, prefix=""):
    if depth < 0:
        return ""

    entries = []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return ""

    tree_str = ""

    for i, entry in enumerate(entries):
        if entry in IGNORE_DIRS:
            continue

        full_path = os.path.join(path, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "

        tree_str += prefix + connector + entry + "\n"

        if os.path.isdir(full_path):
            extension = "    " if i == len(entries) - 1 else "│   "
            tree_str += generate_tree(full_path, depth - 1, prefix + extension)

    return tree_str


def save_tree_to_file(tree_text, output_file="project_tree.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tree_text)
    print(f"[OK] 项目结构已生成：{output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="自动生成项目结构树")
    parser.add_argument("-p", "--path", default=".", help="项目目录（默认当前目录）")
    parser.add_argument("-d", "--depth", type=int, default=5, help="显示层级（默认 5）")
    parser.add_argument("-o", "--output", default=None, help="输出文件（默认不写入文件）")

    args = parser.parse_args()

    tree = generate_tree(args.path, args.depth)
    print(tree)

    if args.output:
        save_tree_to_file(tree, args.output)
