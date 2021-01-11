#!/usr/bin/env python3
# _____________________________PVC_Algo_Genetique_____________________________

# ============================================================================
# PVC_Algo_Genetique.py
# Version 1.0 (21 Décembre 2018)
# ABDALLAH Haribou, KIROV Mihail, PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# ============================================================================

from Algo_Generique import *

# ========================================================================== #
# ==================|         PARTIE SPECIFIQUE        |==================== #
# ========================================================================== #

# Classe ville
# ----------------------------------------------------------------------------
class Ville(Gene):
    
    def __init__(self, valeur, nom="ville"):
        super(Ville, self).__init__(valeur)    # Valeur de type coordonnée
        self.nom = nom

    def distance(self, other):
        """ Récupère la distance euclidienne entre villes. """

        return hypot((self.get_x() - other.get_x()),(self.get_y() - other.get_y()))

    # Accesseurs
    def get_x(self):
        return self.valeur.get_x()

    def get_y(self):
        return self.valeur.get_y()

    def get_nom(self):
        return self.nom

    def __repr__(self):
        return str(self.valeur.x) + ' ' + str(self.valeur.y)


# Classe coordonnées
# ----------------------------------------------------------------------------
class Coordonnees:
    """ Classe définissant les cordonnées d'une ville par x et y. """
    def __init__(self, x, y):

        # x, y latitude et longitude
        self.x = x      
        self.y = y

    # Accesseurs
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# Classe tournées héritant de chromosome
# ----------------------------------------------------------------------------
class Tournee(Chromosome):
    """ Classe permettant de rechercher une tournée. """

    Domaine = list() # ensemble des villes 
    _taille = 0
    valeurMax = 0

    def __init__(self, T): # T = Tableau de permutation(liste des villes) 
        """ Le generateur va fonctionner correctement 
            si les valeurs de T sont des entiers naturels 
        """ 

        # Initialisation de la classe mère et la fonction de fitness
        assert type(T) is list
        super().__init__(T) 

    @classmethod
    def calcul_window(cls):
        """ Méthode retournant les extremum de la window. """

        xmin = min(cls.Domaine, key=lambda ville: ville.get_x()).get_x()
        ymin = min(cls.Domaine, key=lambda ville: ville.get_y()).get_y()
        xmax = max(cls.Domaine, key=lambda ville: ville.get_x()).get_x()
        ymax = max(cls.Domaine, key=lambda ville: ville.get_y()).get_y()


        return (xmin , ymin), (xmax - xmin, ymax - ymin)

    @classmethod
    def init_domaine(cls, liste_villes):
        """ Initialisation du domaine. """

        cls.Domaine = liste_villes
        cls._taille = len(liste_villes)

    @classmethod
    def evaluerValMax(cls):
        """ Evalue la distance maximale d'un ensmeble des villes. """

        maxi = 0
        for i in range(cls._taille):
            for j in range(i + 1, cls._taille):
                disttemp = cls.Domaine[i].distance(cls.Domaine[j])      
                if(disttemp > maxi):
                    maxi = disttemp

        cls.valeurMax = maxi * cls._taille

    # Permute les gènes d'un individus
    # ------------------------------------------------------------------------
    def permutation(self):
        """Méthode utilisée comme pour la mutation dans l'algo genetique. """

        i = 0
        pourc_mutation = self._taille // 10
        while i < pourc_mutation:
            x, y = randrange(self._taille), randrange(self._taille)
            if x != y:
                self.liste_gene[x], self.liste_gene[y] =\
                self.liste_gene[y], self.liste_gene[x]
                i += 1

        self.fit = self.fitness()

    # Calcul de la fitness
    # ------------------------------------------------------------------------
    def cout_tournee(self): 
        """ Méthode retournant la fitness d'un individu. """

        suppression_doublons(self.liste_gene)
        resultat = 0
        taille = Tournee._taille
        for i in range(taille):
            resultat += Tournee.Domaine[self.liste_gene[i]].distance(Tournee.Domaine[self.liste_gene[(i + 1) 
            % taille]])

        return resultat / Tournee.valeurMax

    @classmethod
    def get_taille(cls):

        return cls._taille

    @classmethod 
    def get_Domaine(cls, i):
        """  Retourne une ville se trouvant à la position i dans la 
             liste Domaine"""

        return cls.Domaine[i]

    def get_permutation(self):
        # Spécialisation de la liste gène    
        return self.liste_gene


# ========================================================================== #
# =================|       FONCTIONS SECONDAIRES        |=================== #
# ========================================================================== #


# Supprime les doublons d'un individu
# ----------------------------------------------------------------------------
def suppression_doublons(liste):
    """ Methode supprimant les villes en doublons. Elle sera appelé entre le 
    croisement et l' insertion des individus dans la generation Ai et Ai+1. """
    
    taille = len(liste)
    # Ensemble des villes de la generation courante
    ens = {i for i in range(taille)} 
    listetmp = list()
    card = taille

    for i in range(taille):
        ens -= {liste[i]}  
        if(len(ens) == card):
            listetmp.append(i) # Element en doublon

        else:
            card -= 1

    # Choix au hasard d'un element qui n'est pas presant dans la liste
    for k in listetmp:
        liste[k] = ens.pop() 


# ========================================================================== #
# =================|       FONCTIONS PRINCIPALES        |=================== #
# ========================================================================== #

# Initialisation d'une tournée
# ----------------------------------------------------------------------------
def init_tournee(liste_villes):
    """ Initialisation des parties de l'algo specifique avec liste_villes la 
    liste d'objets de type ville. """

    Tournee.init_domaine(liste_villes)
    Tournee.evaluerValMax()


# Initialisation de la premième population
# ----------------------------------------------------------------------------
def init_population(nbgenes, seuilpop):
    """ Fonction initialisant la premiere population selon le nombre de gène
    et la limite de population. """

    permut = permutations(range(nbgenes)) 
    listepop = list()   
    Population.init_seuil(seuilpop)
    Chromosome.fitness = Tournee.cout_tournee 
    Chromosome.mutation = Tournee.permutation

    for i in range(seuilpop):   
        tournee = Tournee(list(next(permut)))
        listepop.append(deepcopy(tournee))

    pop1 = Population(listepop)
    pop1.ordonner()

    return pop1


# Fonction appellée lors de la génération aléatoire des villes
# ----------------------------------------------------------------------------
def init_villes_aleat(nbsvilles):
    """ Fonction retournant une liste de taille "nbvilles" d'objet de type
    ville générés aletoirement. """

    listeville = list()
    for ville in range(nbsvilles):
        V = Ville(Coordonnees(randrange(1000000), randrange(1000000)), 
        "{}".format(ville))   
        listeville.append(V)

    return listeville


# Fonction appellée lors de la génération des villes à partir d'un fichier
# ----------------------------------------------------------------------------
def init_villes_fich(src): 
    """ Fonction retournant une liste d'objets de type ville chargees a partir 
    d'un fichier src. Le fichier doit avoir le format suivant: NomVille, x, y
    """ 

    liste_villes = list()
    with open(src, "r") as f : 
        for line in f:
            s = line[: -1]
            s = s.split()
            assert len(s) == 3 
            v = Ville(Coordonnees(int(s[1]), int(s[2])), s[0])
            liste_villes.append(v)

    return liste_villes


# ========================================================================== #
# =======================|      TEST UNITAIRE      |======================== #
# ========================================================================== #
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from time import time

    nb_villes = 50
    lvilles = init_villes_alet(nb_villes )
    init_tournee(lvilles)
    start = time()
    algg = algo_genetique(500, 0.2, 1, nb_villes , 0)
    end = time()
    L = list()
    for e in algg:
        L.append(e)

    plt.plot(L)
    plt.show()