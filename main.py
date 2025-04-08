import libf
import dearpygui.dearpygui as dpg
import time
# curl http://localhost:11434/api/generate -d "{\"model\": \"qwen2.5:1.5b\", \"keep_alive\": 0}"

ollama_init = libf.ollama_lib()
ollama_init._model_refresh = True

# while True:
#     od = input("#指令: ")
#     ollama_init.Order(od)

def update_data():
    while True:
        dpg.set_value('Model_list', ollama_init.ModeList_ShowTxt)
        time.sleep(0.1)
        
dpg.create_context()
with dpg.window( width=500, height=270, tag="Main Window"):
    dpg.add_text("model list ...", tag='Model_list')

dpg.set_frame_callback(24, update_data)

dpg.create_viewport(title='Model List UI', width=900, height=270)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main Window", True)
dpg.start_dearpygui()

# 清理
dpg.destroy_context()