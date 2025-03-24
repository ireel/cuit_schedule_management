# GUI.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from html_to_data import Converter  # 导入正确的类

class ScheduleImporter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("课表导入工具 v1.1")
        self.geometry("800x600")
        self.schedule_data = None
        self.current_file = None
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        # 顶部工具栏
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="导入HTML文件", command=self.import_html).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="手动输入", command=self.show_manual_input).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="保存JSON", command=self.save_json).pack(side=tk.RIGHT, padx=2)
        
        # 数据展示区域
        self.notebook = ttk.Notebook(self)
        
        # HTML解析预览
        self.html_frame = ttk.Frame(self.notebook)
        self.html_text = tk.Text(self.html_frame, wrap=tk.NONE)
        self.html_scroll = ttk.Scrollbar(self.html_frame, command=self.html_text.yview)
        self.html_text.configure(yscrollcommand=self.html_scroll.set)
        self.html_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.html_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 手动输入区域
        self.manual_frame = ttk.Frame(self.notebook)
        self.manual_text = tk.Text(self.manual_frame, wrap=tk.WORD)
        self.manual_text.insert(tk.END, '在此粘贴JSON数据...')
        self.manual_text.pack(fill=tk.BOTH, expand=True)
        
        self.notebook.add(self.html_frame, text="HTML解析预览")
        self.notebook.add(self.manual_frame, text="手动输入")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status = ttk.Label(self, text="就绪", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def import_html(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("HTML文件", "*.html")],
            title="选择课表HTML文件"
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 使用Converter类解析
                filename = os.path.splitext(os.path.basename(filepath))[0]
                converter = Converter(html_content, filename)
                self.schedule_data = converter.json  # 获取解析后的数据
                
                # 显示预览
                formatted = json.dumps(self.schedule_data, indent=2, ensure_ascii=False)
                self.html_text.delete(1.0, tk.END)
                self.html_text.insert(tk.END, formatted)
                self.current_file = filename
                self.status.config(text=f"成功导入: {filepath}")
                messagebox.showinfo("导入成功", "HTML文件解析完成！")
            except Exception as e:
                messagebox.showerror("解析错误", f"文件解析失败:\n{str(e)}")

    def show_manual_input(self):
        self.notebook.select(self.manual_frame)

    def validate_json(self):
        try:
            data = json.loads(self.manual_text.get(1.0, tk.END))
            required_fields = ['name', 'teacher', 'week', 'room', 'time']
            for day in data.values():
                for course in day:
                    if not all(field in course for field in required_fields):
                        raise ValueError("课程数据字段不完整")
            self.schedule_data = data
            return True
        except Exception as e:
            messagebox.showerror("数据错误", f"JSON格式错误:\n{str(e)}")
            return False

    def save_json(self):
        if not self.schedule_data:
            messagebox.showwarning("无数据", "请先导入或输入课表数据")
            return
            
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json")],
                initialfile=f"{self.current_file}.json" if self.current_file else None
            )
            if filepath:
                # 确保data目录存在
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.schedule_data, f, indent=2, ensure_ascii=False)
                self.status.config(text=f"已保存: {filepath}")
                messagebox.showinfo("保存成功", "课表数据保存完成！")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存过程中发生错误:\n{str(e)}")

if __name__ == "__main__":
    app = ScheduleImporter()
    app.mainloop()