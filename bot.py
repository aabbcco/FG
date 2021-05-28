'''
@desc: FG主入口
@author: Martin Huang
@time: created on 2020/4/4 14:57
@修改记录:
'''
# import os
# from Utils.JsonUtils import JsonUtils
# import nonebot
# import config
# from nonebot import require
# scheduler = require('nonebot_plugin_apscheduler').scheduler

# if __name__ == '__main__':
#     configuration = JsonUtils.json2Dict(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'config.json'))
#     nonebot.init(config)
#     nonebot.load_plugins(
#         os.path.join(os.path.dirname(__file__), 'cn', 'acmsmu'),
#         'cn.acmsmu'
#     )
#     nonebot.run(host=configuration['nonebotHost'], port=configuration['nonebotPort'])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.gocq import Bot as GoCqBot

# Custom your logger
#
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", GoCqBot)

nonebot.load_builtin_plugins()
nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugins("cn/acmsmu/FG")
nonebot.load_plugin("nonebot_plugin_test")
# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!"
    )
    nonebot.run(app="__mp_main__:app")
