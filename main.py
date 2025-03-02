import setting
import json


def load_data(filename):
    with open(f"{setting.path}data/{filename}", "r", encoding="utf-8") as json_file:
    #with open(f"data/{filename}", "r", encoding="utf-8") as json_file:
        loaded_data = json.load(json_file)
    
    return loaded_data

def find_lesson(loaded_data, week, day):
    keys_list = list(loaded_data.keys())
    all_lesson_list = loaded_data[keys_list[day-1]]
    now_lesson_list = []
    for lesson in all_lesson_list:
        # 判断单双周
        if week % lesson['week'][2] != 0:
            continue
        # 判断是否在范围内
        if week >= lesson['week'][0] and week <= lesson['week'][1]:
            now_lesson_list.append(lesson)

    return now_lesson_list

def make_message(lesson_list):
    text = ''
    for lesson in lesson_list:
        l_time = str(lesson['time']).replace("[","").replace("]","")
        text += f"【第{l_time}节】\n{lesson['name']}\n"
        text += f"教室：{lesson['room']}\n"
        text += f"老师：{lesson['teacher']}\n\n"

    return text

if __name__ == "__main__":
    loaded_data = load_data("example.json")
    week = int(input("要查询的周次:"))
    day = int(input("要查询星期几:"))
    lesson_list = find_lesson(loaded_data,week,day)
    print(make_message(lesson_list))
