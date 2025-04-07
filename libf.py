
import json
import requests
import dearpygui.dearpygui as dpg
import threading
import time

class ollama_lib:
    def __init__(self, JsonPath=None):
        self.fps = 30

        self.host="http://127.0.0.1"
        self.port=11434
        
        if JsonPath:
            self.settingJsonPath=JsonPath
        else:
            self.settingJsonPath="./setting.json"
        self.get_setting()

        self._postApi = self.zh_api()
        
        self.model_list:list[ollama_model] = []
        self.ModelUi_Thread:threading.Thread = None

        self.Main_Thread:threading.Thread = threading.Thread(target=self.MainThread, daemon=True, name="Ollama Main Thread...")
        self.Main_Thread.start()
        self._model_refresh:bool = False

    def MainThread(self):
        while True:
            if self.ModelUi_Thread:
                if not self.ModelUi_Thread.is_alive():
                    self._model_refresh = False
                    self.ModelUi_Thread = None
            if self._model_refresh:
                # b, txt = self.get_models()
                # dpg.set_value("_ModelList", txt) 
                pass
            time.sleep( 1/self.fps )

    def zh_api(self):
        api = self.host + ":" + str(self.port)
        return api

    def get_setting(self):
        with open(self.settingJsonPath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # get Host port
        self.host = data['host']
        self.port = data['port']
        self.fps = data['fps']
        # print(data)

    def get_models(self,CmdLog=False):
        # 获取所有的模型列表
        url = self._postApi + "/api/tags"
        response = requests.get(url).json()
        # 获取运行中模型列表
        ps_model:dict = {}
        url = self._postApi + "/api/ps"
        OnlineModels = requests.get(url).json()

        for rjs in OnlineModels['models']:
            ps_model[ rjs['model'] ] = {
                "name":rjs['name'],
                "expires_at":rjs['expires_at'],
                "size_vram":rjs['size_vram']
            }
        # 更新 self.model_list
        self.model_list.clear()
        for tjs in response['models']:
            # print(type(tjs))
            om = ollama_model(tjs)
            self.model_list.append(om)
            if om.model_id in ps_model:
                om.online = True
                om.expires_at = ps_model[om.model_id]['expires_at']
        if CmdLog:
            model_txt = "Model List"
            for md in self.model_list:
                onlineMode = "***"
                if md.online:
                    onlineMode = "Online"
                line = f"\n#   {md.name}  -  {md.size} : {md.quantization_level}  -  {md.format} : {md.quantization_level}  ->  {onlineMode} {md.expires_at}"
                model_txt += line
            print( model_txt )
        return True, model_txt

    # def Run_UI_thread(self, _target):
    #     _Thread:threading.Thread = threading.Thread(target=self.MainThread, daemon=True)
    #     pass

    def Order(self,order=""):
        help_txt = """
        Order Helper:
            help            <h>     获取帮助
            model           <m>     显示模型列表
            model_run       <mr>    模型列表添加到循环获取中
        """
        if order == "": order="help"
        if order == "help" or order == "h":
            print(help_txt)
        elif order == "model" or order == "m":
            self.get_models(CmdLog=True)
        elif order == "model_run" or order == "mr":
            if not self.ModelUi_Thread:
                self._model_refresh = True
                self.ModelUi_Thread = threading.Thread(target=self._thread_ModelList_UI, daemon=True)
                self.ModelUi_Thread.start()
        else:
            print("""
            --未知指令--
            """)

class ollama_model:
    def __init__(self,loadDict:dict):
        ## api获取基础信息
        self.model_id = ""
        self.name = ""
        self.size = ""
        self.format = ""
        self.parameter_size = ""
        self.quantization_level = ""
        ## cmd show获取详细信息
        # modelfile
        self.ModelfileTxt=""
        ## 是否在热加载中
        self.online = False
        self.expires_at:str = ""

        if loadDict:
            self.model_id = loadDict['model']
            self.name = loadDict['name']
            self.size = self.convert_size(loadDict['size']) 
            self.format = loadDict['details']['format']
            self.parameter_size = loadDict['details']['parameter_size']
            self.quantization_level = loadDict['details']['quantization_level']

    def loadJson(self):
        pass

    @staticmethod
    def convert_size(size_bytes: int) -> str:
        """
        将文件大小(字节)自适应转换为最适合的单位
        
        参数:
            size_bytes (int): 文件大小(字节)
            
        返回:
            str: 转换后的带单位字符串，保留2位小数
        """
        if size_bytes == 0:
            return "0B"
        
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        unit_index = 0
        
        while size_bytes >= 1024 and unit_index < len(units) - 1:
            size_bytes /= 1024
            unit_index += 1
        
        return f"{size_bytes:.2f} {units[unit_index]}"