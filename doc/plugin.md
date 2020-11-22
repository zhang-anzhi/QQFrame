# 插件开发文档

插件位于 `plugins\` 文件夹内

## 插件基本信息

可以被 QQFrame 读取的插件需要创建名为 `PLUGIN_INFO` 的字典, 找不到该字典则会抛出 `PluginInfoError` 异常

该字典内需包含以下值, 缺少任意一项则会抛出 `PluginInfoError` 异常:

- name: str
- version: str

该字典内可选包含以下值:

- authors: list

## 事件

QQFrame 为插件提供了以下事件, 事件被触发时会调用插件内已经实现的事件方法

| 事件 | 触发条件 |
| - | - |
| on_load(server, old_module) | 插件被加载 |
| on_unload(server) | 插件被卸载 |
| on_server_start(server) | 接收服务器启动 |
| on_server_stop(server) | 接收服务器关闭 |
| on_command(server, command) | 控制台输入 |
| on_message(server, info) | 接收QQ消息 |
| on_notice(server, info) | 接收QQ通知 |

各参数的信息如下

### server

`utils/server_interface.py` 中的 `ServerInterface` 类, 提供插件控制QQFrame的接口

它具有以下属性:

| 属性 | 类型 | 功能 |
| - | - | - |
| logger | utils.logger.Logger | 日志记录器 [参考文档](https://docs.python.org/zh-cn/3/library/logging.html#logger-objects) |
| bot | utils.bot.Bot | 使用 [onebot](https://github.com/howmanybots/onebot) 标准的机器人类, 其方法列表可参考 [公开API](https://github.com/howmanybots/onebot/blob/master/v11/specs/api/public.md) |

其中bot对象具有方法 `request(path: str, data: dict = None)`, 该方法将会向api路径 `path` 发送 POST 请求, 用于使用不属于 onebot 标准的其他API

它具有以下方法:

#### 系统控制

| 方法 | 功能 |
| - | - |
| reload_config() | 重载配置文件 |
| exit() | 结束并退出QQFrame |

#### 消息

| 方法 | 功能 |
|-|-|
| reply(info: MessageParser, message) | 向消息源发送消息 |

#### 接收服务器

| 方法 | 功能 |
|-|-|
| is_server_running() | 返回接收服务器是否在运行的布尔值 |
| start() | 开启接收服务器 |
| stop() | 关闭接收服务器 |
| restart() | 重启接收服务器 |

#### 插件管理

| 方法 | 功能 |
|-|-|
| get_plugin_list() | 返回当前已加载插件列表 |
| get_plugin_info(plugin_name) | 返回名为 `plugin_name` 的插件信息字典 |
| reload_plugin(plugin_name) | 重载名为 `plugin_name` 的插件 |
| get_plugin_instance(plugin_name) | 获取名为 `plugin_name` 的插件实例 |
| call_event(plugin_name, func_name, args) | 启用新线程运行插件 `plugin_name` 的函数 `func_name`, 使用参数 `args` 为元组, 返回布尔的运行结果 |

### old_module

插件上次加载的模块实例

### on_message 的 info 参数

`utils/message_parser.py` 中的 `MessageParser` 类

该对象的属性与 onebot 标准的 [消息事件](https://github.com/howmanybots/onebot/blob/master/v11/specs/event/message.md) 相同

### on_notice 的 info 参数

`utils/notice_parser.py` 中的 `NoticeParser` 类

该对象的属性与 onebot 标准的 [通知事件](https://github.com/howmanybots/onebot/blob/master/v11/specs/event/notice.md) 相同

### command

该参数为字符串, 控制台的原始输入内容
