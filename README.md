# python 3.10.x 
# 安装环境
pip install pyinstaller

# 导入全部依赖
pip install -r requirements.txt

# 更新依赖列表
pip freeze > requirements.txt

# 打包
pyinstaller -F main.py

# 路径问题
if getattr(sys, 'frozen', False):
    # 获取当前程序的执行路径，打包的exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 获取当前程序的绝对路径, 本机启动
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
with open(os.path.join(BASE_DIR, "account.txt"), mode='r', encoding='utf-8') as f:
    data = f.read().strip()
print(data)