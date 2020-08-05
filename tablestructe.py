#ods_eeo_class_member_in_out

from multHandle import getMUTLResultOrJson,multisql
from parseConfig import *
class tableStruncte(object):

    eeo_class_member_time_header = "insert into {hadTableName}(`id`,`school_uid`,`course_id`,`class_id`,`member_uid`,`member_account`,`member_nickname`," \
                 "`is_late`,`is_on`,`is_early`,`identity`,`platform_type`,`stayin_time`,`add_time`,`client_class_id`,`json_in`,`json_platform_type`,`json_os_type`," \
                 "`json_out` ,`json_exit_status`,`duration`,operation_type,execute_time) values ".format(hadTableName=hadTableName)

    ##eeo_course_homework
    eeo_course_homework_header = "into ods_eeo_course_homework (homework_id, course_id, school_uid, teacher_uid, homework_title, homework_desc, " \
                                 "image, video, audio, docs, problems_ids, status, is_open, is_revise, is_del, is_download, open_type, score_type, score_value, " \
                                 "end_time, start_time, update_time, add_time) values "

    def eeo_class_member_time(valList):
        totalList = []
        for valDict in valList:
            try:
                id = valDict["id"]
            except KeyError as e:
                id = "0"
            try:
                school_uid = valDict["school_uid"]
            except KeyError as e:
                school_uid = "0"
            try:
                course_id = valDict["course_id"]
            except KeyError as e:
                course_id = "0"
            try:
                class_id = valDict["class_id"]
            except KeyError as e:
                class_id = "0"
            try:
                member_uid = valDict["member_uid"]
            except KeyError as e:
                member_uid = "0"
            try:
                member_account = valDict["member_account"]
            except KeyError as e:
                member_account = "0"
            try:
                member_nickname = valDict["member_nickname"]
            except KeyError as e:
                member_nickname = "0"
            try:
                is_late = valDict["is_late"]
            except KeyError as e:
                is_late = "0"
            try:
                is_on = valDict["is_on"]
            except KeyError as e:
                is_on = "0"
            try:
                is_early = valDict["is_early"]
            except KeyError as e:
                is_early = "0"
            try:
                identity = valDict["identity"]
            except KeyError as e:
                identity = "0"
            try:
                platform_type = valDict["platform_type"]
            except KeyError as e:
                platform_type = "0"
            try:
                stayin_time = valDict["stayin_time"]
            except KeyError as e:
                stayin_time = "0"
            try:
                add_time = valDict["add_time"]
            except KeyError as e:
                add_time = "0"
            try:
                client_class_id = valDict["client_class_id"]
            except KeyError as e:
                client_class_id = "0"
            try:
                json_in = valDict["json_in"]
            except KeyError as e:
                json_in = "0"
            try:
                json_platform_type = valDict["json_platform_type"]
            except KeyError as e:
                json_platform_type = "0"
            try:
                json_os_type = valDict["json_os_type"]
            except KeyError as e:
                json_os_type = "0"
            try:
                json_out = valDict["json_out"]
            except KeyError as e:
                json_out = "0"
            try:
                json_exit_status = valDict["json_exit_status"]
            except KeyError as e:
                json_exit_status = "0"
            try:
                duration = valDict["duration"]
            except KeyError as e:
                duration = "0"
            try:
                operation_type = valDict["operation_type"]
            except KeyError as e:
                operation_type = "0"

            try:
                execute_time = valDict["execute_time"]
            except KeyError as e:
                execute_time = "0"
            tempvalList = [id,school_uid,course_id,class_id,member_uid,member_account,member_nickname,is_late,is_on,is_early,identity,platform_type,stayin_time,add_time,client_class_id,json_in,json_platform_type,json_os_type,json_out ,json_exit_status,duration,operation_type,execute_time]
            totalList.append(tempvalList)

        # print("totalList----ods_eeo_class_member_in_out---->",totalList)
        totalListToStr = str(totalList).replace("[[","(").replace("]]",")").replace("[","(").replace("]",")").replace(" ","")
        # print("totalListToStr------->",totalListToStr)
        return  totalListToStr


    def ods_eeo_course_homework(valList):
        totalList = []
        for valDict in valList:
            try:
                homework_id = valDict["homework_id"]
            except KeyError as e:
                homework_id = "0"
            try:
                course_id = valDict["course_id"]
            except KeyError as e:
                course_id = "0"
            try:
                school_uid = valDict["school_uid"]
            except KeyError as e:
                school_uid = "0"
            try:
                teacher_uid = valDict["teacher_uid"]
            except KeyError as e:
                teacher_uid = "0"
            try:
                homework_title = valDict["homework_title"]
            except KeyError as e:
                homework_title = "0"
            try:
                homework_desc = valDict["homework_desc"]
            except KeyError as e:
                homework_desc = "0"
            try:
                image = valDict["image"]
            except KeyError as e:
                image = "0"
            try:
                video = valDict["video"]
            except KeyError as e:
                video = "0"
            try:
                audio = valDict["audio"]
            except KeyError as e:
                audio = "0"
            try:
                docs = valDict["docs"]
            except KeyError as e:
                docs = "0"
            try:
                problems_ids = valDict["problems_ids"]
            except KeyError as e:
                problems_ids = "0"
            try:
                status = valDict["status"]
            except KeyError as e:
                status = "0"
            try:
                is_open = valDict["is_open"]
            except KeyError as e:
                is_open = "0"
            try:
                is_revise = valDict["is_revise"]
            except KeyError as e:
                is_revise = "0"
            try:
                is_del = valDict["is_del"]
            except KeyError as e:
                is_del = "0"
            try:
                is_download = valDict["is_download"]
            except KeyError as e:
                is_download = "0"
            try:
                open_type = valDict["open_type"]
            except KeyError as e:
                open_type = "0"
            try:
                score_type = valDict["score_type"]
            except KeyError as e:
                score_type = "0"
            try:
                score_value = valDict["score_value"]
            except KeyError as e:
                score_value = "0"
            try:
                end_time = valDict["end_time"]
            except KeyError as e:
                end_time = "0"
            try:
                start_time = valDict["start_time"]
            except KeyError as e:
                start_time = "0"
            try:
                update_time = valDict["update_time"]
            except KeyError as e:
                update_time = "0"
            try:
                add_time = valDict["add_time"]
            except KeyError as e:
                add_time = "0"
            tempvalList = [homework_id,course_id,school_uid,teacher_uid,homework_title,homework_desc,image,video,audio,docs,problems_ids,status,is_open,is_revise,is_del,is_download,open_type,score_type,score_value,end_time,start_time,update_time,add_time]
            totalList.append(tempvalList)

        totalListToStr = str(totalList).replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")").replace(
            " ", "")

        return totalListToStr


# count = 1
# flag = False
# totalList = []
# for i in range(1000):
#     val = ods_eeo_class_member_in_out(getMUTLResultOrJson(str09 ,"time_list", "phpjson",1))
#     totalList.append(val)
#     multisql(totalList,count,10, flag)
#     print(count)
#
#     if count < 100:
#         count += 1
#
#     else:
#         count = 1
#         flag = False
#         totalList = []
