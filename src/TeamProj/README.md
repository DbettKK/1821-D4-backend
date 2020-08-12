### 环境

在本地运行的时候，可以使用虚拟环境

我也导出了相应的requirements清单

```python
# 创建虚拟环境
python -m venv venv
# 激活进入虚拟环境
venv\scripts\activate
# 安装相应模块
pip install -r requirements.txt
```

当然也可以直接在本机python环境下开发，就直接执行上文的最后一条语句即可。

### 注意

我创建了一个我自己的超级用户

需要创建的可自行创建即可

然后setting.py文件中有关数据库的账户密码和域名被我删掉了，不过数据库名称就是teamproj

每次上传的时候也请一定记住删掉，避免被恶意访问