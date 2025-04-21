import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt


class ZipApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ウィンドウの設定
        self.setWindowTitle("フォルダをドラッグ＆ドロップで追加")
        self.setGeometry(100, 100, 600, 400)

        # ドラッグ＆ドロップを有効にする
        self.setAcceptDrops(True)

        # レイアウトを作成
        layout = QVBoxLayout()
        

        # ラベルを追加
        self.label = QLabel("ドラッグ＆ドロップでフォルダを追加してください。")
        self.label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.label)

        # フォルダリストのウィジェット
        self.folderList = QListWidget()
        self.folderList.setSelectionMode(QListWidget.ExtendedSelection)
        self.folderList.setAcceptDrops(True)
        layout.addWidget(self.folderList)


        # buttonLayout（横並び用）を定義
        buttonLayout = QHBoxLayout()

        # 圧縮ボタンを追加
        self.zipButton = QPushButton("ZIPに梱包")
        self.zipButton.clicked.connect(self.compressFolders)
        buttonLayout.addWidget(self.zipButton)

        # リセットボタンを追加
        self.resetButton = QPushButton("リセット")
        self.resetButton.clicked.connect(self.resetList)
        buttonLayout.addWidget(self.resetButton)

        # チェックボックスを追加
        self.optionCheck = QCheckBox("アプリと同じ場所に保存")
        buttonLayout.addWidget(self.optionCheck)

        # 横並びのボタン行をメイン縦レイアウトに追加
        layout.addLayout(buttonLayout)


        # レイアウトをウィンドウにセット
        self.setLayout(layout)

    # ドラッグされたデータがウィンドウ領域に入ったときのイベント
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # ドラッグデータがURL形式であれば受け入れる
            event.accept()
        else:
            event.ignore()

    # ドラッグされたデータがウィンドウ内にドロップされたときのイベント
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            folder_path = url.toLocalFile()  # ドロップされたパスを取得
            if os.path.isdir(folder_path):  # フォルダのみを受け付ける
                self.folderList.addItem(folder_path)  # フォルダをリストに追加

    # リスト内のフォルダを順にZIP化
    def compressFolders(self):
        for i in range(self.folderList.count()):
            folder_path = self.folderList.item(i).text()  # フォルダパスを取得
            zip_name = os.path.basename(folder_path) + ".zip"  # ZIPファイル名を作成

            # チェックボックスの状態で保存先を変更
            if self.optionCheck.isChecked():
                zip_path = os.path.join(os.getcwd(), zip_name)  # アプリと同じ場所
            else:
                zip_path = os.path.join(os.path.dirname(folder_path), zip_name)  # 元のフォルダと同じ場所

            # 進行状況をラベルに表示
            self.label.setText(f"{zip_name} を作成中...")

            # 7zipを使用して無圧縮ZIPを作成(7zipの保存先が違う場合はここを編集)
            subprocess.run(["D:\\Program Files\\7-Zip\\7z.exe", "a", "-tzip", "-mx=0", zip_path, os.path.join(folder_path, "*")], shell=True)


        # 全ての処理が完了したら完了メッセージを表示
        self.label.setText("梱包完了！")

    #リセット
    def resetList(self):
        self.folderList.clear()

    #デリート
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_items = self.folderList.selectedItems()
            for item in selected_items:
                self.folderList.takeItem(self.folderList.row(item))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZipApp()
    window.show()
    sys.exit(app.exec_())
