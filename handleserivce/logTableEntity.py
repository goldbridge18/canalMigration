#ods_eeo_class_member_in_out

from handleserivce.multHandle import getMUTLResultOrJson,multisql
from common.parseConfig import *
class LogTableEntity(object):

    eeo_class_member_time_header = "insert into ods_eeo_class_member_time(`id`,`school_uid`,`course_id`,`class_id`,`member_uid`,`member_account`,`member_nickname`," \
                 "`is_late`,`is_on`,`is_early`,`identity`,`platform_type`,`stayin_time`,`add_time`,`client_class_id`,`json_in`,`json_platform_type`,`json_os_type`," \
                 "`json_out` ,`json_exit_status`,`duration`,operation_type,execute_time) values "

    ##eeo_course_homework

    eeo_course_homework_header = "into ods_eeo_course_homework (homework_id, course_id, school_uid, teacher_uid, homework_title, homework_desc, " \
                                 "image, video, audio, docs, problems_ids, status, is_open, is_revise, is_del, is_download, open_type, score_type, score_value, " \
                                 "end_time, start_time, update_time, add_time) values "

    eeo_class_and_student_header = "insert into ods_eeo_class_and_student_log(class_and_student_id,course_id,class_id,stud_id,school_uid,student_uid,isdel,is_isdel,operation_type,execute_time) values"


    def eeo_class_member_time(valList):
        # print(valList)
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
                platform_type = 0
            try:
                stayin_time = valDict["stayin_time"]
            except KeyError as e:
                stayin_time = 0
            try:
                add_time = valDict["add_time"]
            except KeyError as e:
                add_time = 0
            try:
                client_class_id = valDict["client_class_id"]
            except KeyError as e:
                client_class_id = 0
            try:
                json_in = valDict["json_in"]
            except KeyError as e:
                json_in = 0
            try:
                json_platform_type = valDict["json_platform_type"]
            except KeyError as e:
                json_platform_type = 0
            try:
                json_os_type = valDict["json_os_type"]
            except KeyError as e:
                json_os_type = 0
            try:
                json_out = valDict["json_out"]
            except KeyError as e:
                json_out = 0
            try:
                if len( valDict["json_exit_status"]) == 0:
                    json_exit_status = 0
                else:
                    json_exit_status = valDict["json_exit_status"]
            except KeyError as e:
                json_exit_status = 0
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

        totalListToStr = str(totalList).replace("[[","(").replace("]]",")").replace("[","(").replace("]",")").replace(" ","")

        return  totalListToStr


    def eeo_course_homework(valList):
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

    def eeo_class_and_student(valList):
        totalList = []
        for valDict in valList:
            try:
                class_and_student_id = valDict["class_and_student_id"]
            except KeyError as e:
                class_and_student_id = "0"
            try:
                course_id = valDict["course_id"]
            except KeyError as e:
                course_id = "0"
            try:
                class_id = valDict["class_id"]
            except KeyError as e:
                class_id = "0"
            try:
                stud_id = valDict["stud_id"]
            except KeyError as e:
                stud_id = "0"
            try:
                school_uid = valDict["school_uid"]
            except KeyError as e:
                school_uid = "0"
            try:
                student_uid = valDict["student_uid"]
            except KeyError as e:
                student_uid = "0"
            try:
                isdel = valDict["isdel"]
            except KeyError as e:
                isdel = "0"
            try:
                is_isdel = valDict["is_isdel"]
            except KeyError as e:
                is_isdel = "0"
            try:
                operation_type = valDict["operation_type"]
            except KeyError as e:
                operation_type = "0"
            try:
                execute_time = valDict["execute_time"]
            except KeyError as e:
                execute_time = "0"
            tempvalList = [class_and_student_id, course_id, class_id, stud_id, school_uid, student_uid, isdel, is_isdel,
                           operation_type, execute_time]
            totalList.append(tempvalList)


        totalListToStr = str(totalList).replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")").replace(
            " ", "")

        return totalListToStr

    eeo_course_class_header = "insert into ods_eeo_class_log (class_id,course_id,school_uid,class_number,class_name,is_class_name,teach_id,is_teach_id,cloud_folder," \
          "is_cloud_folder,skin_id,is_skin_id,seat_num,is_seat_num,class_type,is_class_type,main_st_id,is_main_st_id,ass_st_id,is_ass_st_id,class_btime," \
          "is_class_btime,class_etime,is_class_etime,is_is_auto_onstage,class_status,is_class_status,is_dc,is_is_dc,add_status,is_add_status,live_state," \
          "is_live_state,record_state,is_record_state,open_state,is_open_state,watch_by_login,is_watch_by_login,allow_unlogged_chat,is_allow_unlogged_chat," \
          "is_lock,is_is_lock,client_class_id,is_client_class_id,is_hd,addtime,update_time,operation_type) values"
    def eeo_course_class(valList):
        totalList = []
        for valDict in valList:
            try:
             class_id = valDict["class_id"]
            except KeyError as e:
            	class_id = 0
            try:
             course_id = valDict["course_id"]
            except KeyError as e:
            	course_id = 0
            try:
             school_uid = valDict["school_uid"]
            except KeyError as e:
            	school_uid = 0
            try:
             class_number = valDict["class_number"]
            except KeyError as e:
            	class_number = 0
            try:
             class_name = valDict["class_name"]
            except KeyError as e:
            	class_name = "NULL"
            try:
             is_class_name = valDict["is_class_name"]
            except KeyError as e:
            	is_class_name = 0
            try:
             teach_id = valDict["teach_id"]
            except KeyError as e:
            	teach_id = 0
            try:
                if len(valDict["is_teach_id"]) == 0:
                    is_teach_id = 0
                else:
                    is_teach_id = valDict["is_teach_id"]
            except KeyError as e:
            	is_teach_id = 0
            try:
             cloud_folder = valDict["cloud_folder"]
            except KeyError as e:
            	cloud_folder = "0"
            try:
             is_cloud_folder = valDict["is_cloud_folder"]
            except KeyError as e:
            	is_cloud_folder = "0"
            try:
             skin_id = valDict["skin_id"]
            except KeyError as e:
            	skin_id = "0"
            try:
             is_skin_id = valDict["is_skin_id"]
            except KeyError as e:
            	is_skin_id = "0"
            try:
             seat_num = valDict["seat_num"]
            except KeyError as e:
            	seat_num = "0"
            try:
             is_seat_num = valDict["is_seat_num"]
            except KeyError as e:
            	is_seat_num = "0"
            try:
             class_type = valDict["class_type"]
            except KeyError as e:
            	class_type = "0"
            try:
             is_class_type = valDict["is_class_type"]
            except KeyError as e:
            	is_class_type = "0"
            try:
             main_st_id = valDict["main_st_id"]
            except KeyError as e:
            	main_st_id = "0"
            try:
             is_main_st_id = valDict["is_main_st_id"]
            except KeyError as e:
            	is_main_st_id = "0"
            try:
             ass_st_id = valDict["ass_st_id"]
            except KeyError as e:
            	ass_st_id = "0"
            try:
             is_ass_st_id = valDict["is_ass_st_id"]
            except KeyError as e:
            	is_ass_st_id = "0"
            try:
             class_btime = valDict["class_btime"]
            except KeyError as e:
            	class_btime = "0"
            try:
             is_class_btime = valDict["is_class_btime"]
            except KeyError as e:
            	is_class_btime = "0"
            try:
             class_etime = valDict["class_etime"]
            except KeyError as e:
            	class_etime = "0"
            try:
             is_class_etime = valDict["is_class_etime"]
            except KeyError as e:
            	is_class_etime = "0"
            try:
             is_is_auto_onstage = valDict["is_is_auto_onstage"]
            except KeyError as e:
            	is_is_auto_onstage = "0"
            try:
             class_status = valDict["class_status"]
            except KeyError as e:
            	class_status = "0"
            try:
             is_class_status = valDict["is_class_status"]
            except KeyError as e:
            	is_class_status = "0"
            try:
             is_dc = valDict["is_dc"]
            except KeyError as e:
            	is_dc = "0"
            try:
             is_is_dc = valDict["is_is_dc"]
            except KeyError as e:
            	is_is_dc = "0"
            try:
             add_status = valDict["add_status"]
            except KeyError as e:
            	add_status = "0"
            try:
             is_add_status = valDict["is_add_status"]
            except KeyError as e:
            	is_add_status = "0"
            try:
             live_state = valDict["live_state"]
            except KeyError as e:
            	live_state = "0"
            try:
             is_live_state = valDict["is_live_state"]
            except KeyError as e:
            	is_live_state = "0"
            try:
             record_state = valDict["record_state"]
            except KeyError as e:
            	record_state = "0"
            try:
             is_record_state = valDict["is_record_state"]
            except KeyError as e:
            	is_record_state = "0"
            try:
             open_state = valDict["open_state"]
            except KeyError as e:
            	open_state = "0"
            try:
             is_open_state = valDict["is_open_state"]
            except KeyError as e:
            	is_open_state = "0"
            try:
             watch_by_login = valDict["watch_by_login"]
            except KeyError as e:
            	watch_by_login = "0"
            try:
             is_watch_by_login = valDict["is_watch_by_login"]
            except KeyError as e:
            	is_watch_by_login = "0"
            try:
             allow_unlogged_chat = valDict["allow_unlogged_chat"]
            except KeyError as e:
            	allow_unlogged_chat = "0"
            try:
             is_allow_unlogged_chat = valDict["is_allow_unlogged_chat"]
            except KeyError as e:
            	is_allow_unlogged_chat = "0"
            try:
             is_lock = valDict["is_lock"]
            except KeyError as e:
            	is_lock = 0
            try:
             is_is_lock = valDict["is_is_lock"]
            except KeyError as e:
            	is_is_lock = 0
            try:
             client_class_id = valDict["client_class_id"]
            except KeyError as e:
            	client_class_id = "0"
            try:
             is_client_class_id = valDict["is_client_class_id"]
            except KeyError as e:
            	is_client_class_id = 0
            try:
             is_hd = valDict["is_hd"]
            except KeyError as e:
            	is_hd = 0
            try:
             addtime = valDict["addtime"]
            except KeyError as e:
            	addtime = "0"
            try:
             update_time = valDict["update_time"]
            except KeyError as e:
            	update_time = "0"
            try:
             operation_type = valDict["operation_type"]
            except KeyError as e:
            	operation_type = 0
            tempvalList = [class_id,course_id,school_uid,class_number,class_name,is_class_name,teach_id,is_teach_id,cloud_folder,is_cloud_folder,skin_id,is_skin_id,seat_num,is_seat_num,class_type,is_class_type,main_st_id,is_main_st_id,ass_st_id,is_ass_st_id,class_btime,is_class_btime,class_etime,is_class_etime,is_is_auto_onstage,class_status,is_class_status,is_dc,is_is_dc,add_status,is_add_status,live_state,is_live_state,record_state,is_record_state,open_state,is_open_state,watch_by_login,is_watch_by_login,allow_unlogged_chat,is_allow_unlogged_chat,is_lock,is_is_lock,client_class_id,is_client_class_id,is_hd,addtime,update_time,operation_type]
            totalList.append(tempvalList)

        totalListToStr = str(totalList).replace("[[", "(").replace("]]", ")").replace("[", "(").replace("]", ")").replace(
            " ", "")

        return totalListToStr