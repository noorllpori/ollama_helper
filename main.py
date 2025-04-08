import libf
import dearpygui.dearpygui as dpg
import time
import asyncio
import requests
import json

ollama_init = libf.ollama_lib()
ollama_init._model_refresh = True

# while True:
#     od = input("#指令: ")
#     ollama_init.Order(od)

global model_chos
model_chos = 0

async def update_data():
    global model_chos
    while True:
        # print( "> update_data" )
        dpg.set_value('Model_list', ollama_init.ModeList_ShowTxt)
        max_ml = len( ollama_init.model_list )
        if model_chos > max_ml-1:
            model_chos = 0
        elif model_chos < 0:
            model_chos = max_ml-1
        if max_ml > 0:
            md:libf.ollama_model = ollama_init.model_list[model_chos]
            dpg.set_value('modelid', md.model_id)
            dpg.set_value('name', md.name)
            dpg.set_value('size', md.size)
            dpg.set_value('format', md.format)
            dpg.set_value('p_size', md.parameter_size)
            dpg.set_value('q_level', md.quantization_level)
            dpg.set_value('digest', md.digest)
            dpg.set_value('online', md.online)
            lef_t = ""
            if md.online:
                tt = -int(time.time() - md.expires_at_ts)
                lef_t = f"剩余释放时间: {str(tt)}s"
            dpg.set_value('lft', lef_t)
        await asyncio.sleep(1/40)
     
def switch_model(sender, app_data, user_data):
    global model_chos
    if sender == "+":
        model_chos += 1
    elif sender == "-":
        model_chos -= 1

# curl http://localhost:11434/api/generate -d "{\"model\": \"qwen2.5:1.5b\", \"keep_alive\": 0}"
def RunBackHot(sender):
    max_ml = len( ollama_init.model_list )
    if max_ml > 0:
        md:libf.ollama_model = ollama_init.model_list[model_chos]   
        url = f"{ollama_init._postApi}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": md.model_id, 
            "keep_alive": -1
        }
        rsp = requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers
        ).json()
        print(rsp)

def FreeHot(sender): 
    max_ml = len( ollama_init.model_list )
    if max_ml > 0:
        md:libf.ollama_model = ollama_init.model_list[model_chos]   
        url = f"{ollama_init._postApi}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": md.model_id, 
            "keep_alive": 0
        }
        rsp = requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers
        ).json()
        print(rsp)

dpg.create_context()

with dpg.font_registry():
    with dpg.font("Deng.ttf", 16) as font1:
          dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
          dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
          dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)

with dpg.window( width=500, height=270, tag="Main Window"):
    dpg.bind_font(font1)
    dpg.add_text("model list ...", tag='Model_list')
    dpg.add_text("")
    with dpg.group(horizontal=True): 
        dpg.add_button(label="<", callback=switch_model, tag="-")
        dpg.add_text("CModel: ")    
        dpg.add_input_text(tag="modelid", width=200, readonly=True)
        dpg.add_button(label=">", callback=switch_model, tag="+")
    with dpg.group(horizontal=True): 
        dpg.add_text("Name 名称: ")   
        dpg.add_input_text( tag="name", width=180, default_value="qwen2.5:0.5b", readonly=True)
        dpg.add_text("size 大小: ")   
        dpg.add_input_text(tag="size", width=80, default_value="30 mb", readonly=True)
    with dpg.group(horizontal=True): 
        dpg.add_text("format 格式: ")   
        dpg.add_input_text( tag="format", width=50, default_value="gguf", readonly=True)
        dpg.add_text("parameter size 参数量: ")   
        dpg.add_input_text( tag="p_size", width=80, default_value="30 M", readonly=True)
        # quantization_level
        dpg.add_text("quantization level 量化级别: ")   
        dpg.add_input_text( tag="q_level", width=70, default_value="Q4_K_M", readonly=True)
    with dpg.group(horizontal=True): 
        dpg.add_text("digest: ")   
        dpg.add_input_text( 
            tag="digest", 
            width=580, 
            default_value="a8b0c51577010a279d933d14c2a8ab4b268079d44c5c8830c0a93900f1827c67",
            readonly=True
        )
    with dpg.group(horizontal=True): 
        dpg.add_text("  ")   
        dpg.add_button(label="长期后台运行", callback=RunBackHot)
        dpg.add_button(label="后台释放", callback=FreeHot)
        dpg.add_text("    ")   
        dpg.add_text("在线状态: ") 
        dpg.add_checkbox( enabled=False, tag="online")
        dpg.add_text("剩余释放时间: 12s", tag="lft") 

# dpg.set_frame_callback(24, update_data)

dpg.create_viewport(title='Model List UI', width=900, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main Window", True)

async def main():
    asyncio.create_task(update_data())  # 启动异步任务
    while dpg.is_dearpygui_running():
        await asyncio.sleep(0.01)  # 非阻塞等待
        dpg.render_dearpygui_frame()  # 渲染 DPG 帧

asyncio.run(main())  # 运行事件循环

dpg.destroy_context()