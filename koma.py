import sys
import psycopg2
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidget, QGroupBox, QMessageBox, QDialog, QDateEdit, QCalendarWidget 
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QLineEdit, QLabel, QComboBox
from PyQt5 import QtGui
from PyQt5.QtGui import QIntValidator, QFont, QPixmap, QIcon
from PyQt5 import QtWidgets
from login import LoginWidget
import time


class DiplomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Колледж")
        self.ins = True
        #Подключение базы
        self.con()

        self.point_plant_label = QLabel("Контр. точки", self)
        self.point_plant_label.move(10, 494)
        font = QFont("", 14, 700, False)
        self.point_plant_label.setFont(font)
        self.point_plant_label.adjustSize()


        self.result_label = QLabel("Дипломы", self)
        self.result_label.move(10, 5)
        self.result_label.setFont(font)

        pixmap = QPixmap("/home/student/Рабочий стол/Python_SKD/diplom_python/diplom.png")
        pixmap = pixmap.scaled(120 , 120)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.move(10, 0)
        label.resize(pixmap.width(), pixmap.height())

        self.tableofresult = TABLE_OF_RESULT(self)
        self.tableofpoint = TABLE_OF_POINT(self)

        self.result_buttons_groupbox = QGroupBox(self)
        self.result_buttons_groupbox.resize(130, 125)
        self.result_buttons_groupbox.move(930, 25)

        self.result_buttons_groupbox.insert_button = QPushButton('Добавить', self.result_buttons_groupbox)
        self.result_buttons_groupbox.insert_button.resize(100, 30)
        self.result_buttons_groupbox.insert_button.move(10, 10)
        self.result_buttons_groupbox.insert_button.setVisible(self.IsGranTable[1])
        self.result_buttons_groupbox.insert_button.clicked.connect(self.insert_result)

        
        self.result_buttons_groupbox.update_Button = QPushButton('Изменить', self.result_buttons_groupbox)
        self.result_buttons_groupbox.update_Button.resize(100, 30)
        self.result_buttons_groupbox.update_Button.move(10, 50)
        self.result_buttons_groupbox.update_Button.setVisible(self.IsGranTable[1])
        self.result_buttons_groupbox.update_Button.clicked.connect(self.update_result)

        
        self.result_buttons_groupbox.DeleteButton = QPushButton('Удалить', self.result_buttons_groupbox)
        self.result_buttons_groupbox.DeleteButton.resize(100, 30)
        self.result_buttons_groupbox.DeleteButton.move(10, 90)
        self.result_buttons_groupbox.DeleteButton.setVisible(self.IsGranTable[1])
        self.result_buttons_groupbox.DeleteButton.clicked.connect(self.delete_result)

        
        self.result_param_groupbox = QGroupBox(self)
        self.result_param_groupbox.resize(300, 470)
        self.result_param_groupbox.move(600, 10)
        self.result_param_groupbox.hide()

        
        self.result_param_groupbox.label_result = QLabel("Студент", self.result_param_groupbox)
        self.result_param_groupbox.label_result.move(10, 10)
        self.result_param_groupbox.student = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.student.resize(280, 30)
        self.result_param_groupbox.student.move(10, 30)

        
        self.result_param_groupbox.label_result1 = QLabel("Группа", self.result_param_groupbox)
        self.result_param_groupbox.label_result1.move(10, 80)
        self.result_param_groupbox.group = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.group.resize(280, 30)
        self.result_param_groupbox.group.move(10, 100)
        
        
        self.result_param_groupbox.label_result3 = QLabel("Руководитель", self.result_param_groupbox)
        self.result_param_groupbox.label_result3.move(10, 150)
        self.result_param_groupbox.head = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.head.resize(280, 30)
        self.result_param_groupbox.head.move(10, 170)

        self.result_param_groupbox.label_result4 = QLabel("Отчёт", self.result_param_groupbox)
        self.result_param_groupbox.label_result4.move(10, 220)
        self.result_param_groupbox.report_submitted = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.report_submitted.resize(280, 30)
        self.result_param_groupbox.report_submitted.move(10, 240)

        self.result_param_groupbox.label_result5 = QLabel("Оценка", self.result_param_groupbox)
        self.result_param_groupbox.label_result5.move(10, 290)
        self.result_param_groupbox.estimation = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.estimation.resize(280, 30)
        self.result_param_groupbox.estimation.move(10, 310)

        self.result_param_groupbox.label_result6 = QLabel("Тема", self.result_param_groupbox)
        self.result_param_groupbox.label_result6.move(10, 360)
        self.result_param_groupbox.themes = QLineEdit(self.result_param_groupbox)
        self.result_param_groupbox.themes.resize(280, 30)
        self.result_param_groupbox.themes.move(10, 380)

        # кнопка OK
        self.result_param_groupbox.ok_button = QPushButton('OK', self.result_param_groupbox)
        self.result_param_groupbox.ok_button.resize(100, 30)
        self.result_param_groupbox.ok_button.move(10, 420)
        self.result_param_groupbox.ok_button.clicked.connect(self.ok_result)
        
        # кнопка Oтмена
        self.result_param_groupbox.cancel_button = QPushButton('Отмена', self.result_param_groupbox)
        self.result_param_groupbox.cancel_button.resize(100, 30)
        self.result_param_groupbox.cancel_button.move(130, 420)
        self.result_param_groupbox.cancel_button.clicked.connect(self.cancel_result)  

         # блок кнопок таблицы маршруты
        self.point_buttons_groupbox = QGroupBox(self)
        self.point_buttons_groupbox.resize(130, 165)
        self.point_buttons_groupbox.move(930, 205)

        # кнопка добавить 
        self.point_buttons_groupbox.insert_button = QPushButton('Добавить', self.point_buttons_groupbox)
        self.point_buttons_groupbox.insert_button.resize(100, 30)
        self.point_buttons_groupbox.insert_button.move(10, 10)
        self.point_buttons_groupbox.insert_button.setVisible(self.IsGranTable[4])
        self.point_buttons_groupbox.insert_button.clicked.connect(self.insert_point)

        # кнопка изменить 
        self.point_buttons_groupbox.update_button = QPushButton('Изменить', self.point_buttons_groupbox)
        self.point_buttons_groupbox.update_button.resize(100, 30)
        self.point_buttons_groupbox.update_button.move(10, 50)
        self.point_buttons_groupbox.update_button.setVisible(self.IsGranTable[4])
        self.point_buttons_groupbox.update_button.clicked.connect(self.update_point)

        # кнопка удалить запись
        self.point_buttons_groupbox.delete_button = QPushButton('Удалить', self.point_buttons_groupbox)
        self.point_buttons_groupbox.delete_button.resize(100, 30)
        self.point_buttons_groupbox.delete_button.move(10, 90)
        self.point_buttons_groupbox.delete_button.setVisible(self.IsGranTable[4])
        self.point_buttons_groupbox.delete_button.clicked.connect(self.delete_point)

        # кнопка выхода
        self.point_buttons_groupbox.ex_button = QPushButton('Выход', self.point_buttons_groupbox)
        self.point_buttons_groupbox.ex_button.resize(100, 30)
        self.point_buttons_groupbox.ex_button.move(10, 130)
        self.point_buttons_groupbox.ex_button.clicked.connect(self.ex_but)

        self.point_param_groupbox = QGroupBox(self)
        self.point_param_groupbox.resize(300, 350)
        self.point_param_groupbox.move(600, 10)
        self.point_param_groupbox.hide()

        # Сумма кредита
        self.point_param_groupbox.label_point = QLabel("Специальность", self.point_param_groupbox)
        self.point_param_groupbox.label_point.move(10, 10)
        self.point_param_groupbox.specialization = QLineEdit(self.point_param_groupbox)
        self.point_param_groupbox.specialization.resize(280, 30)
        self.point_param_groupbox.specialization.move(10, 30)

        # Имя клиента
        self.point_param_groupbox.label_point1 = QLabel("Дата", self.point_param_groupbox)
        self.point_param_groupbox.label_point1.move(10, 150)
        self.point_param_groupbox.date = QDateEdit(self.point_param_groupbox)
        self.point_param_groupbox.date.resize(280, 30)
        self.point_param_groupbox.date.move(10, 170)
        self.point_param_groupbox.date.setCalendarPopup(True)

        # Годовая ставка %
        self.point_param_groupbox.label_point2 = QLabel("Процент выполнения", self.point_param_groupbox)
        self.point_param_groupbox.label_point2.move(10, 80)
        self.point_param_groupbox.completed_percent = QLineEdit(self.point_param_groupbox)
        self.point_param_groupbox.completed_percent.resize(280, 30)
        self.point_param_groupbox.completed_percent.move(10, 100)

        self.point_param_groupbox.label_point3 = QLabel("Студент", self.point_param_groupbox)
        self.point_param_groupbox.label_point3.move(10, 220)
        self.point_param_groupbox.student = QComboBox(self.point_param_groupbox)
        self.point_param_groupbox.student.resize(280, 30)
        self.point_param_groupbox.student.move(10, 240)
        SQL = 'select * from public."result_completed" order by "student"'
        self.current_cursor.execute(SQL)
        self.stud_rows = self.current_cursor.fetchall()
        for elem in self.stud_rows:
            self.point_param_groupbox.student.addItem(elem[1])

        # SQL = 'select * from public."result_completed" order by "student"'
        # self.current_cursor.execute(SQL)
        # student_data = self.current_cursor.fetchall()

        # # Добавление имен студентов в QComboBox
        # for data in student_data:
        #     self.point_param_groupbox.student.addItem(data[1])

        

        self.point_param_groupbox.ok_button = QPushButton('OK', self.point_param_groupbox)
        self.point_param_groupbox.ok_button.resize(100, 30)
        self.point_param_groupbox.ok_button.move(10, 310)
        self.point_param_groupbox.ok_button.clicked.connect(self.ok_point)
        
        self.point_param_groupbox.cancel_button = QPushButton('Отмена', self.point_param_groupbox)
        self.point_param_groupbox.cancel_button.resize(100, 30)
        self.point_param_groupbox.cancel_button.move(130, 310)
        self.point_param_groupbox.cancel_button.clicked.connect(self.cancel_point)

    def con(self):
        self.User = ""
        self.Password = ""
       
        self.connection = psycopg2.connect(user = "Param", password = "123", host = "localhost", port = "5432", database = 'diplom')
        self.current_cursor = self.connection.cursor()
        SQL = 'select * from public."Param"'
        self.current_cursor.execute(SQL)
        Rows = self.current_cursor.fetchall()
        self.IsCaptcha = Rows[0][1] != 0
        self.IsLock = False
        self.DLockTime = 61
        if self.IsCaptcha:
            current_datetime = time.localtime()        
            mkt = time.mktime(current_datetime)
            LocTime = Rows[0][2]
            self.DLockTime = mkt - LocTime
            if self.DLockTime < 60:
                self.IsLock = True

        self.LoginWidg = LoginWidget(self)
        self.LoginWidg.setWindowIcon(QIcon('/home/student/Рабочий стол/Python_SKD/diplom_python/ico.png'))
        while 1:
            self.LoginWidg.exec()
            try :
                self.connection = psycopg2.connect(user = self.User, password = self.Password, host = "localhost", \
                                  port = "5432", database = 'diplom')
                self.current_cursor = self.connection.cursor()
                SQL = 'UPDATE public."Param" SET "IsCaptcha"=0, "LockTime"=0 WHERE "ID"=1'
                self.current_cursor.execute(SQL)
                self.connection.commit()
                break
            except:
                #if self.IsLock:
                #    self.Error("Доступ запрещен")
                #    exit(0)
                current_datetime = time.localtime()        
                mkt = time.mktime(current_datetime)
                if not self.IsCaptcha:
                    mkt = 0
                self.connection = psycopg2.connect(user = "Param", password = "123", host = "localhost", \
                              port = "5432", database = 'diplom')
                self.current_cursor = self.connection.cursor()
                SQL = 'UPDATE public."Param" SET "IsCaptcha"=1, "LockTime"='+str(mkt)+' WHERE "ID"=1'
                self.current_cursor.execute(SQL)
                self.connection.commit()

                if self.IsCaptcha:
                    self.DLockTime = 0
                    self.LoginWidg.StartLock()
                    self.IsLock = True
                    self.LoginWidg.LockShow()
                self.IsCaptcha = True
                self.LoginWidg.CaptchaShow()

        TableName = ['result_completed', 'point_plant'] 
        PrivilegeType = ['INSERT', 'UPDATE', 'DELETE']
        self.IsGranTable = [0,0,0, 0,0,0, 0,0,0]
        for i in range(0, 2) :
            for j in range(0, 2) :
                SQL = "SELECT is_grantable FROM information_schema.table_privileges WHERE grantee='" + self.User + \
                    "' AND table_name='" + TableName[i] + "' AND privilege_type ='" + PrivilegeType[j] + "'"
                self.current_cursor.execute(SQL)
                rows = self.current_cursor.fetchall()
                for elem in rows:
                    for t in elem: # заполняем внутри строки
                        if str(t).strip() == 'YES':
                            self.IsGranTable[3*i+j] = 1 

       

    def ex_but(self):
        self.close()    

    def result_commit(self):
        self.connection.commit()
        self.tableofresult.Reload() 

    def point_commit(self):
        self.connection.commit()
        self.tableofpoint.Reload()    

    def insert_result(self):
        self.result_param_groupbox.show()    
        self.ins = True
        self.result_param_groupbox.student.setText('')
        self.result_param_groupbox.group.setText('')
        self.result_param_groupbox.head.setText('')
        self.result_param_groupbox.report_submitted.setText('')
        self.result_param_groupbox.estimation.setText('')
        self.result_param_groupbox.themes.setText('')

    def update_result(self):
        self.result_param_groupbox.show()
        self.ins = False
        row = self.tableofresult.row
        self.up_result_id = self.tableofresult.item(row, 0).text().strip()
        student = self.tableofresult.item(row, 1).text().strip()  
        group = self.tableofresult.item(row, 2).text().strip()
        head = self.tableofresult.item(row, 3).text().strip()
        report_submitted = self.tableofresult.item(row, 4).text().strip()
        estimation = self.tableofresult.item(row, 5).text().strip()
        themes = self.tableofresult.item(row, 6).text().strip()
        self.result_param_groupbox.student.setText(student)
        self.result_param_groupbox.group.setText(group)
        self.result_param_groupbox.head.setText(head)
        self.result_param_groupbox.report_submitted.setText(report_submitted)
        self.result_param_groupbox.estimation.setText(estimation)
        self.result_param_groupbox.themes.setText(themes)
        self.result_param_groupbox.student.setFocus()

    def delete_result(self):
        row = self.tableofresult.row
        result_id = self.tableofresult.item(row, 0).text().strip()
        student = self.tableofresult.item(row, 1).text().strip()  
        group = self.tableofresult.item(row, 2).text().strip()
        head = self.tableofresult.item(row, 3).text().strip()
        report_submitted = self.tableofresult.item(row, 4).text().strip()
        estimation = self.tableofresult.item(row, 5).text().strip()
        themes = self.tableofresult.item(row, 6).text().strip()

        text = 'Удалить диплом\n'+themes+'?'
        rc = self.Question(text)
        if rc == QMessageBox.Yes:
            SQL1 = 'select * from public."result_completed" WHERE "result_id"='+result_id
            self.current_cursor.execute(SQL1)
            rows = self.current_cursor.fetchall()
            nRows = len(rows)
            if nRows > 0:
                Text2 = 'У студента не сдан диплом.\n \n\nВсе равно удалить студента ?'
                Rc2 = self.Question(Text2)
                if Rc2 == QMessageBox.No:
                    return
            SQL3 = 'delete from public."point_plant" where "result_id"='+result_id   
            self.current_cursor.execute(SQL3) 
            SQL2 = 'DELETE FROM public."result_completed" WHERE "result_id"='+result_id
            self.current_cursor.execute(SQL2)
            self.result_commit()
            row_count = self.tableofresult.rowCount()
            if row >= row_count:
                row = row_count-1
            if row >= 0:
                self.tableofresult.setFocus()
                self.tableofresult.row = row
                self.tableofresult.selectRow(row)
                self.tableofpoint.setRowCount(0)  

    def ok_result(self):
        row = self.tableofresult.row
        student = self.result_param_groupbox.student.text()
        group =  self.result_param_groupbox.group.text()
        head = self.result_param_groupbox.head.text()
        report_submitted = self.result_param_groupbox.report_submitted.text()
        estimation =  self.result_param_groupbox.estimation.text()
        themes = self.result_param_groupbox.themes.text()

        if student == '':
            self.Error('Заполните поле "Студент"')
            return
        if group == '':
            self.Error('Заполните поле "Группа"')
            return
        if head == '':
            self.Error('Заполните поле "Руководитель"')
            return
        if report_submitted == '':
            self.Error('Заполните поле "Отчёт"')
            return
        if estimation == '':
            self.Error('Заполните поле "Оценка"')
            return
        if themes == '':
            self.Error('Заполните поле "Тема"')
            return    
        self.result_param_groupbox.hide()
        #try:
        if self.ins == True:
            #query = "INSERT INTO Client (id, NameOrFIO) SELECT id, %s FROM Client WHERE NameOrFIO = %s"
            SQL = 'INSERT into public."result_completed" ("student", "group", "head", "report_submitted", "estimation", "themes") values (\''+student+'\',\''+group+'\',\''+head+'\',\''+report_submitted+'\',\''+estimation+'\',\''+themes+'\')'
        else:
            SQL = 'UPDATE public."result_completed" SET "student"=\''+student+'\', "group"=\''+group+'\', "head"=\''+head+'\', "report_submitted"= \''+report_submitted+'\', "estimation"=\''+estimation+'\', "themes"=\''+themes+'\' WHERE "result_id"='+self.up_result_id
        self.current_cursor.execute(SQL)

        self.current_cursor.execute('select student from public."result_completed"  where "result_id"='+self.up_result_id)
        results = self.current_cursor.fetchall()
        self.point_param_groupbox.student.clear()
        #self.point_param_groupbox.student.addItems([str(row[0]) for row in results])
        for elem in results:
            self.point_param_groupbox.student.addItem(elem[0])

        self.result_commit()
        self.FindRowInTable(self.tableofresult, [1,2,3,4,5,6], [student, group, head, report_submitted, estimation, themes])  
        if self.ins == True:
            self.tableofpoint.setRowCount(0)           
    
    def cancel_result(self):
        self.result_param_groupbox.hide()  

    def insert_point(self):
        self.point_param_groupbox.show()    
        self.ins = True
        self.point_param_groupbox.student.currentText()
        self.point_param_groupbox.specialization.setText('')
        self.point_param_groupbox.date.setDate(QDate.currentDate())
        self.point_param_groupbox.completed_percent.setText('')
        self.point_param_groupbox.student.setEditable(True)
        self.point_param_groupbox.student.setEnabled(True)


    def update_point(self):
        self.point_param_groupbox.show()
        self.ins = False
        row = self.tableofpoint.row
        self.up_point_id = self.tableofpoint.item(row, 1).text().strip()
        specialization = self.tableofpoint.item(row, 2).text().strip()  
        date = self.tableofpoint.item(row, 3).text().strip()
        completed_percent = self.tableofpoint.item(row, 4).text().strip()
        date1 = QDate.fromString(date, "dd.MM.yyyy")
        self.point_param_groupbox.specialization.setText(specialization)
        self.point_param_groupbox.date.setDate(date1)
        self.point_param_groupbox.completed_percent.setText(completed_percent)
        self.point_param_groupbox.date.setFocus()
        self.point_param_groupbox.date.setDate(QDate.currentDate())
        self.point_param_groupbox.student.setEditable(False)
        self.point_param_groupbox.student.setEnabled(False)



    def delete_point(self):
        row = self.tableofpoint.row
        point_id = self.tableofpoint.item(row, 1).text().strip()
        specialization = self.tableofpoint.item(row, 2).text().strip()  
        date = self.tableofpoint.item(row, 3).text().strip()
        completed_percent = self.tableofpoint.item(row, 4).text().strip()

        text = 'Удалить контрольную точку\n'+date+'?'
        rc = self.Question(text)
        if rc == QMessageBox.Yes:
            SQL1 = 'select * from public."point_plant" WHERE "point_id"='+point_id
            self.current_cursor.execute(SQL1)
            rows = self.current_cursor.fetchall()
            nRows = len(rows)
            if nRows > 0:
                Text2 = 'Вы уверенны.\n \n\nВсе равно удалить контрольную точку?'
                Rc2 = self.Question(Text2)
                if Rc2 == QMessageBox.No:
                    return
            SQL2 = 'DELETE FROM public."point_plant" WHERE "point_id"='+point_id
            self.current_cursor.execute(SQL2)
            self.point_commit()
            row_count = self.tableofpoint.rowCount()
            if row >= row_count:
                row = row_count-1
            if row >= 0:
                self.tableofpoint.setFocus()
                self.tableofpoint.row = row
                self.tableofpoint.selectRow(row)   

    def ok_point(self):
        row = self.tableofpoint.row
        selected_student = self.point_param_groupbox.student.currentText()
        specialization = self.point_param_groupbox.specialization.text()
        date =  self.point_param_groupbox.date.date()
        date_true = date.toString("dd.MM.yyyy")
        completed_percent = self.point_param_groupbox.completed_percent.text()


        if specialization == '':
            self.Error('Заполните поле "Специальность"')
            return
        if date == '':
            self.Error('Заполните поле "Дата"')
            return
        if completed_percent == '':
            self.Error('Заполните поле "Процент выполнения"')
            return   
        self.point_param_groupbox.hide()
        #try:
        SQL_select = 'SELECT result_id FROM public."result_completed" WHERE "result_completed"."student"= %s'
        self.current_cursor.execute(SQL_select, (selected_student,))
        result_id = self.current_cursor.fetchone()[0]
        if self.ins == True:
            SQL_insert = 'INSERT into public."point_plant" ("specialization", "date", "completed_percent", "result_id") values (%s, %s, %s, %s)'
            values = (specialization, date_true, completed_percent, result_id)
        else:
            SQL_update = 'UPDATE public."point_plant" SET "specialization"=%s, "date"=%s, "completed_percent"=%s WHERE "point_id"=%s'
            values = (specialization, date_true, completed_percent, self.up_point_id)

        if self.ins == True:
            self.current_cursor.execute(SQL_insert, values)
        else:
            self.current_cursor.execute(SQL_update, values)

           
        self.point_commit() 

    def cancel_point(self):
        self.point_param_groupbox.hide()

    # Изменение размера окна
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        w = self.width()
        h = self.height()
        self.tableofresult.resize(w//4+519, h//3-20)
        self.tableofpoint.resize(w//5+45, h//2-20)
        self.tableofresult.move(w//13, 90)
        self.tableofpoint.move(w//13, 520)
        self.result_buttons_groupbox.move(w//2+190, 85)
        self.result_param_groupbox.move(w//2+342, 85)
        self.point_buttons_groupbox.move(w//5+197, 515)
        self.point_param_groupbox.move(w//4+253, 515)
        self.point_plant_label.move(w//13, h//3+150)
        self.result_label.move(w//13, 60)

        return super().resizeEvent(a0)


    # обработка ошибок
    def Error(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
    # вопрос
    def Question(self, Text):        
        msg = QMessageBox()
        msg.setWindowTitle("Вопрос")
        msg.setText(Text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        return msg.exec_()
    
    #находим строку в таблице и делаем ее текущей
    def FindRowInTable(self, table, col_numbers, values):
        for irow in range(table.rowCount()):
            f = True
            i = 0
            for ColNum in col_numbers:
                item = table.item(irow, ColNum)
                s = item.text()
                if s != values[i]:
                    f = False
                    break
                i+=1
            if f:
                table.setFocus()
                table.row = irow
                table.selectRow(irow)
                break 


class TABLE_OF_RESULT(QTableWidget):
    def __init__(self, ParentWindow):
        self.ParentWindow = ParentWindow  # запомнить окно, в котором эта таблица показывается
        super().__init__(ParentWindow)
        self.setGeometry(10, 30, 1000, 300)
        self.setColumnCount(7)
        self.setColumnHidden(0, True)
        self.verticalHeader().hide()
        self.Reload() # обновить таблицу
        self.selectRow(0)
        if self.rowCount() > 1:
            self.ParentWindow.result_id = self.item(0, 0).text().strip()
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелчка мыши в таблице
        self.row = 0 
        # self.setColumnWidth(2, 200)
        # self.setColumnWidth(3, 300)   

    # обновление таблицы
    def Reload(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['ID','Студент', 'Группа', 'Руководитель', 'Отчёт', 'Оценка', 'Тема']) # заголовки столцов
        self.ParentWindow.current_cursor.execute('select * from public."result_completed" order by "student", "group", "head", "report_submitted", "estimation", "themes"')
        rows = self.ParentWindow.current_cursor.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()
        self.row = 0

    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.row = row
        self.selectRow(row)
        self.ParentWindow.result_id = self.ParentWindow.tableofresult.item(row, 0).text().strip()
        self.ParentWindow.tableofpoint.Reload()
        self.ParentWindow.tableofpoint.selectRow(0)

    def keyPressEvent (self, e):
        if e.key() == Qt.Key_Insert:
           self.ParentWindow.insert_result()
        if e.key() == Qt.Key_Return:
           self.ParentWindow.update_result()
        if e.key() == Qt.Key_Delete:
           self.ParentWindow.delete_result()
        if e.key() == Qt.Key_Home:
           self.row = 0
           self.selectRow(0)
        if e.key() == Qt.Key_End:
           self.row = self.rowCount()-1
           self.selectRow(self.rowCount()-1)
        if e.key() == Qt.Key_Down:
           Row = self.row+1
           self.row = Row
           self.selectRow(Row)
        if e.key() == Qt.Key_Up:
           Row = self.row-1
           self.row = Row
           self.selectRow(Row)
        if e.key() == Qt.Key_Escape:
           self.ParentWindow.cancel_result()   

class TABLE_OF_POINT(QTableWidget):
    def __init__(self, ParentWindow):
        self.ParentWindow = ParentWindow  # запомнить окно, в котором эта таблица показывается
        super().__init__(ParentWindow)
        self.setGeometry(10, 30, 100, 100)
        self.setColumnCount(6)
        self.setColumnHidden(0, True)
        self.setColumnHidden(1, True)
        self.verticalHeader().hide()
        self.Reload() # обновить таблицу
        self.selectRow(0)
        if self.rowCount() > 1:
            self.ParentWindow.point_id = self.item(0, 0).text().strip()
        self.setEditTriggers(QTableWidget.NoEditTriggers) # запретить изменять поля
        self.cellClicked.connect(self.cellClick)  # установить обработчик щелчка мыши в таблице
        self.row = 0 
        # self.setColumnWidth(2, 200)
        # self.setColumnWidth(3, 300)   

    # обновление таблицы
    def Reload(self):
        self.clear()
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['ID','id2' ,'Специальность', 'Дата', 'Процент выполнения', 'Студент']) # заголовки столцов
        SQL= 'select public."point_plant"."result_id", "point_id", "specialization", "date", "completed_percent", "student" from public."point_plant", public."result_completed" where public."result_completed"."result_id" = public."point_plant"."result_id" and public."point_plant"."result_id"='+self.ParentWindow.result_id+''
        #SQL = 'select * from point_plant'
        self.ParentWindow.current_cursor.execute(SQL)
        rows = self.ParentWindow.current_cursor.fetchall()
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()
        self.row = 0

    def cellClick(self, row, col): # row - номер строки, col - номер столбца
        self.row = row
        self.selectRow(row)
        #self.ParentWindow.result_id = self.ParentWindow.tableofresult.item(row, 0).text().strip()
        #self.ParentWindow.TableOfCredit.Reload()
        #self.ParentWindow.TableOfCredit.selectRow(0)

    def keyPressEvent (self, e):
        if e.key() == Qt.Key_Insert:
           self.ParentWindow.insert_point()
        if e.key() == Qt.Key_Return:
           self.ParentWindow.update_point()
        if e.key() == Qt.Key_Delete:
           self.ParentWindow.delete_point()
        if e.key() == Qt.Key_Home:
           self.row = 0
           self.selectRow(0)
        if e.key() == Qt.Key_End:
           self.row = self.rowCount()-1
           self.selectRow(self.rowCount()-1)
        if e.key() == Qt.Key_Down:
           Row = self.row+1
           self.row = Row
           self.selectRow(Row)
        if e.key() == Qt.Key_Up:
           Row = self.row-1
           self.row = Row
           self.selectRow(Row)
        if e.key() == Qt.Key_Escape:
           self.ParentWindow.cancel_point() 

app = QApplication(sys.argv)
ex = DiplomWindow()
ex.showMaximized()
ex.setWindowIcon(QIcon('/home/student/Рабочий стол/Python_SKD/diplom_python/ico.png'))
sys.exit(app.exec_())            
