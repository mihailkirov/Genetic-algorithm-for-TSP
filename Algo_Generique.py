#!/usr/bin/env python3
# _____________________________Algo_Generique_____________________________

# ============================================================================
# Algo_Generique.py
# Version 1.0 (21 Décembre 2018)
# ABDALLAH Haribou, KIROV Mihail, PAJANY Allan
# 3ème Année - Licence Informatique - UTLN
# ============================================================================

from random import sample, randint, random, randrange
from itertools import permutations   
from copy import deepcopy
from math import hypot


# ========================================================================== #
# ===================|         PARTIE GENERIQUE        |==================== #
# ========================================================================== #

# Classe population
# ----------------------------------------------------------------------------
class Population:
    _seuil = 0                  # Limite de la population
    _elite_pourcentage = 0.1    # Pourcentage d'élite
    taux_mutat = 0              # Taux de mutation

    def __init__(self, individus = []):
        self.individus = individus
        self.nbs = len(individus)

    def est_complete(self): 
        """ Verifie si la generation est complète. """

        return self._seuil == self.nbs

    def diversification(self):
        """ Diversification de la population à l'aide de la mutation. """

        nb_mut = randint(50, 100) # Nombre aletoire de mutation a chaque individu
        for individu in self.individus:
            tmp = nb_mut 
            while (tmp > 0):
                individu.mutation()
                tmp -= 1

    def ordonner(self):
        """ Tri des chromosommes en fonction de leur fitness. """

        self.individus.sort(key=lambda chromosome: chromosome.fit)

    # Transfert un individus d'une population à une autre
    def transfert_individu(self, chrom):
        self.individus.append(chrom)
        self.nbs += 1

   # Extraction d'un individus d'une population
    def extraire_individus(self, x):
        """ Methode extrayant un individu x d'une population. """

        return self.individus[x]

    # Transfert de l'élite de la populatiion n à n+1
    def transfert_elite(self, other):
        """ Méthode transférant les élites d'une population à une autre. """

        n = int(((self._elite_pourcentage * self.nbs) // 2) * 2) 
        + (self._seuil & 1)
        other.individus += self.individus[:n]
        other.nbs += n

    # Mutation d'un pourcentage la population
    def mutation_population(self):
        """ Méthode mutant un pourcentage de la population. """

        for element in sample(self.individus[int(self._elite_pourcentage
            * self.nbs):], self.taux_mutat):
            element.mutation()

        # Ordonnancement fitnesse croissant de la population
        self.ordonner()  

    # Méthode de selection par tournoi
    def selection_tournoi(self):
        """ Méthode permettant la selection par tournoi. """

        x, y = 0, 0
        while x == y:
            x = randrange(self.nbs)
            y = randrange(self.nbs)

        choix1 = min(x, y, key=lambda t: self.individus[t].fit)
        chrom1 = self.extraire_individus(choix1)

        x, y = 0, 0
        while x == y and self.nbs > 1:
            x = randrange(self.nbs)
            y = randrange(self.nbs)

        choix2 = min(x, y, key=lambda t: self.individus[t].fit)
        chrom2 = self.extraire_individus(choix2)

        return chrom1.croisement(chrom2)

    # Effectue le croisement des individus d'une population
    def croisement_population(self, other):
        """ Méthode permettant d'effectuer le croisement d'un individu d'une
        population et transfert ses enfants vers une autre population. """

        while not other.est_complete():
            # Selection en priviligeant les individus avec meilleur fintess
            chrom1 = self.extraire_individus(selectionner(self.nbs, 5))
            chrom2 = self.extraire_individus(selectionner(self.nbs, 5))
            chrom1, chrom2 = chrom1.croisement(chrom2)
            #chrom1, chrom2 = self.selection_tournoi()
            # Transfert de l'individus
            chrom = min(chrom1, chrom2, key=lambda x: x.fit)
            other.transfert_individu(chrom)

    @classmethod
    def init_seuil(cls, seuil):
        """ Initialisation du seuil de la population."""
        
        cls._seuil = seuil  

    @classmethod
    def init_taux_mutation(cls, pourcentage):
        """ Initialisation de taux de mutation. """
        
        cls.taux_mutat = int(pourcentage * cls._seuil)

    def __repr__(self):
        """ Affichage de la fitness de la generation. """ 

        resultat = ""
        for e in self.individus:
            resultat += str(e) + "\n"

        return resultat

    def __float__(self):
        
        return sum(chrom.fit for chrom in self.individus) / self._seuil 


# Classe chromosome
# ----------------------------------------------------------------------------
class Chromosome:
    def __init__(self, liste_gene):
        """ Initialisation de classe generique avec fitness - fonction propre 
            d'algo specifique. """ 

        self.liste_gene = liste_gene
        self.fit = self.fitness()  
        self._taille = len(liste_gene)

    def croisement(self, other):
        """ Méthode permettant le croisement de 2 individus a partir d'un point 
        de croisement choisit aléatoirement. """ 

        point = randint(1, self._taille - 1)
        individu, individu1 = [], []
        individu = self.liste_gene[:point] + other.liste_gene[point:]
        individu1 = other.liste_gene[:point] + self.liste_gene[point:]

        return Chromosome(individu), Chromosome(individu1)

    def get_liste_gene(self):
        return self.liste_gene

    def __repr__(self):
        return str(self.liste_gene)

    def __str__(self):
        return self.__repr__()

# Classe gène
# ----------------------------------------------------------------------------
class Gene:

    def __init__(self, valeur):
        self.valeur = valeur

    def get_valeur(self):
        return self.valeur

# ========================================================================== #
# ======================|      FONCTION FINALE      |======================= #
# ========================================================================== #

# Fonction finale de l'algorithme génétique
# ----------------------------------------------------------------------------
def algo_genetique(popinit, nbpop, mut_rate, elite, nbsgenes, divers):
    """ Fonction permettant le lancement de l'algorithme génétique. """ 

    pop1 = popinit
    pop1.init_taux_mutation(mut_rate)
    if (divers):
        pop1.diversification()
 
    if (elite): # Si le mode elitisme est choisi
        pop2 = Population([])
        while(True):
            yield pop1
            pop1.transfert_elite(pop2)
            pop1.croisement_population(pop2)
            pop2.mutation_population()
            pop1 = pop2
            pop2 = Population([])     

    else:
        pop1._elite_pourcentage = 0
        pop2 = Population([])
        while(True):
            yield pop1
            pop1.croisement_population(pop2)
            pop2.mutation_population()
            pop1 = pop2
            pop2 = Population([]) 


# Selection d'un individu dans la population de taille nbs
# ----------------------------------------------------------------------------
def selectionner(nbs, degre):
    """ Cette fonction obeit a une loi de probalité dont l'esperence est 
    1/(degre + 1) concrétement plus la valeur de degré est élevé plus la 
    probabilité d'obtenir une petite valeur est grande. Les valeurs obtenues
    sont comprises entre 0 et nbs. """
    
    return int(nbs * (random()**degre))