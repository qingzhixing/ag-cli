#!/usr/bin/env python3
"""
ag-cli 安装脚本 - 简化的跨平台安装方法
"""

import os
import sys
import platform
import subprocess


def main():
    print("🚀 正在安装 ag-cli 项目...")
    print(f"📋 操作系统: {platform.system()} {platform.release()}")
    print(f"🐍 Python版本: {platform.python_version()}")
    print()

    # 检查是否安装了PDM
    try:
        result = subprocess.run(["pdm", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 错误: 未安装PDM，请先安装PDM")
            print("💡 安装命令: pip install pdm")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ 错误: 未安装PDM，请先安装PDM")
        print("💡 安装命令: pip install pdm")
        sys.exit(1)

    # 安装依赖
    print("📦 正在安装依赖...")
    result = subprocess.run(["pdm", "install"])
    if result.returncode != 0:
        print("❌ 依赖安装失败！")
        sys.exit(1)

    # 构建包
    print("🔨 正在构建包...")

    # 清理之前的构建
    if os.path.exists("dist"):
        import shutil

        shutil.rmtree("dist")

    result = subprocess.run(["pdm", "build"])
    if result.returncode != 0:
        print("❌ 构建失败！")
        sys.exit(1)

    # 安装到当前环境
    print("⚡ 正在安装到当前环境...")
    result = subprocess.run(["pdm", "install", "--no-self"])
    if result.returncode != 0:
        print("❌ 安装失败！")
        sys.exit(1)

    print("\n✅ 安装完成！")
    print("🎉 现在你可以使用 'ag' 命令了")
    print("\n📖 使用示例:")
    print('  ag "你好"')
    print("  ag --help")
    print("  ag --list-models")
    print("  ag --continue")

    # 显示包文件信息
    if os.path.exists("dist"):
        print("\n📁 构建的包文件:")
        for file in os.listdir("dist"):
            print(f"  📄 {file}")

    print("\n💡 提示: 使用 'pdm run --list' 查看所有可用命令")


if __name__ == "__main__":
    main()
