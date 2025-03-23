import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QListWidget, QMessageBox, QLabel
from PyQt6.QtGui import QFont

class RenomeadorArquivos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Renomeador de Arquivos")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #f4f4f4;")

        layout = QVBoxLayout()
        
        self.label_diretorio = QLabel("Selecione a pasta:")
        self.label_diretorio.setStyleSheet("padding: 5px; color: #000;")
        self.label_diretorio.setFont(QFont("Arial", 10))
        layout.addWidget(self.label_diretorio)
        
        self.entrada_diretorio = QLineEdit()
        self.entrada_diretorio.setStyleSheet("padding: 5px; color: #000;")
        layout.addWidget(self.entrada_diretorio)
        
        self.btn_selecionar = QPushButton("Selecionar")
        self.btn_selecionar.setStyleSheet("background-color: #007BFF; color: white; padding: 5px;")
        self.btn_selecionar.clicked.connect(self.selecionar_diretorio)
        layout.addWidget(self.btn_selecionar)
        
        self.label_texto_remover = QLabel("Texto a remover:")
        self.label_texto_remover.setStyleSheet("padding: 5px; color: #000;")
        self.label_texto_remover.setFont(QFont("Arial", 10))
        layout.addWidget(self.label_texto_remover)
        
        self.entrada_texto_remover = QLineEdit()
        self.entrada_texto_remover.setStyleSheet("padding: 5px; color: #000;")
        layout.addWidget(self.entrada_texto_remover)
        
        self.btn_renomear = QPushButton("Renomear Arquivos")
        self.btn_renomear.setStyleSheet("background-color: #28A745; color: white; padding: 5px;")
        self.btn_renomear.clicked.connect(self.renomear_arquivos)
        layout.addWidget(self.btn_renomear)
        
        self.lista_arquivos = QListWidget()
        self.lista_arquivos.setStyleSheet("color: black; background-color: white;")  
        layout.addWidget(self.lista_arquivos)
        
        self.setLayout(layout)

    def selecionar_diretorio(self):
        diretorio = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
        if diretorio:
            self.entrada_diretorio.setText(diretorio)

    def exibir_mensagem(self, titulo, texto, icone):
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(texto)
        msg.setIcon(icone)

        msg.setStyleSheet("""
             QMessageBox {
                 font-size: 14px;
                 font-family: Arial;
                 color: black; 
             }
             QLabel {
                  color: black;
             }
             QPushButton {
                  background-color: #ff5555;
                  color: white; 
                  border-radius: 5px;
                  padding: 5px;
             }
             QPushButton:hover {
                 background-color: #ff2222;
             }
        """)

        msg.exec()

    def renomear_arquivos(self):
        diretorio = self.entrada_diretorio.text()
        texto_remover = self.entrada_texto_remover.text().strip()

        if not os.path.isdir(diretorio):
            self.exibir_mensagem("Erro", "Selecione um diretório válido!", QMessageBox.Icon.Critical)
            return
        
        if not texto_remover:
            self.exibir_mensagem("Erro", "Digite o texto a ser removido!", QMessageBox.Icon.Critical)
            return
        
        arquivos_renomeados = []
        for nome_arquivo in os.listdir(diretorio):
            if texto_remover in nome_arquivo:
                novo_nome = nome_arquivo.replace(texto_remover, "").strip()
                caminho_antigo = os.path.join(diretorio, nome_arquivo)
                caminho_novo = os.path.join(diretorio, novo_nome)
                os.rename(caminho_antigo, caminho_novo)
                arquivos_renomeados.append(novo_nome)
        
        self.lista_arquivos.clear()
        if arquivos_renomeados:
            self.lista_arquivos.addItems(arquivos_renomeados)
            self.exibir_mensagem("Sucesso", "Arquivos renomeados com sucesso!", QMessageBox.Icon.Information)
        else:
            self.exibir_mensagem("Aviso", "Nenhum arquivo foi renomeado.", QMessageBox.Icon.Warning)

if __name__ == "__main__":
    app = QApplication([])
    janela = RenomeadorArquivos()
    janela.show()
    app.exec()
