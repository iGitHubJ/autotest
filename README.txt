目录结构
	|---config
		|--config.xml 配置需要测试的接口（已废弃，由数据库统一管理）
	|---logs日志目录
		|--all.log 服务器运行日志、访问日志、脚本输入日志
		|--script.log 脚本执行中遇到的错误日志
	|---server.bat启动django自带的服务器，默认端口8000
	|---sqlite3.db数据库文件，
			server表：服务器信息，inter表：接口信息，result：测试结果
启动服务器后，访问http://localhost:8000/static/index.html测试