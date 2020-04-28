from modules.ALGO.AlgoLogic import Algo
from modules.CORE.CoreLogic import Core
from modules.IO.IOLogic import IO
from modules.DOCX.DocxLogic import Docx
from modules.WEB.WebLogic import Web
from modules._interfaces.CommonLogic import CommonLogic


class ModuleManager:
    __names_to_modules = {
        'CORE' : Core,
        'IO'   : IO,
        'ALGO' : Algo,
        'DOCX' : Docx,
        'WEB'  : Web,
    }

    __loaded_modules = set()
    __default_modules = ['CORE']

    @staticmethod
    def get_registered_modules():
        return ModuleManager.__names_to_modules.keys()

    @staticmethod
    def get_loaded_modules():
        return ModuleManager.__names_to_modules.keys()

    @staticmethod
    def module_was_loaded(module_name):
        return module_name in ModuleManager.__loaded_modules

    @staticmethod
    def download_default_modules():
        for module_name in ModuleManager.__default_modules:
            ModuleManager.load_module(module_name)

    @staticmethod
    def load_module(module_name):
        module = ModuleManager.__names_to_modules[module_name]
        ModuleManager.__loaded_modules.add(module_name)

        for command in module.get_info():
            CommonLogic.add_command(*command)
