#!/usr/bin/env python3
"""
ag-cli 构建脚本
构建可执行文件并输出到.dist目录
用户需要手动复制到PATH目录
"""

import os
import sys
import platform
import subprocess
import shutil


def check_pdm():
    """检查PDM是否安装"""
    try:
        result = subprocess.run(["pdm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass

    print("❌ 未安装PDM，请先安装PDM")
    print("💡 安装命令: pip install pdm")
    return False


def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    result = subprocess.run(["pdm", "install"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 依赖安装失败: {result.stderr}")
        return False
    return True


def get_venv_executable_path():
    """获取虚拟环境中编译好的可执行文件路径"""
    system = platform.system()

    # 检查当前项目的虚拟环境
    project_venv_scripts = os.path.join(
        ".venv", "Scripts" if system == "Windows" else "bin"
    )
    ag_executable = os.path.join(
        project_venv_scripts, "ag.exe" if system == "Windows" else "ag"
    )

    if os.path.exists(ag_executable):
        return ag_executable

    return None


def create_dist_directory():
    """创建.dist目录"""
    dist_dir = ".dist"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir, exist_ok=True)
        print(f"📂 创建输出目录: {dist_dir}")
    return dist_dir


def copy_executable_to_dist():
    """复制可执行文件到.dist目录"""
    executable_path = get_venv_executable_path()

    if not executable_path:
        print("❌ 未找到编译好的可执行文件")
        print("💡 请先运行 'pdm install' 确保依赖已安装")
        return False

    if not os.path.exists(executable_path):
        print(f"❌ 可执行文件不存在: {executable_path}")
        return False

    # 创建.dist目录
    dist_dir = create_dist_directory()

    # 确定目标文件名
    system = platform.system()
    if system == "Windows":
        target_name = "ag.exe"
    else:
        target_name = "ag"

    target_path = os.path.join(dist_dir, target_name)

    try:
        # 复制文件
        shutil.copy2(executable_path, target_path)
        print(f"✅ 复制可执行文件: {executable_path} -> {target_path}")
        return True
    except Exception as e:
        print(f"❌ 复制文件失败: {e}")
        return False


def get_system_path_dirs():
    """获取系统PATH环境变量中的所有目录"""
    path_env = os.environ.get("PATH", "")
    path_dirs = []

    for path_dir in path_env.split(os.pathsep):
        if path_dir.strip() and os.path.isdir(path_dir.strip()):
            path_dirs.append(path_dir.strip())

    return path_dirs


def get_recommended_path_dirs():
    """获取推荐的PATH目录"""
    system = platform.system()
    recommended_dirs = []

    if system == "Windows":
        recommended_dirs = [
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""),
                "Programs",
                "Python",
                "Python314",
                "Scripts",
            ),
            os.path.join(
                os.environ.get("APPDATA", ""), "Python", "Python314", "Scripts"
            ),
            os.path.join(
                os.environ.get("PROGRAMFILES", ""), "Python", "Python314", "Scripts"
            ),
            "C:\\Windows\\System32",
        ]
    elif system == "Linux":
        recommended_dirs = ["/usr/local/bin", "/usr/bin", "/bin", "~/.local/bin"]
    elif system == "Darwin":  # macOS
        recommended_dirs = ["/usr/local/bin", "/opt/local/bin", "/usr/bin", "~/bin"]

    # 过滤出实际存在的目录
    existing_dirs = []
    for dir_path in recommended_dirs:
        expanded_dir = os.path.expanduser(dir_path)
        if os.path.exists(expanded_dir):
            existing_dirs.append(expanded_dir)

    return existing_dirs


def main():
    """主函数 - 构建可执行文件"""
    print("🚀 ag-cli 构建脚本")
    print("=" * 60)
    print(f"📋 操作系统: {platform.system()} {platform.release()}")
    print(f"🐍 Python版本: {platform.python_version()}")
    print()

    # 检查PDM
    if not check_pdm():
        sys.exit(1)

    # 安装依赖
    if not install_dependencies():
        sys.exit(1)

    # 查找可执行文件
    executable_path = get_venv_executable_path()
    if executable_path:
        print(f"🔍 找到可执行文件: {executable_path}")
    else:
        print("❌ 未找到编译好的可执行文件")
        print("💡 请先运行 'pdm install' 确保依赖已安装")
        sys.exit(1)

    # 复制可执行文件到.dist目录
    print("\n📝 复制可执行文件到.dist目录...")
    if not copy_executable_to_dist():
        print("❌ 复制文件失败")
        sys.exit(1)

    print("\n✅ 构建完成！")
    print(f"📁 可执行文件已输出到: {os.path.abspath('.dist')}")

    # 显示手动安装说明
    print("\n📖 手动安装说明:")
    print("=" * 40)

    system = platform.system()
    dist_file = os.path.abspath(
        os.path.join(".dist", "ag.exe" if system == "Windows" else "ag")
    )

    print(f"1. 复制以下文件到任意PATH目录:")
    print(f"   {dist_file}")
    print()

    print("2. 推荐的PATH目录:")
    recommended_dirs = get_recommended_path_dirs()
    path_dirs = get_system_path_dirs()

    for i, dir_path in enumerate(recommended_dirs[:5]):  # 显示前5个推荐目录
        in_path = " (在PATH中)" if dir_path in path_dirs else ""
        print(f"   {i + 1}. {dir_path}{in_path}")

    print()
    print("3. 复制命令示例:")
    if system == "Windows":
        print(f'   copy "{dist_file}" "C:\\Windows\\System32\\"')
        if recommended_dirs:
            print(f'   copy "{dist_file}" "{recommended_dirs[0]}\\"')
    else:
        print(f'   cp "{dist_file}" "/usr/local/bin/"')
        if recommended_dirs:
            print(f'   cp "{dist_file}" "{recommended_dirs[0]}/"')

    print()
    print("4. 验证安装:")
    print("   复制完成后，打开新终端并运行:")
    print("   ag --help")

    print()
    print("💡 提示:")
    print("   - 可能需要管理员权限才能复制到系统目录")
    print("   - 复制后可能需要重启终端才能生效")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ 构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建过程中出现错误: {e}")
        sys.exit(1)
