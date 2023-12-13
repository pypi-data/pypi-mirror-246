import os
import sys
from pathlib import Path
from PySide2.QtWidgets import QApplication

from pytessng.DLLs.Tessng import TessngFactory
from pytessng.Tessng.MyPlugin import MyPlugin


class MyTessngApp:
    def __init__(self, ):
        self.app = QApplication()
        self.workspace = os.path.join(os.fspath(Path(__file__).resolve().parent), "WorkSpace")
        self.config = {
            '__workspace': self.workspace, # 工作空间
            '__simuafterload': False, # 加载路网后是否自动启动仿真
            '__custsimubysteps': False,
            '__allowspopup': False, # 禁止弹窗
            '__cacheid': True, # 快速创建路段
        }
        self.plugin = MyPlugin()
        self.factory = TessngFactory()
        self.tessng = self.factory.build(self.plugin, self.config)

        self.run()

    def run(self, ):
        if self.tessng is not None:
            sys.exit(self.app.exec_())
        else:
            sys.exit()

