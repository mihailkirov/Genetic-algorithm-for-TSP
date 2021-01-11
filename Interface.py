# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
import PVC_Algo_Genetique as pvc
import Dialogue

class Bouton(QtWidgets.QPushButton):
    def __init__(self, nom, chemin, parent = 0):
        super().__init__(QtGui.QIcon(chemin),"", parent)
        self.setMinimumSize(QtCore.QSize(0, 40))
        self.setObjectName(nom)

class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, population, mutrate, elith, nmbsgenes, divers, parent = 0):
        super().__init__(parent)
        popinit = pvc.init_population(nmbsgenes, population)
        self.algg = pvc.algo_genetique(popinit, population, mutrate, elith, nmbsgenes, divers)
        self.setSceneRect(-200, -200, 400, 400)
        W = pvc.Tournee.calcul_window()

        # self.L : Liste de points représentant les coordonnées des villes converties 
        # dans les dimensions des l'espace écran
        self.L = self.transformation_coord(W)



    def projection(self, pos, window, view):
        """ Fonction permettant de projeter un point de coordonné 'pos' situé dans
        l'espace euclidien dans l'espace de la viewport. """

        x, y = pos
        owx, owy = window[0]
        dwx, dwy = window[1]
        ovx, ovy = view[0]
        dvx, dvy = view[1]

        return ((((x - owx) / dwx) * dvx) + ovx), ((((y - owy) / dwy) * dvy) + ovy)

    def affichage_chemin(self, nbs = 10):
        """ Affiche les nbs chemins du plus court (vert) au plus long (rouge)"""

        # Extraction d'une population
        self.pop_courante = next(self.algg)
        tournees = self.pop_courante.individus[:nbs]

        pas = int(255/nbs)
        n = pvc.Tournee.get_taille()
        for i in range(nbs):
            T = tournees[i].get_liste_gene()
            pinceau = QtGui.QPen(QtGui.QColor(255 - pas*i, pas*i, 0))
            for j in range(n):
                self.addLine(self.L[T[j]][0], self.L[T[j]][1], self.L[T[(j + 1) %n]][0], self.L[T[(j
                + 1)%n]][1], pinceau)

        return tournees[0].get_liste_gene()

    def calcul_fitness(self):
        return float(self.pop_courante)
    
    # Affiche graphiquement villes
    # ------------------------------------------------------------------------                 
    def affichage_villes(self):
        """ Méthode affichant les villes du domaine en convertissant leur 
        coordonnées de l'espace euclidien vers l'espace écran """

        
        # self.L : Liste de points représentant les coordonnées des villes converties 
        # dans les dimensions des l'espace écran
        for point in self.L:
            pinceau = QtGui.QPen(QtCore.Qt.red)
            self.addEllipse(point[0], point[1], 3, 3, pinceau)


    def transformation_coord(self, W):
        L = []
        for i in range(pvc.Tournee.get_taille()):
            ville = pvc.Tournee.get_Domaine(i)
            L.append((ville.get_x(), ville.get_y()))

        x = self.sceneRect().x()
        y = self.sceneRect().y()
        w = self.sceneRect().width()
        h =self.sceneRect().height()
        V = [(x, y), (w, h)]
        return [self.projection(e, W, V) for e in L]

# Classe de la fenêtre principale
# ----------------------------------------------------------------------------
class MainWindow(QtWidgets.QMainWindow):
    """ Classe de la fenêtre de simulation. """
    def __init__(self):
        super().__init__()
        self.setObjectName("TSP Genetic Algorithm")
        self.delai = 1000
        self.generation = 0

        self.resize(866, 643)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, 14, -1)
        self.horizontalLayout_3.setSpacing(40)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("population")

        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.horizontalLayout_3.addWidget(self.lineEdit_4)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setMinimumSize(QtCore.QSize(70, 0))

        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setMinimumSize(QtCore.QSize(70, 0))

        self.horizontalLayout_3.addWidget(self.checkBox)
        self.horizontalLayout_3.addWidget(self.checkBox_1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        
        # Espace ou sera affiché les tournées
        self.Tour_view = QtWidgets.QWidget()
        self.Tour_view.setObjectName("Tour_view")
        self.tour_view_layout = QtWidgets.QVBoxLayout(self.Tour_view)

        self.graphicsView = QtWidgets.QGraphicsView(self.Tour_view)
        self.timer = QtCore.QTimer(self.graphicsView)
        self.timer.setObjectName("temps")

        self.tour_view_layout.addWidget(self.graphicsView)
        self.graphicsView.setObjectName("graphicsView")
        self.tabWidget.addTab(self.Tour_view, "")

        # Espace d'affichage des courbes des moyennes de chaque génération
        self.Chart_view = QtWidgets.QWidget()
        self.Chart_view.setObjectName("Chart_view")
        self.chart_view_layout = QtWidgets.QVBoxLayout(self.Chart_view)

        self.graph = QtChart.QChartView(self.Chart_view)
        self.chart_view_layout.addWidget(self.graph)
        self.graph.setObjectName("graphicsView_2")

        self.tabWidget.addTab(self.Chart_view, "")
        self.serie = QtChart.QLineSeries()
        self.graph.chart().setTitle("Fitness average generation chart")
        self.graph.chart().setAnimationOptions(QtChart.QChart.AllAnimations);
        self.graph.chart().addSeries(self.serie)
        self.graph.chart().createDefaultAxes()
        self.graph.chart().axisY().setRange(0, 1)

        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(1)
     
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(250, 0))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.vertical_group_layout = QtWidgets.QFormLayout(self.groupBox)

        self.round_l = QtWidgets.QTextEdit(self.groupBox)
        self.printfitness = QtWidgets.QLineEdit(self.groupBox)
        self.vertical_group_layout.addRow("Round List", self.round_l)
        self.vertical_group_layout.addRow("Average Fitness", self.printfitness)

        self.horizontalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_2.setStretch(0,1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(46, 0, -1, -1)
        self.horizontalLayout.setSpacing(19)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Bouton lecture
        self.pushButton_4 = Bouton("play", "play.png", 
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton_4)

        # Bouton pause
        self.pushButton_5 = Bouton("pause", "pause.png",
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton_5)

        # Bouton stop
        self.pushButton = Bouton("stop", "stop.png",
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton)

        # Bouton retour en arrière
        self.pushButton_2 = Bouton("rewind", "rewind.png",
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton_2)

        # Bouton avancer
        self.pushButton_3 = Bouton("forward", "forward.png",
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton_3)

        # Bouton relancer
        self.pushButton_6 = Bouton("repeat", "repeat.png",
        self.centralwidget)
        self.horizontalLayout.addWidget(self.pushButton_6)

        spacerItem = QtWidgets.QSpacerItem(294, 40, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 7)
        self.setCentralWidget(self.centralwidget)

        # Barre d'outils
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 866, 26))
        self.menubar.setObjectName("menubar")

        # Menu fichier
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier") 

        # Menu aide
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # Menu d'ouverture de fichier
        self.actionOuvrir = QtWidgets.QAction(self)
        self.actionOuvrir.setObjectName("actionOpen")

        self.actionQuitter = QtWidgets.QAction(self)
        self.actionQuitter.setObjectName("actionQuit")

        # Affichage des informations concernant l'application
        self.actionA_propos = QtWidgets.QAction(self)
        self.actionA_propos.setObjectName("actionAbout")
        
        self.actionHelp = QtWidgets.QAction(self)
        self.actionHelp.setObjectName("actionHelp")
        
        # Menu pour sauvegarder
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
       
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSave)
        self.menuFichier.addAction(self.actionQuitter)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionA_propos)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        # Creation de la fenetre de dialogue
        self.dialogue = Dialogue.Dialog(self)

        # Eteindre les boutons liées au contrôle au A.G durant son 
        # fonctionnement 
        self.eteindre_boutons()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    # Traduction des noms et textes
    def retranslateUi(self):
        """ Méthode de traduction des noms et textes. """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "TSP Genetic Algorithm"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", " Population"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Mutation rate"))
        self.checkBox.setText(_translate("MainWindow", "Elitism"))
        self.checkBox_1.setText(_translate("MainWindow", "Diversification"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tour_view), 
        _translate("MainWindow", "Tour view"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Chart_view), 
        _translate("MainWindow", "Chart view"))
        
        self.groupBox.setTitle(_translate("MainWindow", "Generation data"))

        self.pushButton_4.setToolTip(_translate("MainWindow", "Run"))
        self.pushButton_5.setToolTip(_translate("MainWindow", "Pause"))
        self.pushButton.setToolTip(_translate("MainWindow", "Stop"))
        self.pushButton_2.setToolTip(_translate("MainWindow", "Previous generation"))
        self.pushButton_3.setToolTip(_translate("MainWindow", "Next generation"))
        self.pushButton_6.setToolTip(_translate("MainWindow", "Restart"))

        self.menuFichier.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        self.actionOuvrir.setText(_translate("MainWindow", "Open..."))
        self.actionOuvrir.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionQuitter.setText(_translate("MainWindow", "Quit"))
        self.actionQuitter.setShortcut(_translate("MainWindow", "Alt+F4"))
        self.actionA_propos.setText(_translate("MainWindow", "About"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))


    
    # Gestion des évènements avec la souris
    # ------------------------------------------------------------------------

    # Appuie sur le bouton relancer
    @QtCore.pyqtSlot()
    def on_repeat_clicked(self):
        """ Relance l'algorithme. """
        self.timer.stop()
        self.generation = 0
        self.serie.clear()
        self.lancement_algo()

    @QtCore.pyqtSlot()
    def on_stop_clicked(self):
        """ Arrête l'algrithme. """
        self.timer.stop()
        self.eteindre_boutons()
        self.generation = 0

    # Appuie sur le bouton pause
    @QtCore.pyqtSlot() 
    def on_pause_clicked(self):
        """ Met sur pause l'algorithme. """
        self.timer.stop()


    # Appuie sur le bouton avancer
    @QtCore.pyqtSlot() 
    def on_forward_clicked(self):
        """ Accélère la vitesse de simulation. """
        self.delai = self.delai / 2 if self.delai > 1 else self.delai
        self.timer.start(self.delai)

    # Appuie sur le bouton retour en arrière
    @QtCore.pyqtSlot()
    def on_rewind_clicked(self):
        """ Ralentit la vitesse de simulation. """
        self.delai *= 2
        self.timer.start(self.delai)

    # Appuie sur le bouton lecture
    @QtCore.pyqtSlot() 
    def on_play_clicked(self):
        """ Lancement de l'algorithme. """
        if self.generation == 0:
            self.lancement_algo()
            self.serie.clear()
            self.allumer_boutons()

        self.delai = 250
        self.timer.start(self.delai)
    
    # Méthode pour le lancement de l'algorithme génétique
    def lancement_algo(self):
        """ Méthode permettant le lancement de l'algorithme en mode graphique.
        """

        population = int(self.lineEdit.text())
        mutrate = float(self.lineEdit_4.text())
        elith = bool(self.checkBox.checkState())
        divers = bool(self.checkBox_1.checkState())
        nmbsgenes = pvc.Tournee.get_taille()
        self.scene = Scene(population, mutrate, elith, nmbsgenes, divers, self.graphicsView)
        self.graphicsView.setScene(self.scene)

    @QtCore.pyqtSlot() 
    def on_temps_timeout(self):
        """ Gestion de l'affichage des villes et des informations liées à la
        génération. """
        self.generation += 1
        self.scene.clear()
        self.scene.affichage_villes()
        tournee = self.scene.affichage_chemin(5)
        self.fitness = self.scene.calcul_fitness()
        self.groupBox.setTitle("Generation #{} data".format(self.generation))
        self.serie.append(self.generation, self.fitness)
        self.graph.chart().axisX().setRange(0, self.generation)
        self.affichage(tournee)

    # Afficher de "à propos"
    @QtCore.pyqtSlot(bool)
    def on_actionAbout_triggered(self):
        """ Affichage des informations "A propos". """

        aPropos = QtWidgets.QDialog(self)
        ligne = open("A_propos.htm", "r").read()
        layout = QtWidgets.QVBoxLayout(aPropos)
        texte = QtWidgets.QTextEdit()
        texte.setHtml(ligne)
        texte.setReadOnly(True)
        layout.addWidget(texte)
        aPropos.show()

    # Affichage de l'aide
    @QtCore.pyqtSlot(bool)
    def on_actionHelp_triggered(self):
        """ Affichage de l'aide. """

        aHelp = QtWidgets.QDialog(self)
        ligne = open("Help.htm", "r").read()
        layout = QtWidgets.QVBoxLayout(aHelp)
        texte = QtWidgets.QTextEdit()
        texte.setHtml(ligne)
        texte.setReadOnly(True)
        layout.addWidget(texte)
        aHelp.show()

    @QtCore.pyqtSlot(bool)
    def on_actionOpen_triggered(self):
        self.eteindre_boutons()
        self.scene.clear()
        self.timer.stop()
        self.generation = 0
        self.dialogue.exec()

    @QtCore.pyqtSlot(bool)
    def on_actionSave_triggered(self):
        date_courante = QtCore.QDateTime.currentDateTime()
        nom = "Génération_{}".format(date_courante.toString("dd.MM.yy_HH.mm.ss"))
        dossier = QtCore.QDir()
        dossier.mkdir(nom)
        dossier.cd(nom)

        self.screenshot("graphe.png", dossier, self.graph)
        self.screenshot("tour.png", dossier, self.graphicsView)

    # Action pour quitter le programme
    @QtCore.pyqtSlot(bool)
    def on_actionQuit_triggered(self):
        """ Quitte le programme. """
        QtWidgets.QApplication.quit()

    def screenshot(self, nomficher, dossier, attribut):
        chemin = dossier.absoluteFilePath(nomficher)
        fichier = QtCore.QFile(chemin)
        p = attribut.grab()
        p.save(fichier, "PNG", 0)


    def affichage(self, permut):
        resultat = ""
        fleche = "->"
        resultat += pvc.Tournee.get_Domaine(permut[0]).get_nom()
        for e in permut[1:]:
            resultat += fleche
            resultat += pvc.Tournee.Domaine[e].get_nom()

        self.round_l.setText(resultat)
        self.printfitness.setText(str(self.fitness))

    def allumer_boutons(self):
        """ Désactive tous les boutons. """
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)

    def eteindre_boutons(self): 
        """ Désactive tout les boutons sauf le bouton lecture. """

        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)

        self.pushButton_4.setEnabled(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.show()
    sys.exit(app.exec_())
