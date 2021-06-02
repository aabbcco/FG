'''
@desc: FG定时发布每日总结
@author: Martin Huang
@time: created on 2020/4/4 16:22
@修改记录:
        2020/4/12 => 修改定时器模式
'''
import nonebot
from nonebot import require
import os
from cn.acmsmu.FG import DailyConclusion
from Utils.JsonUtils import JsonUtils
from Utils.IOUtils import IOUtils

scheduler = require('nonebot_plugin_apscheduler').scheduler


async def handleTimer(timerName, groupId):
    dataDict = IOUtils.deserializeObjFromPkl(os.path.join(
        os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', groupId, 'var.pkl'))
    flag = dataDict['flag']
    clu = DailyConclusion.DailyConlusion(groupId)
    report = clu.generateReport()
    # print(timerName+'的每日总结为\n'+report)
    await bot.send_group_msg(group_id=int(groupId), message=report)
    if flag:
        dataDict['flag'] = False
        dataDict['file'] = 'chatB.txt'
        IOUtils.serializeObj2Pkl(dataDict, os.path.join(
            os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', groupId, 'var.pkl'))
        IOUtils.deleteFile(os.path.join(os.getcwd(), 'cn',
                           'acmsmu', 'FG', 'data', groupId, 'chatA.txt'))
    else:
        dataDict['flag'] = True
        dataDict['file'] = 'chatA.txt'
        IOUtils.serializeObj2Pkl(dataDict, os.path.join(
            os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', groupId, 'var.pkl'))
        IOUtils.deleteFile(os.path.join(os.getcwd(), 'cn',
                           'acmsmu', 'FG', 'data', groupId, 'chatB.txt'))

# multi bot in nonebot2,try to figure out what should I do
# a trick to slove this is that i know the framework contains only one bot so I could
# use get_bot and for _ to catch the only bot
bots = nonebot.get_bot()
for bot in bots.values():
    configuration = JsonUtils.json2Dict(os.path.join(
        os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'config.json'))
    print(configuration)
    groupInfo = configuration['groupInfo']
    for GroupId in groupInfo.keys():
        hour = groupInfo[GroupId]['beginHour']
        minutes = groupInfo[GroupId]['beginMinutes']
        scheduler.add_job(handleTimer, 'cron', hour=hour, minute=minutes, args=[
            groupInfo[GroupId]['timer'], groupInfo[GroupId]['groupId']])
        print('定时器' + groupInfo[GroupId]['timer'] + '定时任务添加成功!')
