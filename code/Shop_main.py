import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Shop_stock import *
from Shop_sell import *
from Shop_select import *
class Shopmain(QWidget):
    """
    成功登录后的主窗口：Shop_main
    窗口设置title："超市信息管理系统",放置三个按钮："进货录入"、"售货录入"、"信息查询"
    添加一个显示标签：关于本系统
    三个按钮分别连接三个类，点击则实例化
    显示标签按照常理应当连接到网页用以详细介绍系统，此程序选择不使用，直接pass掉
    """
    def __init__(self, parent=None):
        super(Shopmain, self).__init__(parent)
        self.initUI()
        #UI窗口设计
    def initUI(self):
        self.resize(1366,768)
        #self.setGeometry(50, 50, 800, 600)
        #标题
        self.setWindowTitle("超市信息管理系统")
        #三个子系统选择按钮，绑定信号事件
        btn_main_stock = QPushButton("进货录入")
        btn_main_stock.setStyleSheet("background-color :rgb(253,216,174)")
        btn_main_stock.setFixedSize(200, 45)
        btn_main_stock.clicked.connect(self.stock)
        btn_main_sell= QPushButton("售货录入")
        btn_main_sell.setFixedSize(200, 45)
        btn_main_sell.setStyleSheet("background-color :rgb(253,216,174)")
        btn_main_sell.clicked.connect(self.sell)
        btn_main_select = QPushButton("信息查询")
        btn_main_select.setStyleSheet("background-color :rgb(253,216,174)")
        btn_main_select.setFixedSize(200, 45)
        btn_main_select.clicked.connect(self.select)
        #title
        label_main_title = QLabel("欢迎使用文创超市信息管理系统")
        label_main_title.setFont(QFont("华文行楷", 25))
        label_main_title.setStyleSheet('''color: rgb(200,10,100);''')
        label_main_explain = QLabel(self)
        label_main_explain.setText("<a href = '#'>关于本系统</a>")
        label_main_explain.linkActivated.connect(self.explain)
        labe_null1 = QLabel()
        labe_null2 = QLabel()
        #布局设计
        layout = QVBoxLayout(self)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        g1 = QGridLayout()
        g2 = QGridLayout()
        g3 = QGridLayout()
        h1.addWidget(label_main_title, 0, Qt.AlignCenter)
        g1.addWidget(labe_null1)
        g2.addWidget(btn_main_stock, 1, 0)
        g2.addWidget(btn_main_sell, 2, 0)
        g2.addWidget(btn_main_select, 3, 0)
        g3.addWidget(labe_null2)
        h2.addLayout(g1)
        h2.addLayout(g2)
        h2.addLayout(g3)
        h3.addWidget(label_main_explain, 0, Qt.AlignLeft|Qt.AlignBottom)
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)
    def explain(self):
        pass
    #Stock实例化
    def stock(self):
        self.stock = Shopstock()
        self.stock.show()
    #Sell实例化
    def sell(self):
        self.sell = Shopsell()
        self.sell.show()
    #Select实例化
    def select(self):
        self.select = Shopselect()
        self.select.show()
    #设置背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("main.jpg")
        painter.drawPixmap(self.rect(), pixmap)
if __name__ == "__main__":
    app =QApplication(sys.argv)
    shop = Shopmain()
    shop.show()
    sys.exit(app.exec())
