from bs4 import BeautifulSoup
import os
import setting
import json

class Converter():
    def __init__(self, html_content, file_name):
        self.filename = file_name
        self.soup = BeautifulSoup(html_content, "lxml")
        self.tr_list = []
        self.load_model()
        self.keys_list = list(self.json.keys())
        self.load_tr()
        self.analyse_data()
        self.save_data()
        
    def load_model(self):
        with open(f"{setting.path}data/model.json", "r", encoding="utf-8") as json_file:
            loaded_data = json.load(json_file)
        self.json = loaded_data

    def load_tr(self):
        self.tr_list = self.soup.find_all(name='tr')

    def load_td(self,tr):
        self.td_list = tr.find_all(name="td")
    
    def analyse_data(self):
        for class_time in self.tr_list:
            self.load_td(class_time)
            day = 0
            for td in self.td_list:
                data_list = self.parse_td(td)
                if data_list:
                    for data in data_list:
                        self.json[self.keys_list[day-1]].append(data)

                day += 1
            print("-"*15)

        print(self.json)

    def parse_td(self, td):
        # 提取 title 属性并分割字段
        if not td.get("title"):
            return
        title = td.get("title").strip()
        parts = [p.strip() for p in title.split(";")]
        print(parts)
        data_list = []
        parts = [part for part in parts if part]
        print(parts)
        for i in range(0, len(parts), 4):
            # 解析基础字段
            data = {
                "name": parts[i].split("：")[0].strip(),
                "teacher": parts[i+1].split("：")[1].strip(),
                "room": parts[i+3].split("：")[1].strip(),
            }
            
            # 解析周次
            week_str = parts[i+2].split("：")[1].strip("周").strip()
            if "-" not in week_str:
                week_str += "-" + week_str
            if "双" in week_str:
                start_week, end_week = map(int, week_str.strip("双").split("-"))
                data["week"] = [start_week, end_week, 2]
            else:
                print(week_str)
                start_week, end_week = map(int, week_str.split("-"))
                data["week"] = [start_week, end_week, 1]
            
            # 推断时间（基于 rowspan）
            rowspan = int(td.get("rowspan", 1))
            start_time = 1  # 需根据实际表格结构调整起始节次
            end_time = start_time + rowspan - 1
            data["time"] = [start_time, end_time]

            data_list.append(data)
        
        return data_list
    
    def save_data(self):
        with open(f"data/" + self.filename + ".json", "w", encoding="utf-8") as json_file:
            json_file.write(json.dumps(self.json,ensure_ascii=False))


def load_html_files():
    html_dict = {}
    #for root, _, files in os.walk(setting.path + "raw_data"):
    for root, _, files in os.walk("raw_data"):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as file:
                    html_content = file.read()
                    html_dict[str(file.name).strip(".html").split("\\")[1]] = html_content

    return html_dict

dict1 = load_html_files()
for key in dict1:
    a = Converter(dict1[key], key)



