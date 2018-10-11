# ZRBoom
爆破zip，rar文件密码

# 环境说明

## 运行环境
> Python 3.x

## 相关模块说明
> unrar >= 0.3

>只爆破zip文件，该模块可不安装。安装该python模块后还应该安装对于系统的库文件，详情请参照:

>[unrar 说明](https://pypi.org/project/unrar/)

>[解决Python下安装unrar后仍然提示Couldn't find path to unrar library](https://blog.csdn.net/ysy950803/article/details/52939708)
 
# 使用说明

```bash
git clone https://github.com/SuanCaiYu0413/ZRBoom.git

cd ZRBoom

pip install -r requirements.txt

python main.py -h #帮助说明

python main.py -f test.zip -d wordlist.txt -t 10 #测试使用
```
