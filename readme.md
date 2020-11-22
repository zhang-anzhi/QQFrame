# QQFrame

> 使用Python实现的QQ控制台机器人框架
>
> 使用事件触发的插件系统
>
> 使用 [onebot](https://github.com/howmanybots/onebot) 标准

## 环境要求

已在以下环境测试:

- `Windows10 x64` `Python 3.8`

Python模块依赖已存储在 `requirements.txt` 中, 可以使用 `pip install -r requirement.txt` 来直接安装所有模块

## 使用方法

1. 在 [Release](https://github.com/zhang-anzhi/QQFrame/releases) 页面下载最新的release并解压, 安装所需依赖
1. 运行 `QQFrame.py`, 第一次启动时会自动创建配置文件

## 配置文件

`config.yaml`

### lang

默认值: `zh_cn`

使用的语言, 语言文件需位于 `lang` 文件夹中以 `lang.yaml` 格式命名

### api_url

默认值: `http://127.0.0.1:5700`

使用的机器人软件的API地址

### receive_url

默认值: `http://127.0.0.1:5701/post`

使用的机器人软件配置的上报地址

### debug_mode

默认值: `False`

调试模式开关, 调为 `True` 以启用控制台Debug输出

## 插件

阅读 [插件开发文档](doc/plugin.md) 查看插件开发文档

## 指令

| 指令 | 功能 |
| - | - |
| help | 显示帮助 |
| stop | 停止并退出 |
| status | 显示状态信息 |
| reload | 重载指令 |
| server | 接收服务器控制指令 |
| plugin | 插件管理指令 |
| reload all | 重载所有 |
| reload server | 重载接收服务器 |
| reload config | 重载配置文件 |
| server start | 开启接收服务器 |
| server stop | 关闭接收服务器 |
| plugin list | 列出所有插件 |
| plugin info <plugin_name> | 显示插件信息 |
| plugin reload <plugin_name> | 重载插件 |
