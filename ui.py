import dearpygui.dearpygui as dpg
import libf

def button_callback(sender, app_data, user_data):
    input_text = dpg.get_value("input_text")
    print(f"按钮被点击！输入的内容是: {input_text}")
    dpg.set_value("output_text", f"shu ru: {input_text}")

def clear_input():
    dpg.set_value("input_text", "")
    dpg.set_value("output_text", "")

dpg.create_context()
dpg.create_viewport(title='ollama Controller', width=600, height=400)

with dpg.window(label="Main", width=580, height=380):
    # 添加文本标签
    dpg.add_text("Ollama Info")
    
    # 添加输入文本框
    dpg.add_input_text(label="输入内容", tag="input_text", width=200)
    
    # 添加按钮
    with dpg.group(horizontal=True):
        dpg.add_button(label="Update", callback=button_callback)
        dpg.add_button(label="Clear", callback=clear_input)
    
    # 添加分隔线
    dpg.add_separator()
    
    # 添加输出文本
    dpg.add_text("Info Show here:", tag="output_text")
    
    # 添加多行文本框
    dpg.add_input_text(label="duo hang shu ru", multiline=True, height=100, width=300, tag="multi_input")
    
    # 添加另一个按钮
    dpg.add_button(label="duo hang nei rong", callback=lambda: print(dpg.get_value("multi_input")))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()