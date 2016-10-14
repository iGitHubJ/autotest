###自动化测试框架
<pre>
<li>说明：
	编译环境：Python  2.7
	操作系统：Windows/Linux
	依赖包：httplib2，Django
		windos用户，请将install.bat文件移动到Python27的安装主目录，然后双击运行
		linux用户，请运行install.sh脚本

<li>目录结构
	|─server.bat启动服务器（Windows平台），默认端口8000
	|─server.sh启动服务器（Linux），默认端口8000
	|─sqlite3.db数据库文件
	├─install.bat安装依赖插件（Windows平台）
	├─install.sh安装依赖插件（Linux）
	├─autotest 主目录
	├─config 配置文件目录
	├─interapp 主目录
	├─templates 主目录
	└─utils 主目录


启动服务器后，访问 <a href="http://localhost:8000/static/index.html">http://localhost:8000/static/index.html</a> 开启测试之旅!
下载最新源码：<a href="https://github.com/iGitHubJ/autotest">https://github.com/iGitHubJ/autotest</a>

<i>请将反馈信息发送至邮箱 <a href="mailto:898596025@qq.com">898596025@qq.com</a></i>
</pre>
