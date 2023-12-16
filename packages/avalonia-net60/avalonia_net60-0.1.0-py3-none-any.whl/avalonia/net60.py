import os

dir = os.path.abspath(os.path.dirname(__file__))
dir_net60 = os.path.join(dir, "net6.0")
dir_net60_dlls = {}
dir_net60_xmls = {}

if os.path.exists(dir_net60):
    for lib in os.listdir(dir_net60):
        path = os.path.join(dir_net60, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                dir_net60_dlls[lib] = path
            if os.path.splitext(path)[1] == ".xml":  # 判断文件扩展名是否为“.dll”
                dir_net60_xmls[lib] = path

print(dir_net60_dlls)
print(dir_net60_xmls)