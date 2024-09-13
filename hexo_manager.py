import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser

CONFIG_FILE = "config.ini"  # 配置文件名

# 初始化配置解析器
config = ConfigParser()


# 读取配置文件
def load_config():
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding="utf-8")
        hexo_path = config.get('Settings', 'hexo_path', fallback="未设置")
        typora_path = config.get('Settings', 'typora_path', fallback="未设置")
        return hexo_path, typora_path
    return "未设置", "未设置"


# 保存配置文件
def save_config(hexo_path, typora_path):
    if not config.has_section('Settings'):
        config.add_section('Settings')
    config.set('Settings', 'hexo_path', hexo_path)
    config.set('Settings', 'typora_path', typora_path)
    with open(CONFIG_FILE, 'w', encoding="utf-8") as file:
        config.write(file)


# 创建主窗口
root = tk.Tk()
root.title("Hexo 管理工具")
root.geometry("250x190")

# 定义全局变量
hexo_path, typora_path = load_config()  # 从配置文件加载路径
hexo_path_var = tk.StringVar(value=hexo_path)
typora_path_var = tk.StringVar(value=typora_path)
output_text = tk.StringVar()

# 定义处理命令行颜色编码的函数
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


# 定义执行命令的函数
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        output = strip_ansi_codes(result.stdout)
        output_text.set(output)
        messagebox.showinfo("操作结果", output)  # 显示操作结果
    except subprocess.CalledProcessError as e:
        error_message = strip_ansi_codes(e.stderr)
        output_text.set(error_message)
        messagebox.showerror("执行错误", error_message)  # 显示错误信息

# 打开 .md 文件的函数
def open_md_file(post_name):
    if hexo_path_var.get() != "未设置" and typora_path_var.get() != "未设置":
        md_file_path = os.path.join(hexo_path_var.get(), "source", "_posts", f"{post_name}.md")
        command = f'"{typora_path_var.get()}" "{md_file_path}"'
        execute_command(command)
    else:
        messagebox.showwarning("警告", "Hexo 或 Typora 路径未设置！")


# 主页面函数
def show_main_page():
    # 清除当前窗口
    for widget in root.winfo_children():
        widget.destroy()

    # 创建显示输出的文本框
    # output_label = tk.Label(root, textvariable=output_text, wraplength=550)
    # output_label.pack(pady=10)

    # 生成静态文件的函数
    def generate_site():
        if hexo_path_var.get() != "未设置":
            command = f"cd {hexo_path_var.get()} && hexo generate"
            execute_command(command)
        else:
            output_text.set("Hexo 路径未设置！")

    # 部署网站的函数
    def deploy_site():
        if hexo_path_var.get() != "未设置":
            command = f"cd {hexo_path_var.get()} && hexo deploy"
            execute_command(command)
        else:
            output_text.set("Hexo 路径未设置！")

    # 执行 hexo clean 的函数
    def clean_site():
        if hexo_path_var.get() != "未设置":
            command = f"cd {hexo_path_var.get()} && hexo clean"
            execute_command(command)
        else:
            output_text.set("Hexo 路径未设置！")

    # 创建按钮并绑定到函数
    btn_generate = tk.Button(root, text="生成静态文件", command=generate_site)
    btn_generate.place(x=20, y=20)

    btn_deploy = tk.Button(root, text="部署网站", command=deploy_site)
    btn_deploy.place(x=140, y=20)

    btn_clean = tk.Button(root, text="清理生成文件", command=clean_site)
    btn_clean.place(x=20, y=70)

    # 设置 Hexo 路径的按钮
    btn_set_path = tk.Button(root, text="设置路径", command=show_settings_page)
    btn_set_path.place(x=140, y=70)

    # 新建文章的输入框和按钮
    post_frame = tk.Frame(root, width=250, height=70)
    post_frame.place(x=0, y=120)

    post_label = tk.Label(post_frame, text="新建文章名：")
    post_label.place(x=10, y=0)

    post_entry = tk.Entry(post_frame, width=20)
    post_entry.place(x=80, y=0)

    def create_post():
        post_name = post_entry.get()
        if hexo_path_var.get() != "未设置":
            command = f"cd {hexo_path_var.get()} && hexo new \"{post_name}\""
            execute_command(command)
            open_md_file(post_name)

        else:
            output_text.set("Hexo 路径未设置！")



    btn_create_post = tk.Button(post_frame, text="新建文章", command=create_post)
    btn_create_post.place(x=70, y=30)



    # 启动 GUI 主循环
    root.mainloop()


# 设置页面函数
def show_settings_page():
    # 清除当前窗口
    for widget in root.winfo_children():
        widget.destroy()

    # 设置路径的输入框和按钮
    path_frame = tk.Frame(root, width=250, height=90)
    path_frame.place(x=0, y=0)

    path_label = tk.Label(path_frame, text="Hexo 路径：")
    path_label.place(x=0, y=10)

    path_entry = tk.Entry(path_frame, textvariable=hexo_path_var, width=20)
    path_entry.place(x=80, y=10)

    typora_label = tk.Label(path_frame, text="Typora 路径：")
    typora_label.place(x=0, y=30)

    typora_entry = tk.Entry(path_frame, textvariable=typora_path_var, width=20)
    typora_entry.place(x=80, y=30)

    def set_paths():
        hexo_path = path_entry.get()
        typora_path = typora_entry.get()
        if os.path.isdir(hexo_path) and os.path.isfile(typora_path):
            hexo_path_var.set(hexo_path)
            typora_path_var.set(typora_path)
            save_config(hexo_path, typora_path)
            messagebox.showinfo("设置", "路径已保存！")
        else:
            messagebox.showerror("错误", "无效的路径！")

    btn_set_path = tk.Button(path_frame, text="设置路径", command=set_paths)
    btn_set_path.place(x=140, y=60)

    # 返回主页面的按钮
    btn_back = tk.Button(root, text="返回", command=show_main_page)
    btn_back.place(x=70, y=60)

    # 创建显示输出的文本框
    # output_label = tk.Label(root, textvariable=output_text, wraplength=550)
    # output_label.pack(pady=10)


# 显示主页面
show_main_page()
