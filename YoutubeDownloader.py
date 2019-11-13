import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QDesktopWidget, QMessageBox, QCheckBox, \
    QLineEdit,QListWidgetItem
from pytube import YouTube # !pip install pytube
from PyQt5.QtWidgets import QLabel, QComboBox, QProgressBar, QListWidget,QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal, QFile
import time
import YoutubeCrawl
import processed_classification
import os


class YoutubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.Youtube_info = YoutubeCrawl.Youtube()
        self.processed = processed_classification.ProcessSentence()

    def initUI(self):
        self.center()
        self.setGeometry(500, 500, 600, 500)
        ## Button
        self.saveBTN = QPushButton("저장", self)
        self.saveBTN.setGeometry(490, 400, 80,55)
        self.saveBTN.clicked.connect(self.save_cmd)

        self.searchBTN = QPushButton("검색", self)
        self.searchBTN.setGeometry(520, 10, 50, 35)
        self.searchBTN.clicked.connect(self.search_cmd)

        self.dir_pathBTN = QPushButton("폴더", self)
        self.dir_pathBTN.setGeometry(490, 370, 80,30)
        self.dir_pathBTN.clicked.connect(self.path_select)

        self.quality_BTN = QPushButton('해상도 보기',self)
        self.quality_BTN.setGeometry(300,400,80,20)
        self.quality_BTN.clicked.connect(self.quality_add)
        ##
        # Label
        self.path_label = QLabel("경로 : ", self)
        self.path_label.move(50, 370)

        self.quality_label = QLabel("해상도 : ", self)
        self.quality_label.move(50, 400)
        ##
        # TextBox
        self.path_textbox = QLineEdit(self)
        self.path_textbox.setGeometry(90, 370, 365, 20)

        self.search_word_textbox = QLineEdit(self)
        self.search_word_textbox.setGeometry(50,10,420,30)
        ##

        # CheckBox
        self.auto_checkbox = QCheckBox("자동분류", self)
        self.auto_checkbox.move(390, 400)

        # ComboBox
        self.quality_combobox = QComboBox(self)
        self.quality_combobox.setGeometry(90, 400,200,20)


        self.progress = QProgressBar(self)
        self.progress.setGeometry(90, 430, 400, 25)
        self.progress.setMaximum(100)


        self.titleQListWidget = QListWidget(self)
        self.titleQListWidget.setGeometry(50,50,520,300)
        self.titleQListWidget.currentItemChanged.connect(self.get_title)

        self.show()


    def path_select(self):
        self.file_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.path_textbox.setText(self.file_path)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_cmd(self):
        self.download_stream = self.streams[self.combos[self.quality_combobox.currentText()]]

        X = self.processed.sent_to_vec(self.download_stream.title)
        print(X)
        # if os.path.isdir("{}/{}".format(self.path_textbox.text(), self.processed.predict(X))) == False:
        #     os.mkdir("{}/{}".format(self.path_textbox.text(), self.processed.predict(X)))
        #
        # self.download_stream.download("{}/{}".format(self.path_textbox.text(), self.processed.predict(X)))

    def search_cmd(self):
        self.progress.setValue(70)
        self.titleQListWidget.clear()
        self.title_href_dict = self.Youtube_info.search(self.search_word_textbox.text())
        self.titleQListWidget.addItems(list(self.title_href_dict.keys()))
        self.progress.setValue(100)

    def get_title(self):
        try: # 리스트에 item을 클릭하고 검색시 알 수 없는 오류. 아마, currentItem이 가르키는 주소값이 변경되어서 그런것으로 의심됨.
            self.select_title = self.titleQListWidget.currentItem().text()
            print(self.select_title)
        except:
            pass

    def progress_function(self,stream, chunk, file_handle, bytes_remaining):
        self.progress.setValue(int((1 - bytes_remaining / self.download_stream.filesize) * 100))


    def quality_add(self):
        self.quality_combobox.clear()
        self.progress.setValue(30)
        try:
            yt = YouTube('https://www.youtube.com'+self.title_href_dict[self.select_title], on_progress_callback=self.progress_function)
        except:
            print('error')
        # 유튜브의 description을 보고 분류.
        self.streams = yt.streams.all()

        self.combos = dict()

        for idx, stream in enumerate(self.streams):
            if 'video/mp4' in stream.mime_type:
                self.combos['{} {} {} {}MB'.format(stream.mime_type, stream.resolution, stream.fps,
                                                     round(stream.filesize / (1024 * 1024)))] = idx

            elif 'audio/mp4' in stream.mime_type:
                self.combos['{} {}'.format(stream.mime_type, stream.abr)] = idx

        self.quality_combobox.addItems(list(self.combos.keys()))
        self.progress.setValue(100)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YoutubeDownloader()
    sys.exit(app.exec_())