import sys
import pyodbc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Shopstock(QWidget):
    '''
    进货录入系统（Shopstock）：
    将进货信息依次按照顺序进行录入；设计时需要注意以下几项：
    1、输入框应该规范，位置排列应当整齐
    2、每个输入框需要输入的数据类型都有严格的规定，所以应该注意设置每个输入框的输入类型
    3、条形码和采购数量应该为整形，进价和零售价应该为浮点型
    4、日期应该特别注意，要设置日期输入样式示例，还要检查日期输入是否正确，月份（1，12），
         日期（1，31）还应考虑是否是闰年
    5、点击录入时应该首先将整个录入信息显示在显示框内，管理员再次确认无误后才能确定录入，
         如果录入信息出现错误应该选择清除当前录入的信息条
    '''
    def __init__(self):
        super(Shopstock, self).__init__()
        self.initUI()
    #UI设计
    def initUI(self):
        self.setGeometry(60, 60, 800, 600)
        self.label_stock_title = QLabel()
        self.label_stock_title.setText("进货录入")
        self.label_stock_title.setFont(QFont("华文行楷", 25))
        self.label_lrxq = QLabel("录入详情")
        self.label_lrxq.setFont(QFont("宋体", 15))
        self.label1 = QLabel("条形码")
        self.label2 = QLabel("商品名称")
        self.label3 = QLabel("生产厂商")
        self.label4 = QLabel("商品规格")
        self.label5 = QLabel("进价")
        self.label6 = QLabel("零售价")
        self.label7 = QLabel("采购数量")
        self.label8 = QLabel("采购日期")
        #增加一个label作为日期输入样例提醒
        self.label9 = QLabel()
        self.label10 = QLabel("日期输入示例：2018-5-6")
        self.label1.setFixedSize(60, 40)
        self.label2.setFixedSize(60, 40)
        self.label3.setFixedSize(60, 40)
        self.label4.setFixedSize(60, 40)
        self.label5.setFixedSize(60, 40)
        self.label6.setFixedSize(60, 40)
        self.label7.setFixedSize(60, 40)
        self.label8.setFixedSize(60, 40)
        self.label9.setFixedSize(60, 40)

        #定义多个空列表用于暂存录入的信息
        self.txm = []
        self.spmc = []
        self.sccs = []
        self.spgg = []
        self.jj = []
        self.lsj = []
        self.cgsl = []
        self.cgrq = []
        #创建条形码的输入框并设置为只能输入整数
        #设置当条形码输入时，如果不是第一次输入那么自动补全某些信息
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setValidator(QIntValidator())
        self.lineEdit1.editingFinished.connect(self.buquan)
        self.lineEdit1.textChanged.connect(self.buquan)
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
        self.lineEdit4 = QLineEdit()
        #创建进价的输入框并设置为只能输入float型数据
        self.lineEdit5 = QLineEdit()
        self.lineEdit5.setValidator(QDoubleValidator())
        #创建零售价的输入框并设置只能输入float型数据
        self.lineEdit6 = QLineEdit()
        self.lineEdit6.setValidator(QDoubleValidator())
        #创建采购数量的输入框并设置为只允许输入整形数据
        self.lineEdit7 = QLineEdit()
        self.lineEdit7.setValidator(QIntValidator())
        #创建日期录入框并设置录入规范
        self.lineEdit8 = QLineEdit()
        #创建录入显示框并设置为只读模式
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        #定义确定按钮并绑定事件信号
        self.btn_stock_ok = QPushButton("确定")
        self.btn_stock_ok.clicked.connect(self.event_ok)
        #定义清除按钮并绑定事件信号
        self.btn_stock_eliminate = QPushButton("清除")
        self.btn_stock_eliminate.clicked.connect(self.event_eliminate)
        #定义录入按钮并绑定事件信号
        self.btn_stock_lr = QPushButton("录入")
        self.btn_stock_lr.clicked.connect(self.event_lr)
        self.btn_stock_lr.setFixedSize(70, 30)
        hbox = QHBoxLayout()
        v1 = QVBoxLayout()
        v3 = QVBoxLayout()
        v2 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        h4 = QHBoxLayout()
        h5 = QHBoxLayout()
        h6 = QHBoxLayout()
        h7 = QHBoxLayout()
        h8 = QHBoxLayout()
        h9 = QHBoxLayout()
        h10 = QHBoxLayout()
        h1.addWidget(self.label1)
        h1.addWidget(self.lineEdit1)
        h2.addWidget(self.label2)
        h2.addWidget(self.lineEdit2)
        h3.addWidget(self.label3)
        h3.addWidget(self.lineEdit3)
        h4.addWidget(self.label4)
        h4.addWidget(self.lineEdit4)
        h5.addWidget(self.label5)
        h5.addWidget(self.lineEdit5)
        h6.addWidget(self.label6)
        h6.addWidget(self.lineEdit6)
        h7.addWidget(self.label7)
        h7.addWidget(self.lineEdit7)
        h8.addWidget(self.label8)
        h8.addWidget(self.lineEdit8)
        h9.addWidget(self.btn_stock_lr)
        h10.addWidget(self.label9)
        h10.addWidget(self.label10)
        v3.addLayout(h1)
        v3.addLayout(h2)
        v3.addLayout(h3)
        v3.addLayout(h4)
        v3.addLayout(h5)
        v3.addLayout(h6)
        v3.addLayout(h7)
        v3.addLayout(h8)
        v3.addLayout(h10)
        v3.addLayout(h9)
        self.w_top = QWidget()
        self.w_top.setLayout(v1)
        self.w_left = QWidget()
        self.w_left.setLayout(v3)
        self.w_right = QWidget()
        self.w_right.setLayout(v2)
        v1.addWidget(self.label_stock_title, 0, Qt.AlignCenter|Qt.AlignVCenter)
        v2.addWidget(self.label_lrxq, 0, Qt.AlignCenter|Qt.AlignVCenter)
        v2.addWidget(self.textEdit)
        v2.addWidget(self.btn_stock_ok)
        v2.addWidget(self.btn_stock_eliminate)
        splitter_stock1 = QSplitter(Qt.Vertical)
        splitter_stock2 = QSplitter(Qt.Horizontal)
        splitter_stock3 = QSplitter(Qt.Horizontal)
        splitter_stock4 = QSplitter(Qt.Vertical)
        splitter_stock1.addWidget(self.w_top)
        splitter_stock1.setSizes([800, 80])
        splitter_stock2.addWidget(self.w_left)
        splitter_stock2.setSizes([350, 520])
        splitter_stock3.addWidget(splitter_stock2)
        splitter_stock3.addWidget(self.w_right)
        splitter_stock4.addWidget(splitter_stock1)
        splitter_stock4.addWidget(splitter_stock3)
        hbox.addWidget(splitter_stock4)
        self.setLayout(hbox)
        self.show()
    #信息录入槽
    def event_lr(self):
        #获得输入框内的信息
        txm = self.lineEdit1.text()
        spmc = self.lineEdit2.text()
        sccs = self.lineEdit3.text()
        spgg = self.lineEdit4.text()
        jj = self.lineEdit5.text()
        lsj = self.lineEdit6.text()
        cgsl = self.lineEdit7.text()
        cgrq = self.lineEdit8.text()
        #判断任何一个信息框是否为空
        if txm==''or spmc=='' or sccs==''or spgg==''or jj==''or lsj==''or cgsl==''or cgrq=='':
             replay = QMessageBox.warning(self, "!", "录入信息有空缺", QMessageBox.Yes)
        temp = False
        #核查日期输入格式是否正确,并将信息暂存于列表中
        rq = cgrq.split('-')
        if  not rq[0].isdigit()or(len(rq)!=3):
            replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
        else:
            if rq[1]=='' or int(rq[1]) not in range(1, 13):
                replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
            else:
                if int(rq[1]) in [1, 3, 5, 7, 8, 10, 12]:
                    if rq[2]=='' or int(rq[2]) >31 or int(rq[2])<=0:
                        replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
                    else:
                        self.cgrq.append(cgrq)
                        temp = True
                elif int(rq[1]) in [4, 6, 9, 11]:
                    if rq[2]=='' or int(rq[2]) > 30 or int(rq[2]) <= 0:
                        replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
                    else:
                        self.cgrq.append(cgrq)
                        temp = True
                else:
                    if (int(rq[0])%4==0 and int(rq[0])%100!=0)or (int(rq[0])%400==0):
                        if rq[2]=='' or int(rq[2])>29 or int(rq[2])<=0:
                            replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
                        else:
                            self.cgrq.append(cgrq)
                            temp = True
                    else:
                       if rq[2]=='' or int(rq[2])>28 or int(rq[2])<=0:
                          replay = QMessageBox.warning(self, "!", "日期输入错误", QMessageBox.Yes)
                       else:
                           self.cgrq.append(cgrq)
                           temp = True
        #将其余信息读入列表暂存
        if temp:
            self.txm.append(int(txm))
            self.spmc.append(spmc)
            self.sccs.append(sccs)
            self.spgg.append(spgg)
            self.jj.append(float(jj))
            self.lsj.append(float(lsj))
            self.cgsl.append(int(cgsl))
            #将信息显示在录入信息显示框内
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"**********************************\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"条形码："+txm+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"商品名称："+spmc+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"生产厂商："+sccs+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"产品规格："+spgg+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"进价："+jj+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"零售价："+lsj+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"采购数量："+cgsl+"\n")
            self.textEdit.setPlainText(self.textEdit.toPlainText()+"采购日期："+cgrq+"\n")
            #每次录入完一条信息应该将输入框全部清零
            self.lineEdit1.clear()
            self.lineEdit2.clear()
            self.lineEdit3.clear()
            self.lineEdit4.clear()
            self.lineEdit5.clear()
            self.lineEdit6.clear()
            self.lineEdit7.clear()
            self.lineEdit8.clear()
    #将信息存入数据库
    def event_ok(self):
        #首先连接数据库并建立cursor
        conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
        cursor = conn.cursor()
        #依次向数据库中插入数据
        lenth = len(self.txm)
        i = 0
        while(i<lenth):
            cursor.execute("insert into Stock values(%d,%f,%d,%r)"%(self.txm[i], self.jj[i], self.cgsl[i], self.cgrq[i]))
            #给库存表添加信息时应注意表中是否已经有了该商品的一些信息
            cursor.execute("select intxm from Inventory")
            rows = cursor.fetchall()
            r = []
            for k in range(len(rows)):
                r.append(rows[k].intxm)
            if rows !=None and self.txm[i] in r:
                cursor.execute("select kcl from Inventory where intxm=%d"%self.txm[i])
                cgsl_old = cursor.fetchone()
                cursor.execute("update Inventory set kcl=%d where intxm = %d"%(cgsl_old[0]+self.cgsl[i], self.txm[i]))
            else :
                cursor.execute("insert into Inventory values(%d,%r,%d,%r,%r,%f)"%(self.txm[i], self.spmc[i], self.cgsl[i], self.sccs[i], self.spgg[i], self.lsj[i]))
            i +=1
        conn.commit()
        conn.close()
        self.event_eliminate()
    #清除信息
    def event_eliminate(self):
        #首先清除显示框内的录入信息
        self.textEdit.clear()
        #再依次将信息list清零
        self.txm=[]
        self.spmc=[]
        self.sccs=[]
        self.spgg=[]
        self.jj=[]
        self.lsj=[]
        self.cgsl=[]
        self.cgrq=[]
    #自动补全
    def buquan(self):
        conn = pyodbc.connect(r"DRIVER={SQL Server Native Client 10.0};SERVER=192.168.43.220,1433;DATABASE=Supermarket;UID=sa;PWD=Vv86865211")
        cursor = conn.cursor()
        cursor.execute("select sttxm from Stock")
        row = cursor.fetchall()
        #判断条形码是否为空
        if self.lineEdit1.text() != '':
            txm = int(self.lineEdit1.text())
        else:
            txm = 0
            #判断条形码是否已经在表中出现
        r = []
        for i in range(len(row)):
            r.append(row[i].sttxm)
        if row !=None and txm in r:
            self.lineEdit2.setReadOnly(True)
            self.lineEdit3.setReadOnly(True)
            self.lineEdit4.setReadOnly(True)
            self.lineEdit5.setReadOnly(True)
            self.lineEdit6.setReadOnly(True)
            cursor.execute("select Stock.jj,spmc,sccs,spgg,lsj from Stock,Inventory where sttxm=%d and Stock.sttxm=Inventory.intxm"%txm)
            rows = cursor.fetchone()
            self.lineEdit2.setText(str(rows[1].rstrip()))
            self.lineEdit3.setText(str(rows[2].rstrip()))
            self.lineEdit4.setText(str(rows[3].rstrip()))
            self.lineEdit5.setText(str(rows[0]))
            self.lineEdit6.setText(str(rows[4]))
            conn.close()
        else:
            self.lineEdit2.setText("")
            self.lineEdit3.setText("")
            self.lineEdit4.setText("")
            self.lineEdit5.setText("")
            self.lineEdit6.setText("")
            self.lineEdit2.setReadOnly(False)
            self.lineEdit3.setReadOnly(False)
            self.lineEdit4.setReadOnly(False)
            self.lineEdit5.setReadOnly(False)
            self.lineEdit6.setReadOnly(False)            
    #添加背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("stock.jpg")
        painter.drawPixmap(self.rect(), pixmap)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Shopstock()
    sys.exit(app.exec())
        
