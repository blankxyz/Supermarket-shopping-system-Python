import sys
import pyodbc
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Shopsell(QWidget):
    """
    销售（sell）录入系统：
    模仿现实中超市的售货界面
    收货时只需要输入条形码及商品数量，系统自动计算总价并将详细信息显示在窗口中央的表格中
    每次销售商品种类及数量都不相同，在点结算之前所有信息都只是暂存于列表中，只有点击结算
    后才会将信息存储进售货表中
    结算时，信息存入数据库并且将其中一部分信息以TXT形式存储于文本文件中，此处模仿超市打印小票
    销售商品时时间应该精确到秒
    在点击确认结算时要先判断是否输入有预售卖的商品，如果没有弹出提示框
    """
    def __init__(self):
        super(Shopsell, self).__init__()
        self.initUI()
    #UI设计实现
    def initUI(self):
        self.setGeometry(60, 60, 1000, 600)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        label_sell_title = QLabel("售货录入")
        label_sell_title.setFont(QFont("华文行楷", 25))
        label_txm = QLabel("条形码")
        label_xssl = QLabel("销售数量")
        label_sell1 = QLabel("总计")
        label_sell2 = QLabel("应收")
        label_sell3 = QLabel("实收")
        label_sell4 = QLabel("找零")
        #定义多个list用来暂存预售货信息
        self.txm = []
        self.xssl = []
        self.spmc = []
        self.lsj = []
        self.xssj = []
        #定义条形码输入框，并设置只允许输入整数
        self.line_txm = QLineEdit()
        self.line_txm.setValidator(QIntValidator())
        #定义销售数量输入框并设置为只允许输入整数
        self.line_xssl = QLineEdit()
        self.line_xssl.setValidator(QIntValidator())
        #结算窗口
        self.line_sell1 = QLineEdit()
        self.line_sell2 = QLineEdit()
        self.line_sell3 = QLineEdit()
        self.line_sell4 = QLineEdit()
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        #实收框发生改变时
        self.line_sell3.textChanged.connect(self.jiesuan)
        self.line_sell3.selectionChanged.connect(self.jiesuan0)
        self.line_sell4.setText("0.0")
        self.line_sell1.setReadOnly(True)
        self.line_sell2.setReadOnly(True)
        self.line_sell4.setReadOnly(True)
        self.line_sell1.setFixedSize( 150, 20)
        self.line_sell2.setFixedSize( 150, 20)
        self.line_sell3.setFixedSize( 150, 20)
        self.line_sell4.setFixedSize( 150, 20)
        #录入按钮，绑定事件
        btn_sell_lr = QPushButton("录入")
        btn_sell_lr.clicked.connect(self.event_lr)
        #确认按钮，绑定事件 
        btn_sell_qr = QPushButton("确认")
        btn_sell_qr.clicked.connect(self.event_qr)
        #清零按钮，绑定事件
        btn_sell_ql = QPushButton("清零")
        btn_sell_ql.clicked.connect(self.event_ql)
        btn_sell_qr.setFixedSize( 150, 20)
        btn_sell_ql.setFixedSize( 150, 20)
        
        self.tabel_sell = QTableWidget()
        self.tabel_sell.setRowCount(20)
        self.tabel_sell.setColumnCount(6)
        self.tabel_sell.setHorizontalHeaderLabels(["条形码", "商品名称", "单价", "数量", "总计", "销售时间"])
        self.tabel_sell.setColumnWidth(5, 200)
        self.tabel_sell.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #布局
        layout = QVBoxLayout(self)
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        v2 = QVBoxLayout()
        h5 = QHBoxLayout()
        f = QFormLayout()
        w_title =QWidget()
        w_21 = QWidget()
        w_22 = QWidget()
        w_31 = QWidget()
        w_321 = QWidget()
        w_321.setFixedSize(235, 330)
        w_322 = QWidget()
        w_low = QWidget()
        v1.addWidget(label_sell_title,0,  Qt.AlignCenter)
        h1.addWidget(label_txm)
        h1.addWidget(self.line_txm)
        h1.addWidget(label_xssl)
        h1.addWidget(self.line_xssl)
        h2.addWidget(btn_sell_lr)
        h3.addWidget(self.tabel_sell)
        f.addRow(label_sell1, self.line_sell1)
        f.addRow(label_sell2, self.line_sell2)
        f.addRow(label_sell3, self.line_sell3)
        f.addRow(label_sell4, self.line_sell4)
        v2.addWidget(btn_sell_qr, Qt.AlignCenter|Qt.AlignVCenter)
        v2.addWidget(btn_sell_ql, Qt.AlignCenter|Qt.AlignVCenter)
        w_title.setLayout(v1)
        w_21.setLayout(h1)
        w_22.setLayout(h2)
        w_31.setLayout(h3)
        w_321.setLayout(f)
        w_322.setLayout(v2)
        w_low.setLayout(h5)
        splitter_sell1 = QSplitter(Qt.Horizontal)
        splitter_sell1.setSizes([800, 80])
        splitter_sell1.addWidget(w_title)
        splitter_sell2 = QSplitter(Qt.Horizontal)
        splitter_sell2.setSizes([150, 60])
        splitter_sell2.addWidget(w_22)
        splitter_sell3 = QSplitter(Qt.Horizontal)
        #splitter3.setSizes([800, 60])
        splitter_sell3.addWidget(w_21)
        splitter_sell3.addWidget(splitter_sell2)
        splitter_sell4 = QSplitter(Qt.Vertical)
        splitter_sell4.setSizes([800, 140])
        splitter_sell4.addWidget(splitter_sell1)
        splitter_sell4.addWidget(splitter_sell3)
        splitter_sell5 = QSplitter(Qt.Horizontal)
        splitter_sell5.setSizes([150, 60])
        splitter_sell5.addWidget(w_322)
        splitter_sell6 = QSplitter(Qt.Vertical)
        splitter_sell6.addWidget(w_321)
        splitter_sell6.addWidget(splitter_sell5)
        splitter_sell7 = QSplitter(Qt.Horizontal)
        splitter_sell7.setSizes([700, 390])
        splitter_sell7.addWidget(self.tabel_sell)
        splitter_sell8 = QSplitter(Qt.Horizontal)
        splitter_sell8.addWidget(splitter_sell7)
        splitter_sell8.addWidget(splitter_sell6)
        splitter_sell9 = QSplitter(Qt.Vertical)
        splitter_sell9.addWidget(splitter_sell4)
        splitter_sell9.addWidget(splitter_sell8)
        #splitter_sell9.addWidget(w_low)
        layout.addWidget(splitter_sell9)
        self.setLayout(layout)
        #临时变量
        self.Row = 0
        #l录入信息并暂存于表显示框中
    def event_lr(self):
        if self.line_txm.text !='':
            try:
                txm = int(self.line_txm.text())
            except:
                txm = 0
               # replay = QMessageBox.warning(self, "!", "请正确输入条形码！", QMessageBox.Yes)
        else:
            txm = 0
            replay = QMessageBox.warning(self, "!", "请正确输入条形码！", QMessageBox.Yes)
        if self.line_xssl.text() !='':
            xssl = int(self.line_xssl.text())
        else:
            xssl = -1
            #replay = QMessageBox.warning(self, "!", "请输入商品数量！", QMessageBox.Yes)
        conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
        cursor = conn.cursor()
        cursor.execute("select intxm from Inventory")
        row = cursor.fetchall()
        r = []
        for i in range(len(row)):
            r.append(row[i].intxm)
        if txm not in r:
            replay = QMessageBox.warning(self, "!", "商品不存在！", QMessageBox.Yes)
        else:
            #将欲销售的商品数量与库存相比，如果小于报出提醒
            cursor.execute("select kcl from Inventory where intxm=%d"%txm)
            row = cursor.fetchone()
            if xssl > row[0] or xssl == -1:
                 replay = QMessageBox.warning(self, "!", "销售数量超出库存量或未填入销售数量！", QMessageBox.Yes)
            else:
                try:
                    cursor.execute("select* from Inventory where intxm=%d"%txm)
                    rows = cursor.fetchone()
                    newItem1 = QTableWidgetItem(str(rows[0]))
                    newItem2 = QTableWidgetItem(rows[1])
                    newItem3 = QTableWidgetItem(str(rows[5]))
                    newItem4 = QTableWidgetItem(str(xssl))
                    newItem5 = QTableWidgetItem(str(float("%.1f"%(rows[5]*xssl))))
                    newItem6 = QTableWidgetItem(time.strftime("%Y-%m-%d %H:%M:%S"))
                    self.tabel_sell.setItem(self.Row, 0, newItem1)
                    self.tabel_sell.setItem(self.Row, 1, newItem2)
                    self.tabel_sell.setItem(self.Row, 2, newItem3)
                    self.tabel_sell.setItem(self.Row, 3, newItem4)
                    self.tabel_sell.setItem(self.Row, 4, newItem5)
                    self.tabel_sell.setItem(self.Row, 5, newItem6)
                    #计算总价
                    if self.line_sell1.text() != '':
                        self.line_sell1.setText(str(float("%.1f"%(float(self.line_sell1.text())+rows[5]*xssl))))
                    else:
                        self.line_sell1.setText(str(float("%.1f"%(rows[5]*xssl))))
                        
                    self.line_sell2.setText(self.line_sell1.text())
                    
                    self.txm.append(int(newItem1.text()))
                    self.spmc.append(newItem2.text())
                    self.lsj.append(float(newItem3.text()))
                    self.xssl.append(int(newItem4.text()))
                    self.xssj.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                    
                    #每次录入后自动对两个输入框进行清零
                    self.line_txm.setText("")
                    self.line_xssl.setText("")
                    self.Row +=1
                    
                except UnboundLocalError:
                    replay = QMessageBox.warning(self, "!", "发生UnboundLocalError问题！", QMessageBox.Yes)
                except ValueError:
                    replay = QMessageBox.warning(self, "!", "发生ValueError问题！", QMessageBox.Yes)
        conn.close()
        
        #结算
    def jiesuan(self):
        try:
            self.line_sell4.setText(str(float("%.1f"%((float(self.line_sell3.text())-float(self.line_sell2.text()))))))
        except ValueError:
            pass
    def jiesuan0(self):
        self.line_sell3.setText("")
    #确认录入存表
    def event_qr(self):
        #确定是否添加有商品
        if self.line_sell1.text() == "0.0":
            replay = QMessageBox.warning(self, "!", "未添加商品！", QMessageBox.Yes)
        else:
            #录入数据库的同时将收货信息存入txt文件中，模仿打印小票
            xsjl = open("销售记录.txt", "a+")
            xsjl.write("*******************************************************************\n")
            xsjl.write("商品名称\t\t\t\t          单价  数量    总计\n")
            xsjl.write("\n")
            conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
            cursor = conn.cursor()
            l = len(self.txm)
            for i in range(l):
                xsjl.write(self.spmc[i])
                xsjl.write("%.1f\t%d\t%.1f\n"%(self.lsj[i], self.xssl[i], self.xssl[i]*self.lsj[i]))
                cursor.execute("insert into Sellgoods values(%d,%d,%f,%r)"%(self.txm[i], self.xssl[i], self.lsj[i], self.xssj[i]))
                cursor.execute("select kcl from Inventory where intxm=%d"%self.txm[i])
                row = cursor.fetchone()
                cursor.execute("update Inventory set kcl=%d where intxm = %d"%(row[0]-self.xssl[i], self.txm[i]))
            conn.commit()
            conn.close()
            xsjl.write("___________________________________________________________________\n")
            xsjl.write("总计：%.1f\n"%float(self.line_sell1.text()))
            xsjl.write("实收：%.1f\n"%float(self.line_sell3.text()))
            xsjl.write("找零：%.1f\n"%float(self.line_sell4.text()))
            xsjl.write("\n"+time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
            xsjl.write("*******************************************************************\n")
            xsjl.close()
            self.event_ql()
        #清空表格
    def event_ql(self):
        #清空输入框，清除显示列表，清空暂存信息的列表
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        self.line_sell4.setText("0.0")
        self.Row = 0
        for i in range(len(self.txm)):
            for j in range(6):
                newItem = QTableWidgetItem("")
                self.tabel_sell.setItem(i, j, newItem)
                
        self.txm = []
        self.xssj = []
        self.xssl = []
        self.spmc = []
        self.lsj = []
        
        #添加背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("select.jpg")
        painter.drawPixmap(self.rect(), pixmap)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopsell()
    sell.show()
    sys.exit(app.exec())
        
