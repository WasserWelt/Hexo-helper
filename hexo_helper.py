import os
import subprocess
import sys
from datetime import datetime
import webbrowser
import colorama
from colorama import Fore, Back, Style
import json

colorama.init(autoreset=True)


class HexoAssistant:
    def __init__(self):
        self.hexo_path = self._find_hexo()
        self.project_path = os.getcwd()
        self._check_hexo_project()
        self.config_file = os.path.join(
            self.project_path, 'hexo_helper_config.json')
        self.templates = self._load_templates()

    def _check_hexo_project(self):
        """检查当前目录是否是Hexo项目"""
        required_files = ['_config.yml', 'package.json']
        for file in required_files:
            if not os.path.exists(file):
                print(Fore.RED + f"错误: 当前目录不是Hexo项目(缺少{file})")
                sys.exit(1)

    def _find_hexo(self):
        """查找Hexo可执行文件路径"""
        try:
            # 检查全局安装的hexo
            result = subprocess.run(
                ['where', 'hexo'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                path = result.stdout.splitlines()[0].strip()
                # 处理路径中的空格
                if ' ' in path:
                    return f'"{path}"'
                return path

            # 检查本地node_modules中的hexo
            local_hexo = os.path.join('node_modules', '.bin', 'hexo')
            if os.path.exists(local_hexo):
                return local_hexo

            return 'hexo'  # 最后尝试直接调用
        except Exception as e:
            print(Fore.RED + f"查找Hexo路径时出错: {e}")
            return 'hexo'

    def _run_command(self, command, show_output=True):
        """执行命令并处理输出"""
        try:
            # 确保命令是字符串形式
            if isinstance(command, list):
                command = ' '.join(command)

            print(Fore.YELLOW + f"执行命令: {command}")

            process = subprocess.Popen(
                command,
                cwd=self.project_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()

            if show_output and stdout:
                print(Fore.CYAN + stdout)
            if process.returncode != 0:
                print(Fore.RED + f"命令执行失败: {stderr}")
                return False
            return True
        except Exception as e:
            print(Fore.RED + f"执行命令时出错: {e}")
            return False

    def _clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_menu(self):
        """显示菜单选项"""
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + "  Hexo博客管理助手")
        print(Fore.YELLOW + "="*50)
        print("请选择操作:")
        print(Fore.CYAN + " 1. 新建文章")
        print(Fore.CYAN + " 2. 新建草稿")
        print(Fore.CYAN + " 3. 生成静态文件")
        print(Fore.CYAN + " 4. 启动本地服务器")
        print(Fore.CYAN + " 5. 部署到服务器")
        print(Fore.CYAN + " 6. 清理缓存")
        print(Fore.CYAN + " 7. 生成并部署")
        print(Fore.CYAN + " 8. 生成并启动服务器")
        print(Fore.CYAN + " 9. 打开博客目录")
        print(Fore.CYAN + "10. 模板管理")
        print(Fore.RED + " 0. 退出")
        print(Fore.YELLOW + "="*50)

    def _get_choice(self):
        """获取用户选择"""
        while True:
            try:
                choice = input(Fore.GREEN + "请输入选项数字(0-10): ")
                if choice.isdigit() and 0 <= int(choice) <= 10:
                    return int(choice)
                print(Fore.RED + "输入无效，请输入0-10的数字")
            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n操作已取消")
                sys.exit(0)

    def _load_templates(self):
        """加载模板配置"""
        default_templates = {
            "default": {
                "title": "",
                "date": "{{ now }}",
                "updated": "{{ now }}",
                "tags": [],
                "categories": [],
                "description": "",
                "toc": True,
            }
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                    # 合并默认模板和自定义模板(自定义优先)
                    return {**default_templates, **custom_templates.get('templates', {})}
            except Exception as e:
                print(Fore.YELLOW + f"加载模板配置失败，使用默认模板: {e}")
                return default_templates
        return default_templates

    def show_menu(self):
        """显示主菜单"""
        while True:
            self._clear_screen()
            self._show_menu()
            choice = self._get_choice()

            if choice == 1:
                self._new_post(is_draft=False)
            elif choice == 2:
                self._new_post(is_draft=True)
            elif choice == 3:
                self._generate()
            elif choice == 4:
                self._server()
            elif choice == 5:
                self._deploy()
            elif choice == 6:
                self._clean()
            elif choice == 7:
                self._generate()
                self._deploy()
            elif choice == 8:
                self._generate()
                self._server()
            elif choice == 9:
                self._open_directory()
            elif choice == 10:
                self._manage_templates()
            elif choice == 0:
                print(Fore.GREEN + "感谢使用Hexo助手，再见！")
                sys.exit(0)

            input("\n按Enter键继续...")

    def _new_post(self, is_draft):
        """新建文章或草稿"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 新建文章" if not is_draft else " 新建草稿")
        print(Fore.YELLOW + "="*50)

        title = input(Fore.CYAN + "请输入文章标题: ")
        if not title:
            return

        # 选择模板
        print(Fore.CYAN + "\n可用模板:")
        for i, name in enumerate(self.templates.keys(), 1):
            print(f" {i}. {name}")
        default_num = 1  # 默认选择第一个模板

        template_choice = input(
            Fore.CYAN + f"\n选择模板(1-{len(self.templates)}, 默认{default_num}): ") or str(default_num)

        try:
            template_index = int(template_choice) - 1
            template_name = list(self.templates.keys())[template_index]
        except (ValueError, IndexError):
            print(Fore.YELLOW + "无效选择，使用默认模板")
            template_name = 'default'

        # 替换特殊字符
        filename = title.replace(' ', '-')

        # 构建命令
        post_type = "draft" if is_draft else "post"
        cmd = f'{self.hexo_path} new {post_type} "{title}"'

        print(Fore.YELLOW + f"\n正在创建{post_type}...")
        if self._run_command(cmd):
            # 获取文件路径
            dir_name = "_drafts" if is_draft else "_posts"
            filepath = os.path.join("source", dir_name, f"{filename}.md")

            print(Fore.GREEN + f"\n成功创建: {filepath}")

            # 应用模板
            self._apply_template(filepath, template_name, title)

            # 询问是否要编辑
            edit = input(Fore.CYAN + "是否立即用编辑器打开文件?(y/n): ").lower()
            if edit == 'y':
                try:
                    os.startfile(filepath)
                except Exception as e:
                    print(Fore.RED + f"无法打开文件: {e}")

    def _generate(self):
        """生成静态文件"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 生成静态文件")
        print(Fore.YELLOW + "="*50)
        print(Fore.YELLOW + "正在生成静态文件...")
        if self._run_command(f"{self.hexo_path} generate"):
            print(Fore.GREEN + "\n静态文件生成完成!")

    def _server(self):
        """启动本地服务器"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 启动本地服务器")
        print(Fore.YELLOW + "="*50)

        port = input(Fore.CYAN + "请输入端口号(默认4000): ") or "4000"
        print(Fore.YELLOW + f"\n启动本地服务器(端口:{port})...")

        # 询问是否打开浏览器
        open_browser = input(Fore.CYAN + "是否自动打开浏览器?(y/n): ").lower() == 'y'
        if open_browser:
            webbrowser.open(f"http://localhost:{port}")

        # 启动服务器(会阻塞)
        try:
            subprocess.run(
                f"{self.hexo_path} server -p {port}",
                cwd=self.project_path,
                shell=True
            )
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n服务器已停止")

    def _deploy(self):
        """部署到服务器"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 部署到服务器")
        print(Fore.YELLOW + "="*50)
        print(Fore.YELLOW + "正在部署到服务器...")
        if self._run_command(f"{self.hexo_path} deploy"):
            print(Fore.GREEN + "\n部署完成!")

    def _clean(self):
        """清理缓存"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 清理缓存")
        print(Fore.YELLOW + "="*50)
        print(Fore.YELLOW + "正在清理缓存...")
        if self._run_command(f"{self.hexo_path} clean"):
            print(Fore.GREEN + "\n缓存清理完成!")

    def _open_directory(self):
        """打开博客目录"""
        self._clear_screen()
        print(Fore.YELLOW + "="*50)
        print(Fore.GREEN + " 打开博客目录")
        print(Fore.YELLOW + "="*50)

        dirs = {
            1: ("文章目录", "source/_posts"),
            2: ("草稿目录", "source/_drafts"),
            3: ("主题目录", "themes"),
            4: ("静态文件目录", "public"),
            0: ("返回", None)
        }

        while True:
            print("\n选择要打开的目录:")
            for num, (name, _) in dirs.items():
                if num != 0:
                    print(Fore.CYAN + f" {num}. {name}")
            print(Fore.RED + " 0. 返回")

            try:
                choice = int(input(Fore.GREEN + "\n请输入选项数字: "))
                if choice in dirs:
                    if choice == 0:
                        return

                    _, dir_path = dirs[choice]
                    full_path = os.path.join(self.project_path, dir_path)
                    if os.path.exists(full_path):
                        os.startfile(full_path)
                        print(Fore.GREEN + f"\n已打开: {dir_path}")
                        return
                    else:
                        print(Fore.RED + f"\n目录不存在: {dir_path}")
                        return
                else:
                    print(Fore.RED + "输入无效，请输入正确的数字")
            except ValueError:
                print(Fore.RED + "输入无效，请输入数字")

    def _save_templates(self):
        """保存模板配置"""
        try:
            config = {
                "templates": self.templates,
                "default_template": getattr(self, 'default_template', 'default')
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(Fore.RED + f"保存模板配置失败: {e}")
            return False

    def _apply_template(self, filepath, template_name, title):
        """应用模板到文章文件"""
        if template_name not in self.templates:
            print(Fore.YELLOW + f"模板'{template_name}'不存在，使用默认模板")
            template_name = 'default'

        template = self.templates[template_name].copy()

        # 处理特殊占位符
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for key, value in template.items():
            if isinstance(value, str):
                template[key] = value.replace('{{ now }}', now)
                template[key] = template[key].replace('{{ title }}', title)

        # 生成Front-matter
        front_matter = '---\n'
        for key, value in template.items():
            if isinstance(value, list):
                if value:  # 只有列表不为空时才写入
                    front_matter += f"{key}:\n"
                    for item in value:
                        front_matter += f"  - {item}\n"
            elif value:  # 只有值不为空时才写入
                front_matter += f"{key}: {value}\n"
        front_matter += '---\n\n'

        # 读取原文件内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换Front-matter部分
        if content.startswith('---'):
            content = content.split('---', 2)[-1]

        # 写入新内容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter + content)

        print(Fore.GREEN + f"已应用模板: {template_name}")

    def _manage_templates(self):
        """模板管理菜单"""
        while True:
            self._clear_screen()
            print(Fore.YELLOW + "="*50)
            print(Fore.GREEN + "  Front-matter模板管理")
            print(Fore.YELLOW + "="*50)

            print("\n当前模板列表:")
            for i, name in enumerate(self.templates.keys(), 1):
                print(Fore.CYAN + f" {i}. {name}")

            # print(Fore.YELLOW + "\n操作选项:")
            # print(Fore.CYAN + " 1. 查看/编辑模板")
            # print(Fore.CYAN + " 2. 添加新模板")
            # print(Fore.CYAN + " 3. 删除模板")
            # print(Fore.CYAN + " 4. 设置默认模板")
            print(Fore.RED + " 0. 返回主菜单")

            choice = input(Fore.GREEN + "\n请输入选项数字: ")

            # if choice == '1':
            #     self._view_edit_template()
            # elif choice == '2':
            #     self._add_template()
            # elif choice == '3':
            #     self._delete_template()
            # elif choice == '4':
            #     self._set_default_template()
            # elif choice == '0':
            if choice == '0':
                return
            else:
                print(Fore.RED + "无效输入，请重新选择")
                input("\n按Enter键继续...")


def main():
    try:
        assistant = HexoAssistant()
        assistant.show_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
