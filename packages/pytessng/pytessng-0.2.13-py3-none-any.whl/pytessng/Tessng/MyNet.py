from pytessng.DLLs.Tessng import PyCustomerNet, tessngIFace
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from functools import partial


class MyNet(PyCustomerNet):
    def __init__(self):
        super(MyNet, self).__init__()

    def afterLoadNet(self):
        iface = tessngIFace()
        netiface = iface.netInterface()


        # info = netiface.netAttrs().otherAttrs()
        # print(info)
    #
    # # 鼠标点击
    # def afterViewMousePressEvent(self, event):
    #     # 如果是右击
    #     if event.button() == Qt.RightButton:
    #         iface = tessngIFace()
    #         netiface = iface.netInterface()
    #         netiface.buildNetGrid(1)
    #         # 在TESSNG中的坐标
    #         pos = netiface.graphicsView().mapToScene(event.pos())
    #         locations = netiface.locateOnCrid(pos, 1)
    #         linkIds = []
    #         for location in locations:
    #             try:
    #                 print(location.point)
    #                 lane = location.pLaneObject
    #                 linkId = lane.link().id()
    #                 linkIds.append(linkId)
    #             except:
    #                 pass
    #         linkIds = sorted(set(linkIds))
    #         print(linkIds)
    #
    #         win = iface.guiInterface().mainWindow()
    #         self.context_menu = QMenu(win)
    #         # 在菜单中添加动作
    #         for i in linkIds:
    #             action = QAction(f"打断路段{i}", win)
    #             action.triggered.connect(partial(self.split_link, i, pos))
    #             self.context_menu.addAction(action)
    #
    #         # 设置右击事件
    #         win.setContextMenuPolicy(Qt.CustomContextMenu)
    #         win.customContextMenuRequested.connect(self.show_context_menu)
    #
    # # 在鼠标位置显示菜单
    # def show_context_menu(self, event):
    #     iface = tessngIFace()
    #     win = iface.guiInterface().mainWindow()
    #     self.context_menu.exec_(win.mapToGlobal(event))
    #
    # def split_link(self, link_id, pos):
    #     from pytessng.Toolbox.link_processing import link_processing
    #     iface = tessngIFace()
    #     netiface = iface.netInterface()
    #     x = pos.x()
    #     y = pos.y()
    #     print(link_id, x, y)
    #     input_info = f"{link_id},{x},{y}"
    #
    #     state, message = link_processing.splitLink(netiface, input_info)
    #     print(state, message)