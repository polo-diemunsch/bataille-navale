import pygame


class Bouton:
    """
    Attributs
    ---------
    img: pygame.Surface
        Image du bouton
    rect: pygame.Rect
        Position et taille du bouton
    action: str
        Action liée au bouton. Dans la cadre de ce projet, stocke le nom de la scene où l'on doit se rendre après
        l'appui du bouton.
    """
    def __init__(self, img, texte, police, couleur_texte, pos_milieu, action):
        """
        Initialise le bouton.

        Parametres
        ----------
        texte: str
            Texte affiché sur le bouton.
        police: pygame.font.Font
            Police d'écriture du texte du bouton.
        couleur_texte: tuple de 3 int
            Couleur du texte du bouton.
        pos_milieu:
            Position du milieu du bouton.
        """
        self.img = img.copy()
        texte_img = police.render(texte, True, couleur_texte)
        self.img.blit(texte_img, ((self.img.get_width() - texte_img.get_width())//2,
                                  (self.img.get_height() - texte_img.get_height())//2))
        self.img.set_alpha(220)
        self.rect = img.get_rect(center=pos_milieu)
        self.action = action
        self.disabled = False

    def collision_souris(self):
        """
        Vérifie si la souris est sur le bouton. Si c'est le cas, rend le bouton opaque.

        Retourne
        --------
        result: bool
            True si la souris est sur le bouton, False sinon.
        """
        if self.disabled:
            self.img.set_alpha(180)
            result = False
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            self.img.set_alpha(255)
            result = True
        else:
            self.img.set_alpha(220)
            result = False
        return result

    def dessine(self, surface, background=None):
        """
        Dessine le bouton.

        Parametres
        ----------
        surface: pygame.Surface
            Surface sur laquelle dessiner l'image du bouton.
        background: pygame.Surface, optionel
            Fond à dessiner derrière le bouton
        """
        if background is not None:
            surface.blit(background, self.rect, self.rect)
        surface.blit(self.img, self.rect)


class EntreeTexte:
    """
    Attributs
    ---------
    couleur: tuple de 3 int
        Couleur du fond de la zone de texte.
    texte: str
        Texte contenu dans la zone de texte.
    police: pygame.font.Font
        Police d'écriture du texte.
    couleur_texte: tuple de 3 int
        Couleur du texte.
    nb_char_max: int
        Nombre de charactères maximal que l'on peut écrire dans cette zone de texte.
    rect: pygame.Rect
        Position et taille de la zone de texte.
    img: pygame.Surface
        Rendu de la zone de texte.
    """
    def __init__(self, couleur, texte, police, couleur_texte, nb_char_max, longueur, hauteur, pos_milieu):
        """
        Initialise l'entrée texte.

        Parrametres
        -----------
        longueur: int
            Longueur de la zone de texte.
        hauteur: int
            Hauteur de la zone de texte.
        pos_milieu: tuple de 2 int
            Position du milieu de la zone de texte.
        """
        self.couleur = couleur
        self.texte = texte
        self.police = police
        self.couleur_texte = couleur_texte
        self.nb_char_max = nb_char_max
        self.rect = pygame.Rect((0, 0), (longueur, hauteur))
        self.rect.center = pos_milieu
        self.img = pygame.Surface((longueur, hauteur))

    def collision_souris(self):
        """
        Vériife si la souris est sur la zone de texte.

        Retourne
        --------
        bool
            True si la souris est sur la zone de texte, False sinon.
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def dessine(self, surface):
        """
        Dessine la zone de texte.

        Parametres
        ----------
        surface: pygame.Surface
            Surface sur laquelle dessiner le rendu de la zone de texte.
        """
        self.img.fill(self.couleur)
        texte_img = self.police.render(self.texte, True, self.couleur_texte)
        self.img.blit(texte_img, ((self.img.get_width() - texte_img.get_width())//2, (self.img.get_height() - texte_img.get_height())//2))
        surface.blit(self.img, self.rect)


class Bateau:
    """
    Attributs
    ---------
    taille: {2, 3, 4, 5}
        Nombre de cases dont est composé le bateau.
    parties: list de pygame.Surface
        Liste des images des cases du bateau.
    nombre_parties_non_detruites: {0, 1, 2, 3, 4, 5}
        Nombre de parties du bateau n'ayant pas été détruites.
    img: pygame.Surface
        Image du bateau.
    rect: pygame.Rect
        Position et taille du bateau.
    """
    def __init__(self, taille, img, pos):
        """
        Initialise le bateau.

        Parametres
        ----------
        pos: tuple de 2 int
            Position du point en haut à gauche du bateau.
        """
        self.taille = taille
        self.parties = []
        self.nombre_parties_non_detruites = taille
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = pos

    def tourner_90(self):
        """
        Tourne le bateau de 90° dans le sens trigo.
        """
        self.img = pygame.transform.rotate(self.img, 90)
        w, h = self.rect.size
        self.rect.width = h
        self.rect.height = w

    def dessine(self, surface):
        """
        Dessine le bateau.

        Parametres
        ----------
        surface: pygame.Surface
            Surface sur laquelle dessiner l'image.
        """
        surface.blit(self.img, self.rect)

    def collision_souris(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


class Joueur:
    """
    Attribus
    --------
    nom: str
        Nom du joueur.
    score: int
        Nombre de manches gagnées par le joueur
    bateaux: list de Bateau
        Bateaux appartenant au joueur.
    img: pygame.Surface
        Image du personnage du joueur.
    grille: list de str
        Chaines de caractères correspondant à ce qui est placé sur chacune des cases de la grille du joueur.
    grille_adversaire: list de str
        Chaines de caractères correspondant à ce qui est placé sur chacune des cases de la grille du joueur adverse.
    """
    def __init__(self, nom, bateaux, img, taille_grille):
        """
        Initialise le joueur.

        Parametres
        ----------
        taille_grille: int
            Nombre de cases d'un côté de la grille.
        """
        self.nom = nom
        self.score = 0
        self.nb_coups = 0
        self.bateaux = bateaux
        self.img = img
        self.grille = [["eau" for i in range(taille_grille)] for j in range(taille_grille)]
        self.grille_adversaire = [["nuage" for i in range(taille_grille)] for j in range(taille_grille)]

