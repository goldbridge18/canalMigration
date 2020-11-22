import re
import json,os,sys
from collections  import abc


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




print("=========================================================")
# dict_l = {}



str0001 = {"Name":"inoutEnd","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791381}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795486}]]},{"Name":"Identity","Value":1}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792932}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794948}]]},{"Name":"Identity","Value":1}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796315}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796448}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796867}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796873}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797147}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797154}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797158}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797174}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797184}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797360}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797365}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797384}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599804977}]]},{"Name":"Identity","Value":194}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791363}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599792629}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792637}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794161}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794187}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794802}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794808}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794964}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794987}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795058}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795089}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795093}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795112}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795288}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795297}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795301}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795324}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795408}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795730}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795758}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796516}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797149}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797156}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797263}]]},{"Name":"Identity","Value":3}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791560}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791985}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792086}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796166}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796197}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796202}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796684}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599805330}]]},{"Name":"Identity","Value":1}]}]}


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

def detailsHandle_test(string,filed):
    # count = 0
    total_r = []
    if filed == "Details":
        for i in [x for x in range(len(string)) if x%2 == 0]:
            tmp_list = []
            tmp_dict = {}
            for value in string[i]:
                # tmp_dict[value["Name"]+"_in_"+str(count)] = value["Value"]
                tmp_dict[value["Name"]+"_in"] = value["Value"]
            for value in string[i+1]:
                # tmp_dict[value["Name"]+"_out_"+str(count)] = value["Value"]
                tmp_dict[value["Name"]+"_out"] = value["Value"]
            # count += 1
            # print(tmp_dict)
            total_r.append(tmp_dict)
    elif filed == "Persons":
        tmp_list = [{x["Name"]:v}  for x in string  for v in  x["Value"] ]
        total_r = [{k:{v["Name"]:v["Value"]}} for val in tmp_list  for k,v in val.items()]
    return  total_r

#key 是inoutEnd、stageEnd\handsupEnd....
def getDataToCover(string):
    total_dict = {}
    dict_l = {}
    for val in string["Value"]:
        tmp_dict = {}
        if isinstance(val["Value"], abc.Sequence) and   val["Name"] == "Persons":
             tmp_dict["Persons"] = detailsHandle_test(val["Value"],"Persons")
        elif isinstance(val["Value"], abc.Sequence) and len(val["Value"]) == 0:
            dict_l[val["Name"]] = ""
        elif isinstance(val["Value"], abc.Sequence) and isinstance(val["Value"][0],abc.Mapping):
            dict_l[val["Name"]] = val["Value"]
            # print("----------->",val)
            for val01 in val["Value"]:
                if val01["Name"] == "Details":
                    # tmp_dict["Details"] = detailsHandle(val01["Value"])
                     tmp_dict["Details"] = detailsHandle_test(val01["Value"],"Details")
                elif val01["Name"] == "Persons":
                    # detailsHandle_test(string,filed)
                    tmp_dict["Persons"] = detailsHandle_test(val01["Value"],"Persons")
                else:
                    tmp_dict[val01["Name"]] = val01["Value"]
        else:
            # tmp_dict[val["Name"]] = val["Value"]
            dict_l[val["Name"]] = val["Value"]
        if len(tmp_dict) == 0:
            pass
        else:
            dict_l[val["Name"]] = tmp_dict

    total_dict[string["Name"]] = dict_l

    return  total_dict


# print(getInoutEndData(str0001))

str002 = {"Name":"textboardEnd","Value":[{"Name":"Count","Value":3},{"Name":"Total","Value":10865},{"Name":"Period","Value":[2583,318,7964]},{"Name":"DCount","Value":15}]}
# print(getDataToCover(str002))
str002 ={"ts":6871111718345375747,"v":2,"op":"i","ns":"hamster.ClassSummary44","o":[{"Name":"_id","Value":"5f5b17b4b3b74f73b7a3244e"},{"Name":"ActionTime","Value":1599805364},{"Name":"CID","Value":3605755},{"Name":"CourseID","Value":1742029},{"Name":"Cmd","Value":"End"},{"Name":"CloseTime","Value":1599805274},{"Name":"StartTime","Value":1599791474},{"Name":"SID","Value":1335588},{"Name":"Data","Value":[{"Name":"stageEnd","Value":[{"Name":"1338366","Value":[{"Name":"DownCount","Value":114},{"Name":"DownTotal","Value":1513},{"Name":"UpCount","Value":114},{"Name":"UpTotal","Value":3710}]},{"Name":"1334360","Value":[{"Name":"DownCount","Value":5},{"Name":"DownTotal","Value":4730},{"Name":"UpCount","Value":2},{"Name":"UpTotal","Value":1992}]},{"Name":"1334356","Value":[{"Name":"DownCount","Value":204},{"Name":"DownTotal","Value":2552},{"Name":"UpCount","Value":205},{"Name":"UpTotal","Value":1553}]},{"Name":"1334362","Value":[{"Name":"DownCount","Value":83},{"Name":"DownTotal","Value":1233},{"Name":"UpCount","Value":83},{"Name":"UpTotal","Value":783}]},{"Name":"1325910","Value":[{"Name":"DownCount","Value":7},{"Name":"UpTotal","Value":0},{"Name":"UpCount","Value":0},{"Name":"DownTotal","Value":7947}]},{"Name":"1335588","Value":[{"Name":"DownCount","Value":0},{"Name":"UpTotal","Value":4668},{"Name":"UpCount","Value":12},{"Name":"DownTotal","Value":0}]},{"Name":"1325888","Value":[{"Name":"DownCount","Value":81},{"Name":"DownTotal","Value":12262},{"Name":"UpCount","Value":82},{"Name":"UpTotal","Value":894}]}]},{"Name":"handsupEnd","Value":[{"Name":"1334356","Value":[{"Name":"CTime","Value":3},{"Name":"Total","Value":1}]},{"Name":"1334362","Value":[{"Name":"CTime","Value":7},{"Name":"Total","Value":2}]},{"Name":"1325888","Value":[{"Name":"CTime","Value":62},{"Name":"Total","Value":17}]}]},{"Name":"textboardEnd","Value":[{"Name":"Count","Value":3},{"Name":"Total","Value":10865},{"Name":"Period","Value":[2583,318,7964]},{"Name":"DCount","Value":15}]},{"Name":"smallboardEnd","Value":[{"Name":"Count","Value":3},{"Name":"Total","Value":10908},{"Name":"Period","Value":[2594,343,7971]},{"Name":"DCount","Value":9}]},{"Name":"authorizeEnd","Value":[{"Name":"1338366","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1334360","Value":[{"Name":"Count","Value":5},{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1334362","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1325910","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1325888","Value":[{"Name":"Count","Value":0},{"Name":"Total","Value":0}]},{"Name":"1335588","Value":[{"Name":"Count","Value":12},{"Name":"Total","Value":4668}]}]},{"Name":"inoutEnd","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599793107}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796027}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796789}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599799092}]]},{"Name":"Identity","Value":1}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791537}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791574}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791666}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792142}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796619}],[{"Name":"Device","Value":2},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796621}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796696}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796814}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599798742}]]},{"Name":"Identity","Value":4}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791381}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795486}]]},{"Name":"Identity","Value":1}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792932}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794948}]]},{"Name":"Identity","Value":1}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796315}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796448}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796867}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796873}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797147}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797154}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797158}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797174}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797184}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797360}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797365}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797384}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797387}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599804977}]]},{"Name":"Identity","Value":194}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791363}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599792629}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792637}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794161}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794187}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794802}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794808}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599794964}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599794987}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795058}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795089}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795093}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795112}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795288}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795297}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795301}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795324}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795408}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599795730}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599795758}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796516}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797149}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599797156}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599797263}]]},{"Name":"Identity","Value":3}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156},{"Name":"Details","Value":[[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599791560}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599791985}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599792086}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796166}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796197}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599796202}],[{"Name":"Device","Value":0},{"Name":"Type","Value":"In"},{"Name":"Time","Value":1599796684}],[{"Name":"Type","Value":"Out"},{"Name":"Time","Value":1599805330}]]},{"Name":"Identity","Value":1}]}]},{"Name":"muteEnd","Value":[{"Name":"Persons","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668}]}]},{"Name":"MuteAll","Value":[]}]},{"Name":"silenceEnd","Value":[{"Name":"SilenceAll","Value":[]},{"Name":"Persons","Value":[{"Name":"1338366","Value":[{"Name":"Total","Value":5223}]},{"Name":"1334360","Value":[{"Name":"Total","Value":6722}]},{"Name":"1334356","Value":[{"Name":"Total","Value":4105}]},{"Name":"1334362","Value":[{"Name":"Total","Value":2016}]},{"Name":"1325910","Value":[{"Name":"Total","Value":7947}]},{"Name":"1325888","Value":[{"Name":"Total","Value":13156}]},{"Name":"1335588","Value":[{"Name":"Total","Value":4668}]}]}]}]}],"o2":0}
# getStageEndData(str002)
# print(str002["o"])

for val in str002["o"]:
    if val["Name"] == "Data":
        for i in val["Value"]:
            print("------start----------------------")
            print(getDataToCover(i))


print("-------------------------------------------------------------------------------------")

str003 = {'Name': 'muteEnd', 'Value': [{'Name': 'Persons', 'Value': [{'Name': '1338366', 'Value': [{'Name': 'Total', 'Value': 5223}]}, {'Name': '1334360', 'Value': [{'Name': 'Total', 'Value': 6722}]}, {'Name': '1334356', 'Value': [{'Name': 'Total', 'Value': 4105}]}, {'Name': '1334362', 'Value': [{'Name': 'Total', 'Value': 2016}]}, {'Name': '1325910', 'Value': [{'Name': 'Total', 'Value': 7947}]}, {'Name': '1325888', 'Value': [{'Name': 'Total', 'Value': 13156}]}, {'Name': '1335588', 'Value': [{'Name': 'Total', 'Value': 4668}]}]}, {'Name': 'MuteAll', 'Value': []}]}

# print(getDataToCover(str003))

# str004 = {'Name': 'Persons', 'Value': [{'Name': '1338366', 'Value': [{'Name': 'Total', 'Value': 5223}]}, {'Name': '1334360', 'Value': [{'Name': 'Total', 'Value': 6722}]}, {'Name': '1334356', 'Value': [{'Name': 'Total', 'Value': 4105}]}, {'Name': '1334362', 'Value': [{'Name': 'Total', 'Value': 2016}]}, {'Name': '1325910', 'Value': [{'Name': 'Total', 'Value': 7947}]}, {'Name': '1325888', 'Value': [{'Name': 'Total', 'Value': 13156}]}, {'Name': '1335588', 'Value': [{'Name': 'Total', 'Value': 4668}]}]}

# tmp_list = [{x["Name"]:v}  for x in str004["Value"] for v in  x["Value"] ]
# print([{k:{v["Name"]:v["Value"]}} for val in tmp_list  for k,v in val.items()])