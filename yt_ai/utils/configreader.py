import json
import importlib
import os
from yt_ai.utils.logger import logger
from yt_ai.utils.datareader import read_data_csv

class Config:
    def __init__(self, configFile):
        self.configFile = configFile
        logger.info(f"Reading Config file from {configFile}")
        with open(self.configFile, "r") as f:
            self.config = json.load(f)
        
        logger.debug(f"Setting cache folder : {self.config['cache']}")
        os.environ['HF_DATASETS_CACHE']=self.config["cache"]
        if self.config_file["use_cpu"]:
            os.environ["CUDA_VISIBLE_DEVICES"] = ""
            os.environ["SUNO_OFFLOAD_CPU"] = "True"
            os.environ["SUNO_USE_SMALL_MODELS"] = "True"
        
        
        self.data = read_data_csv(self.config["dataFile"])
        self.ttsDict = {}
        self.ttvDict = {}
        self._decode_tts()
        self._decode_ttv()
        
    def _decode_tts(self):
        for model in self.config["tts"]:
            logger.info(f"Loading tts model: {model}")
            # lazy loading
            module = importlib.import_module(f'yt_ai.tts.{model}')
            self.ttsDict[model] = getattr(module, f"{model}")(self.config)
            # self.ttsDict[model] = self.ttsDict[model]

    def _decode_ttv(self):
         for model in self.config["ttv"]:
            logger.info(f"Loading ttv model: {model}")
             # lazy loading
            module = importlib.import_module(f'yt_ai.ttv.{model}')
            self.ttvDict[model] = getattr(module, f"{model}")(self.config)
            
    def get_tts_dict(self):
        return self.ttsDict
    
    def get_ttv_dict(self):
        return self.ttvDict
    
    def get_config_path(self):
        return self.config
    