# ____________________________________Main____________________________________

# ============================================================================
# Main.py
# Version 1.0 (21 Décembre 2018)
# ABDALLAH Haribou, KIROV Mihail, PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# ============================================================================

from PyQt5 import QtCore, QtGui, QtWidgets
import Dialogue, Interface

# ========================================================================== #
# =======================|      TEST UNITAIRE      |======================== #
# ========================================================================== #
if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Fenetre = Interface.MainWindow()
	Fenetre.show()
	Fenetre.dialogue.exec()
	sys.exit(app.exec_())