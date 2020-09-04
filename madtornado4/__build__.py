import os
import shutil

"""

    通过pyinstaller构建平台可执行程序，如windows下面的exe文件，
    需要安装pyinstaller，通过命令行：pip install pyinstaller

"""

if __name__ == '__main__':
    root_path = os.path.dirname(__file__)
    build_path = os.path.join(root_path, "dist/program")

    program = os.path.join(root_path, "program.py")
    code = os.system("pyinstaller {}".format(program))
    if code != 0:
        exit(code)

    ignore = ["build", "dist", "program.spec", "__pycache__", ".idea"]
    for file in os.listdir(root_path):
        if file in ignore:
            continue

        file_path = os.path.join(root_path, file)
        target_path = os.path.join(build_path, file)
        if os.path.isdir(file_path):
            shutil.copytree(file_path, target_path)
        else:
            shutil.copyfile(file_path, target_path)
