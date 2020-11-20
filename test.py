import re
import json,os,sys
from collections  import abc
# str01 = '''a:2:{s:2:"in";a:5:{i:0;s:10:"1464070293";i:1;s:10:"1464070611";i:2;s:10:"1464070950";i:3;s:10:"1464071656";i:4;s:10:"1464072082";}s:3:"out";a:5:{i:0;s:10:"1464070559";i:1;s:10:"1464070945";i:2;s:10:"1464071402";i:3;s:10:"1464072077";i:4;s:10:"1464072532";}}'''
# str02 = '{"title":{"img":"20180301\/507c286d7cff01c69792.png","name":"title","color":"#2F2F35","alpha":0.3},"seat":{"img":"","name":"seat","color":"#2F2F35","alpha":0},"background":{"img":"","name":"background","color":"#2E3037","alpha":1},"outBackground":{"img":"","name":"outBackground","color":"#000000","alpha":1},"recordCountdown":{"duration":600},"recordBitRatePlus":false,"echoCancellationDisabled":false,"headimageToolbar":{"teacher":{"ResetAll":true,"MuteAll":true,"DownStageAll":false,"AllStudentsToFreeRegion":true,"ReplaceAll":false,"RewardAll":true,"AuthorityAll":false},"student":{"authority":true,"Mute":true,"reward":true,"Stage":true}},"commentWindow":{"CommentVisible":true},"clouddisk":{"teacherDefaultTab":"AuthorizedResources","limitStudentsCloseCourseWare":false},"classroomWindow":{"student":{"FrontLock":false,"ScreenMark":false},"teacher":{"ExtendClassTime":false,"CameraMirroring":false,"LockBlackboardElement":false,"Win7AeroThemeRecording":false,"MoveStudentOut":true}},"help":{"studentsShow":false},"chatWindow":{"QuestionVisible":true,"EnableSnapshot":true,"MinTimespan":0},"screenShare":{"studentsControlTeacher":false,"ScreenShareMemberLimit":35},"handsupWindow":{"visible":true},"blackboard":{"limitStudentsScroll":false},"dropBlackboardAuthority":false,"dropBackStageCancelAuthority":false,"SmallBlackboardMemberLimit":35,"boardToolbar":{"teacher":{"MiniToolbox":true,"MiniTools":[]},"student":{"Roster":true}}}'
# str03 = '''a:5:{s:2:"in";a:2:{i:0;s:10:"1594891562";i:1;s:10:"1594891975";}s:13:"platform_type";a:2:{i:0;i:301;i:1;i:301;}s:7:"os_type";a:2:{i:0;i:4;i:1;i:4;}s:3:"out";a:2:{i:0;s:10:"1594891676";i:1;s:10:"1594892246";}s:11:"exit_status";a:2:{i:0;s:2:"56";i:1;s:3:"111";}}'''
# str04 = '''a:2:{s:2:"in";a:1:{i:0;s:10:"1467868772";}s:3:"out";a:1:{i:0;s:10:"1467869025";}}'''
# str112 = 'a:3:{s:3:"out";a:2:{i:0;s:10:"1474376929";i:1;s:10:"1474377337";}s:11:"exit_status";a:2:{i:0;s:1:"1";i:1;s:1:"1";}s:2:"in";a:1:{i:0;s:10:"1474376933";}}'
# str05 = 'a:3:{s:2:"in";a:2:{i:0;s:10:"1501134167";i:1;s:10:"1501140558";}s:3:"out";a:1:{i:0;s:10:"1501141533";}s:11:"exit_status";a:1:{i:0;s:1:"1";}}'

from handleserivce.handleJson import jsonToList
from handleserivce.handleJson import jsonToList
# str11 = '{["uid":"1000082","isInClass":1,"platformType":2]}'
# print(re.sub('\]$',"",re.sub('^\[?',"",str11)))


# tablelist = ['class_id']
# for i in tablelist:
#     print("            try:")
#     print("             {name} = valDict[\"{name}\"]".format(name=i))
#     print("            except KeyError as e:")
#     print("            	{name} = \"0\"".format(name=i))


'''
from common.common import getBinlogValues
str12 ={'db': 'eo_os', 'table': 'eeo_school_auth_info', 'event_type': 2, 'data': {'before': {'school_auth_info_id': '1335', 'school_uid': '2388352', 'school_introduce': '<p>放大</p>', 'class_skin_id': '1', 'del_pic_month': '3', 'del_video_month': '3', 'open_cloud_disk': '0', 'push_class_report': '1', 'balance_remind': '1', 'class_remind': '1', 'balance_remind_info': '[{"money":50000,"telephone":[15810913872]},{"money":200000,"telephone":[15810913872]}]', 'class_remind_info': '{"student":{"day":"111","hour":"211","minute":"321"},"teacher":{"day":"111","hour":"211","minute":"321"}}', 'auto_del_video': '1', 'auto_del_pic': '0', 'student_num': '100', 'stage_num': '13', 'audit_num': '20', 'sub_num': '100', 'class_num': '200', 'super_custom_service': '1', 'hidden_mob': '0', 'notify_mail': '', 'class_report_info': '{"configList":[{"configId":0,"configName":"studyReportTemplate1","layoutSort":["topUserAvatarBox","topUserInfoBox","teacherCommentsBox","lessonIntroBox","studentAchievementBox","studentActivityDegreeBox","studentAttendanceBox","studentLessonNoteBox","teacherLessonNoteBox","assistantLessonNoteBox","lessonMomentsBox","schoolIntroBox"],"visibleConfig":{"schoolBrand":true,"lessonName":true,"teacherComments":true,"teacherCommentsTranslate":true,"lessonIntro":true,"studentAchievement":true,"studentRewardRanking":true,"singleStudentRewardRanking":true,"studentLessonAnswerAccuracy":true,"studentActivityDegree":true,"studentActivityDegreeRanking":true,"studentActivityDegreeOnStageTimes":true,"studentActivityDegreeOnSpeakTimes":true,"studentActivityDegreeOnControlTimes":true,"studentAttendance":true,"studentLessonAttendance":true,"studentAttendNum":true,"studentLateNum":true,"studentQuitEarly":true,"studentLessonNote":true,"teacherLessonNote":true,"assistantLessonNote":true,"lessonVideo":true,"lessonMoments":true,"schoolIntro":true}},{"configId":1,"configName":"studyReportTemplate2","layoutSort":["topUserAvatarBox","topUserInfoBox","teacherCommentsBox","lessonIntroBox","studentAchievementBox","studentAnswerAccuracyBox","studentActivityDegreeBox","studentAttendanceBox","studentLessonNoteBox","teacherLessonNoteBox","assistantLessonNoteBox","lessonMomentsBox","schoolIntroBox"],"visibleConfig":{"schoolBrand":true,"lessonName":true,"teacherComments":true,"teacherCommentsTranslate":true,"lessonIntro":true,"studentAchievement":true,"studentRewardRanking":true,"singleStudentRewardRanking":true,"studentLessonAnswerAccuracy":true,"studentActivityDegree":true,"studentActivityDegreeRanking":true,"studentActivityDegreeOnStageTimes":true,"studentActivityDegreeOnSpeakTimes":true,"studentActivityDegreeOnControlTimes":true,"studentAttendance":true,"studentLessonAttendance":true,"studentAttendNum":true,"studentLateNum":true,"studentQuitEarly":true,"studentLessonNote":true,"teacherLessonNote":true,"assistantLessonNote":true,"lessonVideo":false,"lessonMoments":true,"schoolIntro":true}}],"configUse":0}', 'guide_step': '0', 'cloud_free_volume': '', 'cloud_folder_toplimit': '2000', 'classroom_set_num': '10', 'hd_legibility': '1', 'login_no_checking': '0', 'double_teacher_course': '0', 'sole_supervise_class_page': '0', 'authorize_between_school': '1', 'add_course_student_replay': '0', 'delete_course_student_replay': '0', 'repaly_view_power': '0', 'avoid_record_replay': '1', 'set_as_cluster_nickname': '1', 'live_reservation': '20200703/013e1a65a7ba02257709.jpg', 'live_default_cover': '{"live1":{"radioValue":1,"customizeTips":{"zh-CN":"世界很大，我想去看看","en":"但是房贷算房贷房贷算发第三方神大夫"}},"live2":{"radioValue":1,"customizeTips":{"zh-CN":"老师开小差啦，同学们可以回忆一下课堂内容，马上回来！","en":"不要着急"}},"live3":{"radioValue":1,"customizeTips":{"zh-CN":"","en":""}}}', 'customize_live_prompt': '20200703/7f855a8707bfd2138313.png', 'default_course_cover': ''}, 'after': {'school_auth_info_id': '1335', 'school_uid': '2388352', 'school_introduce': '<p>放大</p>', 'class_skin_id': '2019', 'del_pic_month': '3', 'del_video_month': '3', 'open_cloud_disk': '0', 'push_class_report': '1', 'balance_remind': '1', 'class_remind': '1', 'balance_remind_info': '[{"money":50000,"telephone":[15810913872]},{"money":200000,"telephone":[15810913872]}]', 'class_remind_info': '{"student":{"day":"111","hour":"211","minute":"321"},"teacher":{"day":"111","hour":"211","minute":"321"}}', 'auto_del_video': '1', 'auto_del_pic': '0', 'student_num': '100', 'stage_num': '13', 'audit_num': '20', 'sub_num': '100', 'class_num': '200', 'super_custom_service': '1', 'hidden_mob': '0', 'notify_mail': '', 'class_report_info': '{"configList":[{"configId":0,"configName":"studyReportTemplate1","layoutSort":["topUserAvatarBox","topUserInfoBox","teacherCommentsBox","lessonIntroBox","studentAchievementBox","studentActivityDegreeBox","studentAttendanceBox","studentLessonNoteBox","teacherLessonNoteBox","assistantLessonNoteBox","lessonMomentsBox","schoolIntroBox"],"visibleConfig":{"schoolBrand":true,"lessonName":true,"teacherComments":true,"teacherCommentsTranslate":true,"lessonIntro":true,"studentAchievement":true,"studentRewardRanking":true,"singleStudentRewardRanking":true,"studentLessonAnswerAccuracy":true,"studentActivityDegree":true,"studentActivityDegreeRanking":true,"studentActivityDegreeOnStageTimes":true,"studentActivityDegreeOnSpeakTimes":true,"studentActivityDegreeOnControlTimes":true,"studentAttendance":true,"studentLessonAttendance":true,"studentAttendNum":true,"studentLateNum":true,"studentQuitEarly":true,"studentLessonNote":true,"teacherLessonNote":true,"assistantLessonNote":true,"lessonVideo":true,"lessonMoments":true,"schoolIntro":true}},{"configId":1,"configName":"studyReportTemplate2","layoutSort":["topUserAvatarBox","topUserInfoBox","teacherCommentsBox","lessonIntroBox","studentAchievementBox","studentAnswerAccuracyBox","studentActivityDegreeBox","studentAttendanceBox","studentLessonNoteBox","teacherLessonNoteBox","assistantLessonNoteBox","lessonMomentsBox","schoolIntroBox"],"visibleConfig":{"schoolBrand":true,"lessonName":true,"teacherComments":true,"teacherCommentsTranslate":true,"lessonIntro":true,"studentAchievement":true,"studentRewardRanking":true,"singleStudentRewardRanking":true,"studentLessonAnswerAccuracy":true,"studentActivityDegree":true,"studentActivityDegreeRanking":true,"studentActivityDegreeOnStageTimes":true,"studentActivityDegreeOnSpeakTimes":true,"studentActivityDegreeOnControlTimes":true,"studentAttendance":true,"studentLessonAttendance":true,"studentAttendNum":true,"studentLateNum":true,"studentQuitEarly":true,"studentLessonNote":true,"teacherLessonNote":true,"assistantLessonNote":true,"lessonVideo":false,"lessonMoments":true,"schoolIntro":true}}],"configUse":0}', 'guide_step': '0', 'cloud_free_volume': '', 'cloud_folder_toplimit': '2000', 'classroom_set_num': '10', 'hd_legibility': '1', 'login_no_checking': '0', 'double_teacher_course': '0', 'sole_supervise_class_page': '0', 'authorize_between_school': '1', 'add_course_student_replay': '0', 'delete_course_student_replay': '0', 'repaly_view_power': '0', 'avoid_record_replay': '1', 'set_as_cluster_nickname': '1', 'live_reservation': '20200703/013e1a65a7ba02257709.jpg', 'live_default_cover': '{"live1":{"radioValue":1,"customizeTips":{"zh-CN":"世界很大，我想去看看","en":"但是房贷算房贷房贷算发第三方神大夫"}},"live2":{"radioValue":1,"customizeTips":{"zh-CN":"老师开小差啦，同学们可以回忆一下课堂内容，马上回来！","en":"不要着急"}},"live3":{"radioValue":1,"customizeTips":{"zh-CN":"","en":""}}}', 'customize_live_prompt': '20200703/7f855a8707bfd2138313.png', 'default_course_cover': ''}}, 'updated_fields': {'school_auth_info_id': False, 'school_uid': False, 'school_introduce': False, 'class_skin_id': True, 'del_pic_month': False, 'del_video_month': False, 'open_cloud_disk': False, 'push_class_report': False, 'balance_remind': False, 'class_remind': False, 'balance_remind_info': False, 'class_remind_info': False, 'auto_del_video': False, 'auto_del_pic': False, 'student_num': False, 'stage_num': False, 'audit_num': False, 'sub_num': False, 'class_num': False, 'super_custom_service': False, 'hidden_mob': False, 'notify_mail': False, 'class_report_info': False, 'guide_step': False, 'cloud_free_volume': False, 'cloud_folder_toplimit': False, 'classroom_set_num': False, 'hd_legibility': False, 'login_no_checking': False, 'double_teacher_course': False, 'sole_supervise_class_page': False, 'authorize_between_school': False, 'add_course_student_replay': False, 'delete_course_student_replay': False, 'repaly_view_power': False, 'avoid_record_replay': False, 'set_as_cluster_nickname': False, 'live_reservation': False, 'live_default_cover': False, 'customize_live_prompt': False, 'default_course_cover': False}, 'execute_time': 1597135538}

print(getBinlogValues(str12))
print(dict(zip(getBinlogValues(str12)[0],getBinlogValues(str12)[1])))

# !/usr/bin/python3

import pymongo

myclient = pymongo.MongoClient("mongodb://10.1.0.11:27017/")
mydb = myclient["eeotest"]
mycol = mydb["users"]

for num in range(100):
    mydict = {"uid":i,"name":i}
    x = mycol.insert_one(mydict)
    print(mydict)
'''


datastr = "stageEnd=Document{{{{UpTotal=5, DownCount=0, UpCount=1, DownTotal=0}}}}, " \
          "silenceEnd=Document{{SilenceAll=Document{{Count=0, Total=0}}, Persons=Document{{{{Total=5}}}}}}, " \
          "authorizeEnd=Document{{{{Count=1, Total=5}}}}, inoutEnd=Document{{{{Total=5, Details=[Document{{Device=0, Type=In, " \
          "Time=1603440724}}, Document{{Type=Out, Time=1603440729}}], Identity=3}}}}, " \
          "muteEnd=Document{{Persons=Document{{{{Total=5}}}}, MuteAll=Document{{Count=0, Total=0}}}}, " \
          "equipmentsEnd=Document{{{{Camera=Document{{Total=5}}}}}}"


# def matchlp(s):
#     pos = []
#     rs = ""
#     for i in range(0, len(s)):
#         if (s[i] == '{'):
#             pos.append(i)
#             continue
#         if (s[i] == '}' and pos):
#             ts = s[pos[-1]: i + 1]
#             if (len(ts) > len(rs)):
#                 rs = ts
#             pos.pop()
#     return rs
#
#
#
# for i in range(10):
#     rs = matchlp(datastr)
#     try:
#         l_bracket = re.match("^(\{)+", rs).group()
#         r_bracket = "}" * int(len(l_bracket))
#         after_rs =re.sub("(?<=^){aa}(?!$)".format(aa=l_bracket), "",re.sub("{aa}$".format(aa=r_bracket),"",rs))
#         # print("--------rs------->",rs)
#         print("--------after_rs------->",after_rs)
#     except AttributeError as e:
#         pass


    # if len(rs) ==0:
    #     break
    # if len(matchlp(rs)) >0:
    #     pass



    # datastr = datastr.replace(rs,"=list")
# print(datastr)


print("-----------------------------------------------")

str11 = {"ts":6886695294214340610,"v":2,"op":"i","ns":"hamster.ClassSummary44","o":[{"Name":"_id","Value":"5f9274e2fa63f14b64274d87"},{"Name":"ActionTime","Value":1603433698},{"Name":"CID","Value":3606866},{"Name":"CourseID","Value":1742379},{"Name":"Cmd","Value":"End"},{"Name":"CloseTime","Value":1603433608},{"Name":"StartTime","Value":1603432648},{"Name":"SID","Value":1334488},{"Name":"Data","Value":[{"Name":"stageEnd","Value":[{"Name":"1334488","Value":[{"Name":"DownCount","Value":0},{"Name":"UpTotal","Value":77},{"Name":"UpCount","Value":1},{"Name":"DownTotal","Value":0}]}]},{"Name":"silenceEnd","Value":[{"Name":"SilenceAll","Value":[]},{"Name":"Persons","Value":[{"Name":"1334488","Value":[{"Name":"Total","Value":77}]}]}]},{"Name":"muteEnd","Value":[{"Name":"Persons","Value":[{"Name":"1334488","Value":[{"Name":"Total","Value":77}]}]},{"Name":"MuteAll","Value":[]}]},{"Name":"authorizeEnd","Value":[{"Name":"1334488","Value":[{"Name":"Count","Value":1},{"Name":"Total","Value":77}]}]},{"Name":"screenshareEnd","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0},{"Name":"Period","Value":[]}]},{"Name":"inoutEnd","Value":[{"Name":"1334488","Value":[{"Name":"Total","Value":77},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1603432653}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1603432730}]]},{"Name":"Identity","Value":3}]}]},{"Name":"equipmentsEnd","Value":[{"Name":"1334488","Value":[{"Name":"Camera","Value":[{"Name":"Total","Value":0}]}]}]}]}],"o2":"null"}


# for i in str12["Value"]:
#     print(i["Name"],":",i["Value"])

# def nestedDictIter(nested):
#     for key, value in nested.items():
#         if isinstance(value, abc.Mapping):
#             # yield from nested_dict_iter(value)
#             for k2 in nestedDictIter(value):
#                 if isinstance(k2, int):
#                     k2 = str(k2)
#                 yield (key,) + k2
#         else:
#             yield key, value
import collections
#https://www.google.com/search?sxsrf=ALeKk00sJ-9F8LLSwIK7tIbm82YlyqXzpg%3A1605572187128&ei=WxazX9q0B8q80PEP3oejuA4&q=python+%E9%81%8D%E5%8E%86%E5%AD%97%E5%85%B8%E7%9A%84%E5%BE%AA%E7%8E%AF%E5%B5%8C%E5%A5%97+yield&oq=python+%E9%81%8D%E5%8E%86%E5%AD%97%E5%85%B8%E7%9A%84%E5%BE%AA%E7%8E%AF%E5%B5%8C%E5%A5%97+yield&gs_lcp=CgZwc3ktYWIQA1AAWABgngFoAHAAeACAAQCIAQCSAQCYAQCqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiazv--pojtAhVKHjQIHd7DCOcQ4dUDCA0&uact=5
# dict_str = {'a':{'b':{'c':1, 'd':2},'e':{'f':3, 'g':4}},'h':{'i':5, 'j':6}}


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            for k2 in recursive_items(value):
                yield (key,) + k2
            # yield from recursive_items(value)
        else:
            yield (key, value)

a001 = {'a': {"b": {"c": 2, "d": 4}, "e": {"f": 6}},"a1":11}

# print(next(recursive_items(a001)))
# for key in recursive_items(a001):
#     print(key)


list_str  = [{'Name': '1334488', 'Value': [{'Name': 'Total', 'Value': 77}, {'Name': 'Details', 'Value': [[{'Name': 'Device', 'Value': 0}, {'Name': 'Type', 'Value': 'In'}, {'Name': 'Time', 'Value': 1603432653}], [{'Name': 'Type', 'Value': 'Out'}, {'Name': 'Time', 'Value': 1603432730}]]}, {'Name': 'Identity', 'Value': 3}]}]


def detailsHandle(str):
    count = 0
    total_r = []
    for i in [x for x in range(len(str)) if x%2 == 0]:
        tmp_list = []
        tmp_dict = {}
        for value in str[i]:
            # tmp_dict[value["Name"]+"_in_"+str(count)] = value["Value"]
            tmp_dict[value["Name"]+"_in"] = value["Value"]
        for value in str[i+1]:
            # tmp_dict[value["Name"]+"_out_"+str(count)] = value["Value"]
            tmp_dict[value["Name"]+"_out"] = value["Value"]
        # count += 1
        # print(tmp_dict)
        total_r.append(tmp_dict)
    return  total_r


print("=========================================================")
# dict_l = {}
total_dict = {}
dict_l = {}
def nestedTest(str,keystr = ""):

    if isinstance(str,abc.Sequence):
        for value in str:
            # print("---------------->",value)
            nestedTest(value,'')

    elif isinstance(str,abc.Mapping):

        if isinstance(str["Value"],abc.Sequence):
            #
            if str["Name"] == "Details":
                dict_l[str["Name"]] = detailsHandle(str["Value"])
            else:
                nestedTest(str["Value"], '')

        elif isinstance(str,abc.Mapping):
            if str["Name"] == "Type":
                dict_l[str["Value"]] = 0
            else:
                dict_l[str["Name"]] = str["Value"]
                print("list----------->:",dict_l)

        #

str001 = [{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]}]
str002 = [{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]}]

liststr = [[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]
liststr1 = [{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]}]

# nestedTest(str001[0])

def detailsHandle_test(str):

    total_r = []
    for i in [x for x in range(len(str)) if x%2 == 0]:
        tmp_dict = {}
        for value in str[i]:
            tmp_dict[value["Name"]+"_in"] = value["Value"]
        for value in str[i+1]:
            tmp_dict[value["Name"]+"_out"] = value["Value"]
        total_r.append(tmp_dict)

    return  total_r

# print("0000000",detailsHandle_test(liststr))
# print(liststr1[0])

teststr = {"Name":"Data","Value":[{"Name":"stageEnd","Value":[{"Name":"1338366","Value":[{"Name":"DownCount","Value":114},{"Name":"DownTotal","Value":1513},{"Name":"UpCount","Value":114},{"Name":"UpTotal","Value":3710}]},{"Name":"1334360","Value":[{"Name":"DownCount","Value":5},{"Name":"DownTotal","Value":4730},{"Name":"UpCount","Value":2},{"Name":"UpTotal","Value":1992}]},{"Name":"1334356","Value":[{"Name":"DownCount","Value":204},{"Name":"DownTotal","Value":2552},{"Name":"UpCount","Value":205},{"Name":"UpTotal","Value":1553}]},{"Name":"1334362","Value":[{"Name":"DownCount","Value":83},{"Name":"DownTotal","Value":1233},{"Name":"UpCount","Value":83},{"Name":"UpTotal","Value":783}]},{"Name":"1325910","Value":[{"Name":"DownCount","Value":7},{"Name":"UpTotal","Value":0},{"Name":"UpCount","Value":0},{"Name":"DownTotal","Value":7947}]},{"Name":"1335588","Value":[{"Name":"DownCount","Value":0},{"Name":"UpTotal","Value":4668},{"Name":"UpCount","Value":12},{"Name":"DownTotal","Value":0}]},{"Name":"1325888","Value":[{"Name":"DownCount","Value":81},{"Name":"DownTotal","Value":12262},{"Name":"UpCount","Value":82},{"Name":"UpTotal","Value":894}]}]},{"Name":"handsupEnd","Value":[{"Name":"1334356","Value":[{"Name":"CTime","Value":3},{"Name":"Total","Value":1}]},{"Name":"1334362","Value":[{"Name":"CTime","Value":7},{"Name":"Total","Value":2}]},{"Name":"1325888","Value":[{"Name":"CTime","Value":62},{"Name":"Total","Value":17}]}]},{"Name":"textboardEnd","Value":[{"Name":"Count","Value":3},{"Name":"Total","Value":10865},{"Name":"Period","Value":[2583,318,7964]},{"Name":"DCount","Value":15}]},{"Name":"smallboardEnd","Value":[{"Name":"Count","Value":3},{"Name":"Total","Value":10908},{"Name":"Period","Value":[2594,343,7971]},{"Name":"DCount","Value":9}]},{"Name":"authorizeEnd","Value":[{"Name":"1338366","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1334360","Value":[{"Name":"Count","Value":5},{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1334362","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1325910","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1325888","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1335588","Value":[{"Name":"Count","Value":12},{"Name":"Total","Value":4668}]}]},{"Name":"inoutEnd","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791381}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795486}]]},{"Name":"Identity","Value":1}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792932}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794948}]]},{"Name":"Identity","Value":1}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796315}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796448}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796867}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796873}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797147}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797154}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797158}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797174}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797184}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797360}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797365}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797384}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599804977}]]},{"Name":"Identity","Value":194}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791363}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599792629}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792637}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794161}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794187}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794802}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794808}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794964}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794987}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795058}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795089}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795093}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795112}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795288}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795297}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795301}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795324}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795408}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795730}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795758}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796516}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797149}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797156}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797263}]]},{"Name":"Identity","Value":3}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791560}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791985}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792086}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796166}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796197}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796202}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796684}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599805330}]]},{"Name":"Identity","Value":1}]}]},{"Name":"muteEnd","Value":[{"Name":"Persons","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668}]}]},{"Name":"MuteAll","Value":[]}]},{"Name":"silenceEnd","Value":[{"Name":"SilenceAll","Value":[]},{"Name":"Persons","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668}]}]}]}]}
def getDataInfo(teststr):

    for value in teststr["Value"]:
        if value["Name"] == "inoutEnd":
            print("-----------------",value["Value"])
            total_dicts = {}
            tmp_dict = {}
            for val in value["Value"]:

                print(val["Name"])

                if val["Name"] == "Details":
                    tmp_dict["Details"] = detailsHandle(val["Value"])
                else:
                    # print(val["Name"])
                    pass

                    # print(detailsHandle(val["Value"]))
                    tmp_dict[val["Name"]] =  val["Value"]

            total_dicts[value["Name"]] = tmp_dict
            print("=========",total_dicts)

getDataInfo(teststr)


laststr = {"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]}