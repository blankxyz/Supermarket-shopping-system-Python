import sys
import pyodbc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class Shopselect(QWidget):
    """
    查询（select）系统：
    查询种类分为三种：库存查询、售货查询、进货查询
    库存查询查询条件为商品名称或条形码，用户 在输入条形码或者商品名称时
    系统进行查询并将相应的信息显示，如果用户未输入任何信息，则将库存表中所有信息全部打印
    进货查询和售货查询的查询条件都是商品名称或条形码及时间域，时间域由两个时间组成
    其中进货时间域精确到日，售货时间域精确到秒
    当用户使用进货查询或售货查询时如果未输入任何查询内容即开始查询，系统将会将时间域内
    所有的信息全部显示
    所有查询结果显示是都以时间为准升序排列
    查询结果显示方式是表格，所以每次点击查询时会先清除上次查询的结果
    
    """
    def __init__(self):
        super(Shopselect, self).__init__()
        self.initUI()
    #UI窗口设计
    def initUI(self):
        self.resize(1366, 768)
        #self.setGeometry(50, 50, 800, 600)
        label_select_title = QLabel()
        label_select_title.setText("信息查询")
        label_select_title.setFont(QFont("华文行楷", 25))
        self.tabel_main = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabel_main.addTab(self.tab1, "Tab 1")
        self.tabel_main.addTab(self.tab2, "Tab 2")
        self.tabel_main.addTab(self.tab3, "Tab 3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
    #布局设计
        layout = QVBoxLayout(self)
        v = QVBoxLayout()
        s_title = QWidget()
        s_title.setFixedSize(800, 80)
        s_title.setLayout(v)
        v.addWidget(label_select_title,0,  Qt.AlignCenter)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(s_title)
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.tabel_main)
        layout.addWidget(splitter2)
        #tab1的UI
    def tab1UI(self):
        #窗口1的标题
        self.tabel_main.setTabText(0, "库存查询")
        #创建一个下拉列表框，并设置信号槽绑定事件
        self.tab1.cb = QComboBox()
        self.tab1.cb.addItems(["商品名称", "条形码"])
        self.tab1.cb.activated.connect(self.event_cb1)
        self.tab1.lineEdit = QLineEdit()
        #定义查询按钮，绑定事件
        self.tab1.btn_select = QPushButton("查询")
        self.tab1.btn_select.clicked.connect(self.event_select1)
        layout_tab1 = QHBoxLayout()
        tab1_11 = QWidget()
        tab1_12 = QWidget()
        self.tab1_2 = QTableWidget()
        self.tab1_2.setRowCount(25)
        self.tab1_2.setColumnCount(6)
        self.tab1_2.setHorizontalHeaderLabels(["条形码", "商品名称", "生产厂商", "规格", "零售价", "库存量"])
        self.tab1_2.setColumnWidth(2, 200)
        self.tab1_2.setColumnWidth(1, 140)
        self.tab1_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab1.cb)
        h1.addWidget(self.tab1.lineEdit)
        h2.addWidget(self.tab1.btn_select)
        tab1_11.setLayout(h1)
        tab1_12.setLayout(h2)
        splitter_select_Tab1_1 = QSplitter(Qt.Horizontal)
        splitter_select_Tab1_1.addWidget(tab1_12)
        splitter_select_Tab1_1.setSizes([150, 80])
        splitter_select_Tab1_2 = QSplitter(Qt.Horizontal)
        splitter_select_Tab1_2.addWidget(tab1_11)
        splitter_select_Tab1_2.addWidget(splitter_select_Tab1_1)
        splitter_select_Tab1_3 = QSplitter(Qt.Vertical)
        splitter_select_Tab1_3.addWidget(splitter_select_Tab1_2)
        splitter_select_Tab1_3.addWidget(self.tab1_2)
        layout_tab1.addWidget(splitter_select_Tab1_3)
        self.tab1.setLayout(layout_tab1)
        #tab2的UI
    def tab2UI(self):
        self.tabel_main.setTabText(1, "进货查询")
        self.tab2.cb = QComboBox()
        self.tab2.cb.addItems(["商品名称", "条形码"])
        self.tab2.cb.activated.connect(self.event_cb2)
        self.tab2.label = QLabel("采购时间")
        self.tab2.labelnull = QLabel("——")
        self.tab2.lineEdit = QLineEdit()
        self.tab2.dateEdit1 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab2)
        self.tab2.dateEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab2)
        self.tab2.dateEdit1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tab2.dateEdit2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tab2.dateEdit1.setCalendarPopup(True)
        self.tab2.dateEdit2.setCalendarPopup(True)
        self.tab2.btn_select = QPushButton("查询")
        self.tab2.btn_select.clicked.connect(self.event_select2)
        layout_tab2 = QHBoxLayout()
        tab2_11 = QWidget()
        tab2_12 = QWidget()
        self.tab2_2 = QTableWidget()
        self.tab2_2.setRowCount(500)
        self.tab2_2.setColumnCount(7)
        self.tab2_2.setHorizontalHeaderLabels(["条形码", "商品名称", "生产厂商", "规格", "进价","采购数量", "采购日期"])
        self.tab2_2.setColumnWidth(6, 190)
        self.tab2_2.setColumnWidth(1, 120)
        self.tab2_2.setColumnWidth(2, 150)
        self.tab2_2.setColumnWidth(3, 50)
        self.tab2_2.setColumnWidth(4, 75)
        self.tab2_2.setColumnWidth(5, 75)
        self.tab2_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab2.cb)
        h1.addWidget(self.tab2.lineEdit)
        h1.addWidget(self.tab2.label)
        h1.addWidget(self.tab2.dateEdit1)
        h1.addWidget(self.tab2.labelnull)
        h1.addWidget(self.tab2.dateEdit2)
        h2.addWidget(self.tab2.btn_select)
        tab2_11.setLayout(h1)
        tab2_12.setLayout(h2)
        splitter_select_tab2_1 = QSplitter(Qt.Horizontal)
        splitter_select_tab2_1.addWidget(tab2_12)
        splitter_select_tab2_1.setSizes([150, 80])
        splitter_select_tab2_2 = QSplitter(Qt.Horizontal)
        splitter_select_tab2_2.addWidget(tab2_11)
        splitter_select_tab2_2.addWidget(splitter_select_tab2_1)
        splitter_select_tab2_3 = QSplitter(Qt.Vertical)
        splitter_select_tab2_3.addWidget(splitter_select_tab2_2)
        splitter_select_tab2_3.addWidget(self.tab2_2)
        layout_tab2.addWidget(splitter_select_tab2_3)
        self.tab2.setLayout(layout_tab2)
        #tab3的UI
    def tab3UI(self):
        self.tabel_main.setTabText(2, "售货查询")
        self.tab3.cb = QComboBox()
        self.tab3.cb.addItems(["商品名称", "条形码"])
        self.tab3.cb.activated.connect(self.event_cb3)
        self.tab3.label = QLabel("销售时间")
        self.tab3.labelnull = QLabel("——")
        self.tab3.lineEdit = QLineEdit()
        self.tab3.dateEdit1 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab3)
        self.tab3.dateEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab3)
        self.tab3.dateEdit1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tab3.dateEdit2.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.tab3.dateEdit1.setCalendarPopup(True)
        self.tab3.dateEdit2.setCalendarPopup(True)
        self.tab3.btn_select = QPushButton("查询")
        self.tab3.btn_select.clicked.connect(self.event_select3)
        layout_tab3 = QHBoxLayout()
        tab3_11 = QWidget()
        tab3_12 = QWidget()
        self.tab3_2 = QTableWidget()
        self.tab3_2.setRowCount(500)
        self.tab3_2.setColumnCount(6)
        self.tab3_2.setHorizontalHeaderLabels(["条形码", "商品名称", "规格", "零售价", "销售数量", "售出时间"])
        self.tab3_2.setColumnWidth(1, 150)
        self.tab3_2.setColumnWidth(5, 200)
        self.tab3_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab3.cb)
        h1.addWidget(self.tab3.lineEdit)
        h1.addWidget(self.tab3.label)
        h1.addWidget(self.tab3.dateEdit1)
        h1.addWidget(self.tab3.labelnull)
        h1.addWidget(self.tab3.dateEdit2)
        h2.addWidget(self.tab3.btn_select)
        tab3_11.setLayout(h1)
        tab3_12.setLayout(h2)
        splitter_select_tab3_1 = QSplitter(Qt.Horizontal)
        splitter_select_tab3_1.addWidget(tab3_12)
        splitter_select_tab3_1.setSizes([150, 80])
        splitter_select_tab3_2 = QSplitter(Qt.Horizontal)
        splitter_select_tab3_2.addWidget(tab3_11)
        splitter_select_tab3_2.addWidget(splitter_select_tab3_1)
        splitter_select_tab3_3 = QSplitter(Qt.Vertical)
        splitter_select_tab3_3.addWidget(splitter_select_tab3_2)
        splitter_select_tab3_3.addWidget(self.tab3_2)
        layout_tab3.addWidget(splitter_select_tab3_3)
        self.tab3.setLayout(layout_tab3)
        
        #下拉选框出现变化时输入框清零
    def event_cb1(self):
        self.tab1.lineEdit.setText("")
    def event_cb2(self):
        self.tab2.lineEdit.setText("")
    def event_cb3(self):
        self.tab3.lineEdit.setText("")
        
    #库存查询
    def event_select1(self):
        #每次查询前都应该先清除表中内容
        for i in range(25):
            for j in range(6):
                tab1_newItem0 = QTableWidgetItem("")
                self.tab1_2.setItem(i, j, tab1_newItem0)
        #获取输入框中的内容
        text = self.tab1.lineEdit.text()
        if self.tab1.cb.currentText() == "条形码":
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select intxm,spmc,sccs,spgg,lsj,kcl from Inventory")
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    newItem1 = QTableWidgetItem(str(rows[i].intxm))
                    newItem2 = QTableWidgetItem(rows[i].spmc)
                    newItem3 = QTableWidgetItem(rows[i].sccs)
                    newItem4 = QTableWidgetItem(rows[i].spgg)
                    newItem5 = QTableWidgetItem(str(rows[i].lsj))
                    newItem6 = QTableWidgetItem(str(rows[i].kcl))
                    self.tab1_2.setItem(i, 0, newItem1)
                    self.tab1_2.setItem(i, 1, newItem2)
                    self.tab1_2.setItem(i, 2, newItem3)
                    self.tab1_2.setItem(i, 3, newItem4)
                    self.tab1_2.setItem(i, 4, newItem5)
                    self.tab1_2.setItem(i, 5, newItem6)
                conn.close()
            else:
                try:
                    conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                    cursor = conn.cursor()
                    cursor.execute("select intxm from Inventory")
                    row = cursor.fetchall()
                    r = []
                    #将库存表中的所有物品的条形码存入到一个列表中，便于比较信息判断库存表中是否存储有所查询的信息
                    for i in range(len(row)):
                        r.append(row[i].intxm)
                    if int(text) not in r:
                        replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                    else:
                        cursor.execute("select intxm,spmc,sccs,spgg,lsj,kcl from Inventory where intxm=%d"%int(text))
                        rows = cursor.fetchone()
                        newItem1 = QTableWidgetItem(str(rows[0]))
                        newItem2 = QTableWidgetItem(rows[1])
                        newItem3 = QTableWidgetItem(rows[2])
                        newItem4 = QTableWidgetItem(rows[3])
                        newItem5 = QTableWidgetItem(str(rows[4]))
                        newItem6 = QTableWidgetItem(str(rows[5]))
                        self.tab1_2.setItem(0, 0, newItem1)
                        self.tab1_2.setItem(0, 1, newItem2)
                        self.tab1_2.setItem(0, 2, newItem3)
                        self.tab1_2.setItem(0, 3, newItem4)
                        self.tab1_2.setItem(0, 4, newItem5)
                        self.tab1_2.setItem(0, 5, newItem6)
                    conn.close()
                except ValueError:
                    replay = QMessageBox.warning(self, "条形码输入错误!", "请正确填写查询信息！", QMessageBox.Yes)
        else:
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select intxm,spmc,sccs,spgg,lsj,kcl from Inventory")
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    newItem1 = QTableWidgetItem(str(rows[i].intxm))
                    newItem2 = QTableWidgetItem(rows[i].spmc)
                    newItem3 = QTableWidgetItem(rows[i].sccs)
                    newItem4 = QTableWidgetItem(rows[i].spgg)
                    newItem5 = QTableWidgetItem(str(rows[i].lsj))
                    newItem6 = QTableWidgetItem(str(rows[i].kcl))
                    self.tab1_2.setItem(i, 0, newItem1)
                    self.tab1_2.setItem(i, 1, newItem2)
                    self.tab1_2.setItem(i, 2, newItem3)
                    self.tab1_2.setItem(i, 3, newItem4)
                    self.tab1_2.setItem(i, 4, newItem5)
                    self.tab1_2.setItem(i, 5, newItem6)
                conn.close()
            else:
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select spmc from Inventory")
                row = cursor.fetchall()
                r = []
                #将库存表中所偶物品的名称全部存储到一个列表r中
                for i in range(len(row)):
                    r.append(row[i].spmc.strip())
                if text not in r:
                    replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                else:
                    cursor.execute("select intxm,spmc,sccs,spgg,lsj,kcl from Inventory where spmc=%r"%text)
                    rows = cursor.fetchone()
                    newItem1 = QTableWidgetItem(str(rows[0]))
                    newItem2 = QTableWidgetItem(rows[1])
                    newItem3 = QTableWidgetItem(rows[2])
                    newItem4 = QTableWidgetItem(rows[3])
                    newItem5 = QTableWidgetItem(str(rows[4]))
                    newItem6 = QTableWidgetItem(str(rows[5]))
                    self.tab1_2.setItem(0, 0, newItem1)
                    self.tab1_2.setItem(0, 1, newItem2)
                    self.tab1_2.setItem(0, 2, newItem3)
                    self.tab1_2.setItem(0, 3, newItem4)
                    self.tab1_2.setItem(0, 4, newItem5)
                    self.tab1_2.setItem(0, 5, newItem6)
                conn.close()
        #进货查询
    def event_select2(self):
        #清空显示table
        for i in range(500):
            for j in range(7):
                tab2_newItem0 = QTableWidgetItem("")
                self.tab2_2.setItem(i, j, tab2_newItem0)
        #获取输入框内容
        text = self.tab2.lineEdit.text()
        #获取两个时间，组成时间段
        time1 = self.tab2.dateEdit1.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        time2 = self.tab2.dateEdit2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.tab2.cb.currentText() == "条形码":
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中时间段内所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select sttxm,spmc,sccs,spgg,jj,cgsl,cgrq from Stock,Inventory  where Stock.sttxm=Inventory.intxm and cgrq>=%r and cgrq <=%r order by cgrq"%( time1, time2))
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    tab2_newItem1 = QTableWidgetItem(str(rows[i].sttxm))
                    tab2_newItem2 = QTableWidgetItem(rows[i].spmc)
                    tab2_newItem3 = QTableWidgetItem(rows[i].sccs)
                    tab2_newItem4 = QTableWidgetItem(rows[i].spgg)
                    tab2_newItem5 = QTableWidgetItem(str(rows[i].jj))
                    tab2_newItem6 = QTableWidgetItem(str(rows[i].cgsl))
                    tab2_newItem7 = QTableWidgetItem(str(rows[i].cgrq))
                    self.tab2_2.setItem(i, 0, tab2_newItem1)
                    self.tab2_2.setItem(i, 1, tab2_newItem2)
                    self.tab2_2.setItem(i, 2, tab2_newItem3)
                    self.tab2_2.setItem(i, 3, tab2_newItem4)
                    self.tab2_2.setItem(i, 4, tab2_newItem5)
                    self.tab2_2.setItem(i, 5, tab2_newItem6)
                    self.tab2_2.setItem(i, 6, tab2_newItem7)
                conn.close()
            else:
                try:
                    conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                    cursor = conn.cursor()
                    cursor.execute("select intxm from Inventory")
                    row = cursor.fetchall()
                    r = []
                    for i in range(len(row)):
                        r.append(row[i].intxm)
                    if int(text) not in r:
                        replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                    else:
                        cursor.execute("select sttxm,spmc,sccs,spgg,jj,cgsl,cgrq from Stock,Inventory  where intxm=sttxm and sttxm=%d and cgrq>=%r and cgrq <=%r order by cgrq"%(int(text), time1, time2))
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            tab2_newItem1 = QTableWidgetItem(str(rows[i].sttxm))
                            tab2_newItem2 = QTableWidgetItem(rows[i].spmc)
                            tab2_newItem3 = QTableWidgetItem(rows[i].sccs)
                            tab2_newItem4 = QTableWidgetItem(rows[i].spgg)
                            tab2_newItem5 = QTableWidgetItem(str(rows[i].jj))
                            tab2_newItem6 = QTableWidgetItem(str(rows[i].cgsl))
                            tab2_newItem7 = QTableWidgetItem(str(rows[i].cgrq))
                            self.tab2_2.setItem(i, 0, tab2_newItem1)
                            self.tab2_2.setItem(i, 1, tab2_newItem2)
                            self.tab2_2.setItem(i, 2, tab2_newItem3)
                            self.tab2_2.setItem(i, 3, tab2_newItem4)
                            self.tab2_2.setItem(i, 4, tab2_newItem5)
                            self.tab2_2.setItem(i, 5, tab2_newItem6)
                            self.tab2_2.setItem(i, 6, tab2_newItem7)
                        conn.close()
                except ValueError:
                    replay = QMessageBox.warning(self, "条形码输入错误!", "请正确填写查询信息！", QMessageBox.Yes)
        else:
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中时间段内所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select sttxm,spmc,sccs,spgg,jj,cgsl,cgrq from (select Stock.*,Inventory.* from Stock inner join Inventory on Stock.sttxm=Inventory.intxm)A where cgrq>=%r and cgrq <=%r order by cgrq"%( time1, time2))
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    tab2_newItem1 = QTableWidgetItem(str(rows[i].sttxm))
                    tab2_newItem2 = QTableWidgetItem(rows[i].spmc)
                    tab2_newItem3 = QTableWidgetItem(rows[i].sccs)
                    tab2_newItem4 = QTableWidgetItem(rows[i].spgg)
                    tab2_newItem5 = QTableWidgetItem(str(rows[i].jj))
                    tab2_newItem6 = QTableWidgetItem(str(rows[i].cgsl))
                    tab2_newItem7 = QTableWidgetItem(str(rows[i].cgrq))
                    self.tab2_2.setItem(i, 0, tab2_newItem1)
                    self.tab2_2.setItem(i, 1, tab2_newItem2)
                    self.tab2_2.setItem(i, 2, tab2_newItem3)
                    self.tab2_2.setItem(i, 3, tab2_newItem4)
                    self.tab2_2.setItem(i, 4, tab2_newItem5)
                    self.tab2_2.setItem(i, 5, tab2_newItem6)
                    self.tab2_2.setItem(i, 6, tab2_newItem7)
                conn.close()
            else:
                try:
                    conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                    cursor = conn.cursor()
                    cursor.execute("select spmc from Inventory")
                    row = cursor.fetchall()
                    r = []
                    for i in range(len(row)):
                        r.append(row[i].spmc.strip())
                    if text not in r:
                        replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                    else:
                        cursor.execute("select sttxm,spmc,sccs,spgg,jj,cgsl,cgrq from (select Stock.*,Inventory.* from Stock inner join Inventory on Stock.sttxm=Inventory.intxm)A where spmc=%r and cgrq>=%r and cgrq <=%r order by cgrq"%(text, time1, time2))
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            tab2_newItem1 = QTableWidgetItem(str(rows[i].sttxm))
                            tab2_newItem2 = QTableWidgetItem(rows[i].spmc)
                            tab2_newItem3 = QTableWidgetItem(rows[i].sccs)
                            tab2_newItem4 = QTableWidgetItem(rows[i].spgg)
                            tab2_newItem5 = QTableWidgetItem(str(rows[i].jj))
                            tab2_newItem6 = QTableWidgetItem(str(rows[i].cgsl))
                            tab2_newItem7 = QTableWidgetItem(str(rows[i].cgrq))
                            self.tab2_2.setItem(i, 0, tab2_newItem1)
                            self.tab2_2.setItem(i, 1, tab2_newItem2)
                            self.tab2_2.setItem(i, 2, tab2_newItem3)
                            self.tab2_2.setItem(i, 3, tab2_newItem4)
                            self.tab2_2.setItem(i, 4, tab2_newItem5)
                            self.tab2_2.setItem(i, 5, tab2_newItem6)
                            self.tab2_2.setItem(i, 6, tab2_newItem7)
                        conn.close()
                except ValueError:
                   replay = QMessageBox.warning(self, "商品名称输入错误!", "请正确填写查询信息！", QMessageBox.Yes)
    #售货查询
    def event_select3(self):
        #清空
        for i in range(500):
            for j in range(6):
                tab3_newItem0 = QTableWidgetItem("")
                self.tab3_2.setItem(i, j, tab3_newItem0)
        #获取输入框内容及时间
        text = self.tab3.lineEdit.text()
        time1 = self.tab3.dateEdit1.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        time2 = self.tab3.dateEdit2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.tab3.cb.currentText() == "条形码":
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中时间段内所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select setxm,spmc,spgg,Sellgoods.lsj lsj,xssl,xssj from Sellgoods,Inventory  where Inventory.intxm=Sellgoods.setxm and xssj>=%r and xssj<=%r order by xssj"%( time1, time2))
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    tab3_newItem1 = QTableWidgetItem(str(rows[i].setxm))
                    tab3_newItem2 = QTableWidgetItem(rows[i].spmc)
                    tab3_newItem3 = QTableWidgetItem(rows[i].spgg)
                    tab3_newItem4 = QTableWidgetItem(str(rows[i].lsj))
                    tab3_newItem5 = QTableWidgetItem(str(rows[i].xssl))
                    tab3_newItem6 = QTableWidgetItem(str(rows[i].xssj))
                    self.tab3_2.setItem(i, 0, tab3_newItem1)
                    self.tab3_2.setItem(i, 1, tab3_newItem2)
                    self.tab3_2.setItem(i, 2, tab3_newItem3)
                    self.tab3_2.setItem(i, 3, tab3_newItem4)
                    self.tab3_2.setItem(i, 4, tab3_newItem5)
                    self.tab3_2.setItem(i, 5, tab3_newItem6)
                conn.close()
            else:
                try:
                    conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                    cursor = conn.cursor()
                    cursor.execute("select setxm from Sellgoods")
                    row = cursor.fetchall()
                    r = []
                    for i in range(len(row)):
                        r.append(row[i].setxm)
                    if int(text) not in r:
                        replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                    else:
                        cursor.execute("select setxm,spmc,spgg,Sellgoods.lsj lsj,xssl,xssj from Sellgoods,Inventory  where Inventory.intxm=Sellgoods.setxm and setxm=%d and xssj>=%r and xssj<=%r order by xssj"%(int(text), time1, time2))
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            tab3_newItem1 = QTableWidgetItem(str(rows[i].setxm))
                            tab3_newItem2 = QTableWidgetItem(rows[i].spmc)
                            tab3_newItem3 = QTableWidgetItem(rows[i].spgg)
                            tab3_newItem4 = QTableWidgetItem(str(rows[i].lsj))
                            tab3_newItem5 = QTableWidgetItem(str(rows[i].xssl))
                            tab3_newItem6 = QTableWidgetItem(str(rows[i].xssj))
                            self.tab3_2.setItem(i, 0, tab3_newItem1)
                            self.tab3_2.setItem(i, 1, tab3_newItem2)
                            self.tab3_2.setItem(i, 2, tab3_newItem3)
                            self.tab3_2.setItem(i, 3, tab3_newItem4)
                            self.tab3_2.setItem(i, 4, tab3_newItem5)
                            self.tab3_2.setItem(i, 5, tab3_newItem6)
                        conn.close()
                except ValueError:
                    replay = QMessageBox.warning(self, "条形码输入错误!", "请正确填写查询信息！", QMessageBox.Yes)
        else:
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中时间段内所有数据全部显示出来
                conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                cursor = conn.cursor()
                cursor.execute("select setxm,spmc,spgg,Sellgoods.lsj lsj,xssl,xssj from Sellgoods,Inventory  where intxm=setxm and xssj>=%r and xssj<=%r order by xssj"%( time1, time2))
                rows = cursor.fetchall()
                for i in range(len(rows)):
                    tab3_newItem1 = QTableWidgetItem(str(rows[i].setxm))
                    tab3_newItem2 = QTableWidgetItem(rows[i].spmc)
                    tab3_newItem3 = QTableWidgetItem(rows[i].spgg)
                    tab3_newItem4 = QTableWidgetItem(str(rows[i].lsj))
                    tab3_newItem5 = QTableWidgetItem(str(rows[i].xssl))
                    tab3_newItem6 = QTableWidgetItem(str(rows[i].xssj))
                    self.tab3_2.setItem(i, 0, tab3_newItem1)
                    self.tab3_2.setItem(i, 1, tab3_newItem2)
                    self.tab3_2.setItem(i, 2, tab3_newItem3)
                    self.tab3_2.setItem(i, 3, tab3_newItem4)
                    self.tab3_2.setItem(i, 4, tab3_newItem5)
                    self.tab3_2.setItem(i, 5, tab3_newItem6)
                conn.close()
            else:
                try:
                    conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
                    cursor = conn.cursor()
                    cursor.execute("select spmc from Inventory")
                    row = cursor.fetchall()
                    r = []
                    for i in range(len(row)):
                        r.append(row[i].spmc.strip())
                    if text not in r:
                        replay = QMessageBox.warning(self, "商品不存在！", "请正确填写商品信息！", QMessageBox.Yes)
                    else:
                        cursor.execute("select setxm,spmc,spgg,Sellgoods.lsj lsj,xssl,xssj from Sellgoods,Inventory  where intxm=setxm and spmc=%r and xssj>=%r and xssj<=%r order by xssj"%(text, time1, time2))
                        rows = cursor.fetchall()
                        for i in range(len(rows)):
                            tab3_newItem1 = QTableWidgetItem(str(rows[i].setxm))
                            tab3_newItem2 = QTableWidgetItem(rows[i].spmc)
                            tab3_newItem3 = QTableWidgetItem(rows[i].spgg)
                            tab3_newItem4 = QTableWidgetItem(str(rows[i].lsj))
                            tab3_newItem5 = QTableWidgetItem(str(rows[i].xssl))
                            tab3_newItem6 = QTableWidgetItem(str(rows[i].xssj))
                            self.tab3_2.setItem(i, 0, tab3_newItem1)
                            self.tab3_2.setItem(i, 1, tab3_newItem2)
                            self.tab3_2.setItem(i, 2, tab3_newItem3)
                            self.tab3_2.setItem(i, 3, tab3_newItem4)
                            self.tab3_2.setItem(i, 4, tab3_newItem5)
                            self.tab3_2.setItem(i, 5, tab3_newItem6)
                        conn.close()
                except ValueError:
                    replay = QMessageBox.warning(self, "商品名称输入错误!", "请正确填写查询信息！", QMessageBox.Yes)
        #添加背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("select.jpg")
        painter.drawPixmap(self.rect(), pixmap)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopselect()
    sell.show()
    sys.exit(app.exec())
        
