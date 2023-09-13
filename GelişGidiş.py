import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget

class GunlukUygulama(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Günlük Geliş Gidiş Listesi")
        self.setGeometry(100, 100, 400, 400)

        self.initUI()

        self.conn = sqlite3.connect("gunluk.db")
        self.create_table()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.tarih_label = QLabel("Tarih:")
        self.plaka_label = QLabel("Plaka:")
        self.nereden_label = QLabel("Nereden Geldi:")
        self.nereye_label = QLabel("Nereye Gidiyor:")
        self.getirdi_label = QLabel("Ne Getirdi:")
        self.goturdu_label = QLabel("Ne Götürüyor:")

        self.tarih_input = QLineEdit()
        self.plaka_input = QLineEdit()
        self.nereden_input = QLineEdit()
        self.nereye_input = QLineEdit()
        self.getirdi_input = QLineEdit()
        self.goturdu_input = QLineEdit()

        self.kaydet_button = QPushButton("Kaydet")
        self.kaydet_button.clicked.connect(self.kaydet)

        self.yeni_button = QPushButton("Yeni")
        self.yeni_button.clicked.connect(self.yeni_liste)

        self.liste_widget = QListWidget()

        self.layout.addWidget(self.tarih_label)
        self.layout.addWidget(self.tarih_input)
        self.layout.addWidget(self.plaka_label)
        self.layout.addWidget(self.plaka_input)
        self.layout.addWidget(self.nereden_label)
        self.layout.addWidget(self.nereden_input)
        self.layout.addWidget(self.nereye_label)
        self.layout.addWidget(self.nereye_input)
        self.layout.addWidget(self.getirdi_label)
        self.layout.addWidget(self.getirdi_input)
        self.layout.addWidget(self.goturdu_label)
        self.layout.addWidget(self.goturdu_input)
        self.layout.addWidget(self.kaydet_button)
        self.layout.addWidget(self.yeni_button)
        self.layout.addWidget(self.liste_widget)

        self.central_widget.setLayout(self.layout)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gunluk (
                            tarih TEXT,
                            plaka TEXT,
                            nereden TEXT,
                            nereye TEXT,
                            getirdi TEXT,
                            goturdu TEXT
                            )''')
        self.conn.commit()

    def kaydet(self):
        tarih = self.tarih_input.text()
        plaka = self.plaka_input.text()
        nereden = self.nereden_input.text()
        nereye = self.nereye_input.text()
        getirdi = self.getirdi_input.text()
        goturdu = self.goturdu_input.text()

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO gunluk VALUES (?, ?, ?, ?, ?, ?)",
                       (tarih, plaka, nereden, nereye, getirdi, goturdu))
        self.conn.commit()

        self.tarih_input.clear()
        self.plaka_input.clear()
        self.nereden_input.clear()
        self.nereye_input.clear()
        self.getirdi_input.clear()
        self.goturdu_input.clear()

        self.liste_guncelle()

    def yeni_liste(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS gunluk_yeni AS SELECT * FROM gunluk")
        cursor.execute("DELETE FROM gunluk")
        self.conn.commit()
        self.liste_guncelle()

    def liste_guncelle(self):
        self.liste_widget.clear()
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM gunluk")
        veriler = cursor.fetchall()
        for veri in veriler:
            self.liste_widget.addItem(f"Tarih: {veri[0]}, Plaka: {veri[1]}, Nereden: {veri[2]}, Nereye: {veri[3]}, Getirdi: {veri[4]}, Götürdü: {veri[5]}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = GunlukUygulama()
    uygulama.show()
    sys.exit(app.exec_())
