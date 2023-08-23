import sys
from PyQt5.QtWidgets import *
from recursos.prediccion import predict_disease_voting
import os

class DiseaseDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Detección de Enfermedades en Hojas de Cítricos'
        self.correct_predictions = 0  #Contador para cantidad de predicciones correctas
        self.total_predictions = 0    #Contador para cantidad total de predicciones
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        
        layout = QVBoxLayout()
        
        #Botón para cargar carpeta con imágenes
        self.loadButton = QPushButton('Seleccionar carpeta', self)
        self.loadButton.clicked.connect(self.loadImages)
        layout.addWidget(self.loadButton)
        
        #Tabla para mostrar resultados
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)
        
        #Etiqueta para mostrar el porcentaje de efectividad
        self.accuracyLabel = QLabel("Porcentaje de efectividad: 0%")
        layout.addWidget(self.accuracyLabel)
        
        self.setLayout(layout)
        
    def loadImages(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        
        if folder_path:
            #Se reinician los contadores
            self.correct_predictions = 0
            self.total_predictions = 0

            #Se obtienen todas las imágenes en la carpeta seleccionada
            images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            #Se configura la tabla
            self.tableWidget.setRowCount(len(images))
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(['Nombre Imagen', 'Enfermedad'])
            
            #Lista de modelos
            model_paths = ['recursos/Neural_Net_7.joblib', 'recursos/Linear_SVM_63.joblib', 'recursos/LogisticRegression_63.joblib']
            
            for index, image in enumerate(images):
                image_path = os.path.join(folder_path, image)
                disease = predict_disease_voting(image_path, model_paths)
                
                self.tableWidget.setItem(index, 0, QTableWidgetItem(image))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(disease))
                
                #Se compara la predicción con la primera parte del nombre de la imagen
                true_label = image.split("_")[0]
                self.total_predictions += 1
                if true_label == disease:
                    self.correct_predictions += 1
            
            #Se calcula y se muestra el porcentaje de efectividad
            accuracy = (self.correct_predictions / self.total_predictions) * 100
            self.accuracyLabel.setText(f"Porcentaje de efectividad: {accuracy:.2f}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiseaseDetectionApp()
    ex.show()
    sys.exit(app.exec_())
