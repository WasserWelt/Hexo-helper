import os
import subprocess
import sys
from datetime import datetime
import webbrowser
import colorama
from colorama import Fore, Back, Style
import questionary

colorama.init(autoreset=True)

class HexoAssistant:
    def __init__(self):
        self.hexo_path = self._find_hexo()
        self.project_path = os.getcwd()
        self._check_hexo_project()
    
    def _find_hexo(self):
        """查找Hexo可执行文件路径"""
        try:
            # 检查全局安装的hexo
            result = subprocess.run(['where', 'hexo'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.splitlines()[0].strip()
            
            # 检查本地node_modules中的hexo
            local_hexo = os.path.join('node_modules', '.bin', 'hexo')
            if os.path.exists(local_hexo):
                return local_hexo
                
            return 'hexo'  # 最后尝试直接调用
        except:
            return 'hexo'
    
    def _check_hexo_project(self):
        """检查当前目录是否是Hexo项目"""
        required_files = ['_config.yml', 'package.json']
        for file in required_files:
            if not os.path.exists(file):
                print(Fore.RED + f"错误: 当前目录不是Hexo项目(缺少{file})")
                sys.exit(1)
    
    def _run_command(self, command, show_output=True):
        """执行命令并处理输出"""
        try:
            result = subprocess.run(
                command,
                cwd=self.project_path,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if show_output and result.stdout:
                print(Fore.CYAN + result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"命令执行失败: {e.stderr}")
            return False
    
    def show_menu(self):
        """显示主菜单"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.YELLOW + "="*50)
            print(Fore.GREEN + "  Hexo博客管理助手")
            print(Fore.YELLOW + "="*50)
            
            choice = questionary.select(
                "请选择操作:",
                choices=[
                    "新建文章",
                    "新建草稿",
                    "生成静态文件",
                    "启动本地服务器",
                    "部署到服务器",
                    "清理缓存",
                    "生成并部署",
                    "生成并启动服务器",
                    "打开博客目录",
                    "退出"
                ]
            ).ask()
            
            if choice == "新建文章":
                self._new_post(is_draft=False)
            elif choice == "新建草稿":
                self._new_post(is_draft=True)
            elif choice == "生成静态文件":
                self._generate()
            elif choice == "启动本地服务器":
                self._server()
            elif choice == "部署到服务器":
                self._deploy()
            elif choice == "清理缓存":
                self._clean()
            elif choice == "生成并部署":
                self._generate()
                self._deploy()
            elif choice == "生成并启动服务器":
                self._generate()
                self._server()
            elif choice == "打开博客目录":
                self._open_directory()
            elif choice == "退出":
                print(Fore.GREEN + "感谢使用Hexo助手，再见！")
                sys.exit(0)
            
            input("\n按Enter键继续...")
    
    def _new_post(self, is_draft):
        """新建文章或草稿"""
        title = questionary.text("请输入文章标题:").ask()
        if not title:
            return
        
        # 替换特殊字符
        filename = title.replace(' ', '-')
        
        # 构建命令
        post_type = "draft" if is_draft else "post"
        cmd = f'{self.hexo_path} new {post_type} "{title}"'
        
        print(Fore.YELLOW + f"正在创建{post_type}...")
        if self._run_command(cmd):
            # 获取文件路径
            dir_name = "_drafts" if is_draft else "_posts"
            filepath = os.path.join("source", dir_name, f"{filename}.md")
            
            print(Fore.GREEN + f"成功创建: {filepath}")
            
            # 询问是否要编辑
            if questionary.confirm("是否立即用编辑器打开文件?").ask():
                try:
                    os.startfile(filepath)
                except Exception as e:
                    print(Fore.RED + f"无法打开文件: {e}")
    
    def _generate(self):
        """生成静态文件"""
        print(Fore.YELLOW + "正在生成静态文件...")
        if self._run_command(f"{self.hexo_path} generate"):
            print(Fore.GREEN + "静态文件生成完成!")
    
    def _server(self):
        """启动本地服务器"""
        port = questionary.text("请输入端口号(默认4000):", default="4000").ask()
        print(Fore.YELLOW + f"启动本地服务器(端口:{port})...")
        
        # 询问是否打开浏览器
        open_browser = questionary.confirm("是否自动打开浏览器?").ask()
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
        print(Fore.YELLOW + "正在部署到服务器...")
        if self._run_command(f"{self.hexo_path} deploy"):
            print(Fore.GREEN + "部署完成!")
    
    def _clean(self):
        """清理缓存"""
        print(Fore.YELLOW + "正在清理缓存...")
        if self._run_command(f"{self.hexo_path} clean"):
            print(Fore.GREEN + "缓存清理完成!")
    
    def _open_directory(self):
        """打开博客目录"""
        dirs = {
            "文章目录": "source/_posts",
            "草稿目录": "source/_drafts",
            "主题目录": "themes",
            "静态文件目录": "public"
        }
        
        choice = questionary.select(
            "选择要打开的目录:",
            choices=list(dirs.keys()) + ["返回"]
        ).ask()
        
        if choice != "返回":
            dir_path = os.path.join(self.project_path, dirs[choice])
            if os.path.exists(dir_path):
                os.startfile(dir_path)
            else:
                print(Fore.RED + f"目录不存在: {dir_path}")

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