'''
@desc: FG群文件处理
@author: Martin Huang
@time: created on 2020/4/4 15:04
@修改记录:
'''
import nonebot
import time
import os
from nonebot.adapters.cqhttp.event import GroupMessageEvent

from nonebot.plugin import on_message
from . import Timer
from .Utils.JsonUtils import JsonUtils
from .Utils.IOUtils import IOUtils
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

configuration = JsonUtils.json2Dict(os.path.join(
    os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', 'config.json'))
groupInfo = configuration['groupInfo']
for group_id in groupInfo.keys():
    fpath = os.path.join(os.getcwd(), 'cn', 'acmsmu',
                         'FG', 'data', groupInfo[group_id])
    try:
        dataDict = dict()
        dataDict['flag'] = True
        dataDict['file'] = 'chatA.txt'
        IOUtils.mkdir(fpath)
        IOUtils.serializeObj2Pkl(dataDict, fpath + '/var.pkl')
    except FileExistsError:
        continue


def CheckGroup(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupMessageEvent) and str(event.group_id) in groupInfo.keys()


wordcloud = on_message(block=False, rule=CheckGroup)


# change the group session to nb2 event
# can even abandon the bot,if possible
@wordcloud.handle()
async def HandleGroupMsg(bot: Bot, event: GroupMessageEvent):
    # read each pkl
    # why dont we,i mean create an sql or something?
    dataDict = IOUtils.deserializeObjFromPkl(
        os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', str(event.group_id), 'var.pkl')
    flag = dataDict['flag']
    msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + \
        str(event.user_id) + '\n' + event.raw_message + '\n'
    # determine what file we would write
    if flag:
        with open(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', str(event.group_id), 'chatA.txt'), 'a', encoding='utf-8') as fileA:
            fileA.write(msg)
    else:
        with open(os.path.join(os.getcwd(), 'cn', 'acmsmu', 'FG', 'data', str(event.group_id), 'chatB.txt'), 'a', encoding='utf-8') as fileB:
            fileB.write(msg)


# @bot.on_message('group')
# async def handleGroupMsg(session):
#     groupInfo = configuration['groupInfo']
#     for each in groupInfo:
#         if each['groupId'] == str(session['group_id']):
#             # 读取每个群文件夹的pkl
#             dataDict = IOUtils.deserializeObjFromPkl(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'var.pkl'))
#             # 确定flag的值
#             flag = dataDict['flag']
#             # 确定要往哪一个文件中写入聊天记录
#             msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + str(session['user_id']) + '\n' + session['raw_message'] + '\n'
#             if flag:
#                 with open(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'chatA.txt'), 'a', encoding='utf-8') as fileA:
#                     fileA.write(msg)
#             else:
#                 with open(os.path.join(os.getcwd(),'cn','acmsmu','FG','data',each['groupId'],'chatB.txt'), 'a', encoding='utf-8') as fileB:
#                     fileB.write(msg)
#             break
