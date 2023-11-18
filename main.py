import pygame
import os
from classes.classes import Joueur, Bateau, Bouton, EntreeTexte
from random import randint


def reinitialiser():
    """
    Reinitialise les placements des bateaux et le nombre de coups joués en vue d'une nouvelle partie.
    """
    global joueur_actuel
    global joueur_adverse
    global origine_grille_j_actuel
    global origine_grille_j_adverse
    global pos_rangement_bateaux

    for i in range(len(joueur_gauche.bateaux)):
        # Remet le bateau à la verticale
        if joueur_gauche.bateaux[i].rect.w > joueur_gauche.bateaux[i].rect.h:
            joueur_gauche.bateaux[i].tourner_90()
        joueur_gauche.bateaux[i].rect.topleft = POSITIONS_RANGEMENT_BATEAUX_GAUCHE[i]
        joueur_gauche.bateaux[i].nombre_parties_non_detruites = joueur_gauche.bateaux[i].taille

        # Remet le bateau à la verticale
        if joueur_droite.bateaux[i].rect.w > joueur_droite.bateaux[i].rect.h:
            joueur_droite.bateaux[i].tourner_90()
        joueur_droite.bateaux[i].rect.topleft = POSITIONS_RANGEMENT_BATEAUX_DROITE[i]
        joueur_droite.bateaux[i].nombre_parties_non_detruites = joueur_droite.bateaux[i].taille

    joueur_gauche.nb_coups = 0
    joueur_droite.nb_coups = 0
    # Changement de 1er joueur 1 partie sur 2 en mode 2 joueurs.
    if (joueur_gauche.score + joueur_droite.score) % 2 == 1 and mode_de_jeu == "2_joueurs":
        joueur_actuel = joueur_droite
        joueur_adverse = joueur_gauche
        origine_grille_j_actuel = ORIGINE_GRILLE_DROITE
        origine_grille_j_adverse = ORIGINE_GRILLE_GAUCHE
        pos_rangement_bateaux = POSITIONS_RANGEMENT_BATEAUX_DROITE
    else:
        joueur_actuel = joueur_gauche
        joueur_adverse = joueur_droite
        origine_grille_j_actuel = ORIGINE_GRILLE_GAUCHE
        origine_grille_j_adverse = ORIGINE_GRILLE_DROITE
        pos_rangement_bateaux = POSITIONS_RANGEMENT_BATEAUX_GAUCHE

    # Réinitialisation des grilles.
    joueur_gauche.grille = [["eau" for i in range(TAILLE_GRILLE)] for j in range(TAILLE_GRILLE)]
    joueur_gauche.grille_adversaire = [["nuage" for i in range(TAILLE_GRILLE)] for j in range(TAILLE_GRILLE)]

    joueur_droite.grille = [["eau" for i in range(TAILLE_GRILLE)] for j in range(TAILLE_GRILLE)]
    joueur_droite.grille_adversaire = [["nuage" for i in range(TAILLE_GRILLE)] for j in range(TAILLE_GRILLE)]


def change_scene(nv_scene):
    """
    Change la scène pour une nouvelle et affiche les éléments de cette nouvelle scène à l'écran.

    Parametres
    ----------
    nv_scene: str
        nom de la nouvelle scène
    """
    global scene
    global background
    global boutons
    global entrees_texte
    global entree_texte_activee
    global mode_de_jeu
    global joueur_actuel

    scene = nv_scene
    boutons = []
    entrees_texte = []
    entree_texte_activee = None

    if scene == "menu":     # Scène de menu.
        fenetre.blit(menu_background, (0, 0))

        bouton_quitter.rect.center = (WIDTH / 2, HEIGHT * 6 / 7)
        boutons = [bouton_2_joueurs, bouton_1_joueur, bouton_quitter]

        dessine_texte("Bataille Navale", POLICE_TITRES, NOIR, (WIDTH / 2, HEIGHT / 7))

    elif scene == "creation_2_joueurs":     # Scène de création (des noms) des joueurs en mode 2j.
        fenetre.blit(menu_background, (0, 0))
        boutons = [bouton_retour, bouton_cest_parti]
        mode_de_jeu = "2_joueurs"

        joueur_gauche.score = 0
        joueur_droite.score = 0

        temp = pygame.transform.scale2x(joueur_gauche.img)
        rect = pygame.Rect((0, 0), temp.get_size())
        rect.center = (WIDTH / 3, HEIGHT / 4)
        fenetre.blit(temp, rect)

        temp = pygame.transform.scale2x(joueur_droite.img)
        rect = pygame.Rect((0, 0), temp.get_size())
        rect.center = (WIDTH * 2 / 3, HEIGHT / 4)
        fenetre.blit(temp, rect)

        entree_nom_joueur_g.couleur = COULEUR1_ENTREES_TEXTE
        entree_nom_joueur_g.rect.center = (WIDTH / 3, HEIGHT * 4 / 7)
        entree_nom_joueur_d.couleur = COULEUR1_ENTREES_TEXTE

        entrees_texte = [entree_nom_joueur_g, entree_nom_joueur_d]

    elif scene == "creation_1_joueur":      # Scène de création (du nomu) du joueur en mode 1j.
        fenetre.blit(menu_background, (0, 0))
        boutons = [bouton_retour, bouton_cest_parti]
        mode_de_jeu = "1_joueur"

        joueur_gauche.score = 0
        joueur_droite.score = 0

        temp = pygame.transform.scale2x(joueur_gauche.img)
        rect = pygame.Rect((0, 0), temp.get_size())
        rect.center = (WIDTH / 2, HEIGHT / 4)
        fenetre.blit(temp, rect)

        entree_nom_joueur_g.couleur = COULEUR1_ENTREES_TEXTE
        entree_nom_joueur_g.rect.center = (WIDTH / 2, HEIGHT * 4 / 7)

        entrees_texte = [entree_nom_joueur_g]

    elif scene == "placement_bateaux":      # Scène de placement des bateaux.
        if mode_de_jeu == "2_joueurs":
            fenetre.blit(carte, (0, 0))
            dessine_grilles()

            fenetre.blit(joueur_gauche.img, POSITION_JOUEUR_GAUCHE)
            fenetre.blit(joueur_droite.img, POSITION_JOUEUR_DROITE)

            joueur_gauche.nom = entree_nom_joueur_g.texte
            joueur_droite.nom = entree_nom_joueur_d.texte

            dessine_texte(joueur_gauche.nom, POLICE_NOM_JOUEURS, SABLE, (WIDTH * 1 / 4, HEIGHT * 14 / 15))

            dessine_texte(joueur_droite.nom, POLICE_NOM_JOUEURS, SABLE, (WIDTH * 3 / 4, HEIGHT * 14 / 15))

            boutons = [bouton_fini]
            bouton_fini.disabled = True
            explications = "Cliquez sur un bateau\npour le selectionner.\n\n" \
                           "Appuyez sur R pour\nle faire tourner.\n\n" \
                           "Cliquez à nouveau\npour le placer."

            if joueur_actuel == joueur_gauche:
                dessine_texte(explications, POLICE_EXPLICATIONS, NOIR, (WIDTH * 5 / 7, HEIGHT * 4 / 11))
                bouton_fini.rect.center = (WIDTH * 5 / 7, HEIGHT * 11 / 15)

            else:
                dessine_texte(explications, POLICE_EXPLICATIONS, NOIR, (WIDTH * 2 / 7, HEIGHT * 4 / 11))
                bouton_fini.rect.center = (WIDTH * 2 / 7, HEIGHT * 11 / 15)

                for i in range(len(POSITIONS_RANGEMENT_BATEAUX_DROITE)):
                    joueur_droite.bateaux[i].rect.topleft = POSITIONS_RANGEMENT_BATEAUX_DROITE[i]

            for b in joueur_actuel.bateaux:
                b.dessine(fenetre)

        elif mode_de_jeu == "1_joueur":
            positions_aleatoires_bateaux(joueur_droite, ORIGINE_GRILLE_DROITE)
            placer_bateaux(joueur_droite, ORIGINE_GRILLE_DROITE)
            change_scene("jeu")

    elif scene == "jeu":        # Scène du tour de jeu.
        fenetre.blit(carte, (0, 0))

        fenetre.blit(joueur_gauche.img, POSITION_JOUEUR_GAUCHE)
        fenetre.blit(joueur_droite.img, POSITION_JOUEUR_DROITE)

        for bateau in joueur_actuel.bateaux:
            bateau.dessine(fenetre)

        dessine_grilles()

        if mode_de_jeu == "2_joueurs":
            dessine_texte(joueur_gauche.nom, POLICE_NOM_JOUEURS, SABLE, (WIDTH * 1 / 4, HEIGHT * 14 / 15))
            dessine_texte(str(joueur_gauche.score), POLICE_SCORE, SABLE, (WIDTH * 3 / 7, HEIGHT * 14 / 15))

            dessine_texte(joueur_droite.nom, POLICE_NOM_JOUEURS, SABLE, (WIDTH * 3 / 4, HEIGHT * 14 / 15))
            dessine_texte(str(joueur_droite.score), POLICE_SCORE, SABLE, (WIDTH * 4 / 7, HEIGHT * 14 / 15))

        elif mode_de_jeu == "1_joueur":
            dessine_texte(joueur_gauche.nom, POLICE_NOM_JOUEURS, SABLE, (WIDTH * 2 / 7, HEIGHT * 14 / 15))
            dessine_texte(f"Nombre de coups : {joueur_actuel.nb_coups}", POLICE_EXPLICATIONS, SABLE,
                          (WIDTH * 5 / 7, HEIGHT * 14 / 15))

    elif scene == "changement_joueur":  # Scène de transition entre les joueurs.
        son_transition.play()

        fenetre.blit(nuages_image, (0, 0))

        global joueur_adverse
        global origine_grille_j_actuel
        global origine_grille_j_adverse
        global pos_rangement_bateaux

        if joueur_actuel == joueur_gauche:
            joueur_actuel = joueur_droite
            joueur_adverse = joueur_gauche
            origine_grille_j_actuel = ORIGINE_GRILLE_DROITE
            origine_grille_j_adverse = ORIGINE_GRILLE_GAUCHE
            pos_rangement_bateaux = POSITIONS_RANGEMENT_BATEAUX_DROITE
        else:
            joueur_actuel = joueur_gauche
            joueur_adverse = joueur_droite
            origine_grille_j_actuel = ORIGINE_GRILLE_GAUCHE
            origine_grille_j_adverse = ORIGINE_GRILLE_DROITE
            pos_rangement_bateaux = POSITIONS_RANGEMENT_BATEAUX_GAUCHE

        boutons = [bouton_cest_bon]

        # Détermine si la scène doit être ensuite changée pour jeu ou placement bateaux.
        # Si une des bateaux est à sa position initiale, cela signifie que le 2nd joueur doit placer ses bateaux.
        i = 0
        bouton_cest_bon.action = "jeu"
        while i < len(POSITIONS_RANGEMENT_BATEAUX_GAUCHE) and bouton_cest_bon.action != "placement_bateaux":
            if joueur_gauche.bateaux[i].rect.topleft == POSITIONS_RANGEMENT_BATEAUX_GAUCHE[i] \
                    or joueur_droite.bateaux[i].rect.topleft == POSITIONS_RANGEMENT_BATEAUX_DROITE[i]:
                bouton_cest_bon.action = "placement_bateaux"
            i += 1

        dessine_texte(f"Au tour de\n{joueur_actuel.nom} !", POLICE_TITRES, NOIR, (WIDTH / 2, HEIGHT * 1 / 3))

    elif scene == "menu_fin":   # Scène de menu après une partie.
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join("sons", "Trompette.mp3"))
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.queue(os.path.join("sons", "Ken Arai - Next to you (from Parasyte).mp3"), loops=-1)

        fenetre.blit(carte, (0, 0))

        fenetre.blit(joueur_gauche.img, POSITION_JOUEUR_GAUCHE)
        fenetre.blit(joueur_droite.img, POSITION_JOUEUR_DROITE)

        for i in range(len(joueur_gauche.bateaux)):
            joueur_gauche.bateaux[i].dessine(fenetre)
            joueur_droite.bateaux[i].dessine(fenetre)

        boutons = [bouton_rejouer, bouton_menu,  bouton_quitter]

        dessine_texte(f"{joueur_actuel.nom} gagne !\n", POLICE_TITRES, NOIR, (WIDTH / 2, HEIGHT / 6))
        if mode_de_jeu == "2_joueurs":
            dessine_texte(f"Score : {joueur_gauche.score} - {joueur_droite.score}", POLICE_SCORE, SABLE,
                          (WIDTH * 2 / 7, HEIGHT * 14 / 15))
            dessine_texte(f"Nombres de coups : {joueur_actuel.nb_coups}", POLICE_EXPLICATIONS, SABLE,
                          (WIDTH * 5 / 7, HEIGHT * 14 / 15))

            bouton_rejouer.rect.centerx = WIDTH / 2
            bouton_menu.rect.centerx = WIDTH / 2
            bouton_quitter.rect.center = (WIDTH / 2, HEIGHT * 7 / 9)
        elif mode_de_jeu == "1_joueur":
            global record_nb_coups
            if joueur_actuel.nb_coups < record_nb_coups:
                record_nb_coups = joueur_actuel.nb_coups
            dessine_texte(f"Nombres de coups : {joueur_actuel.nb_coups}", POLICE_EXPLICATIONS, SABLE,
                          (WIDTH * 2 / 7, HEIGHT * 14 / 15))
            dessine_texte(f"Record : {record_nb_coups}", POLICE_SCORE, SABLE,
                          (WIDTH * 5 / 7, HEIGHT * 14 / 15))

            bouton_rejouer.rect.centerx = WIDTH * 2 / 7
            bouton_menu.rect.centerx = WIDTH * 2 / 7
            bouton_quitter.rect.center = (WIDTH * 2 / 7, HEIGHT * 7 / 9)

        reinitialiser()

    elif scene == "quitter":    # Scène servant quitter le jeu.
        # L'action du bouton quitter va rediriger vers cette scène.
        global running
        running = False

    background = fenetre.copy()


def dessine_texte(texte, police, couleur, pos_milieu):
    """
    Dessine un texte sur la fenetre.

    Parametres
    ----------
    texte: str
        Texte à afficher. Peut être sur plusieurs lignes.
    police: pygame.font.Font
        Police d'écriture du texte.
    couleur: tuple de 3 int
        Couleur du texte.
    pos: tuple de 2 int
        Position du milieu du texte.
    """
    lignes = texte.split("\n")
    for i in range(len(lignes)):
        surf = police.render(lignes[i], True, couleur)
        y_milieu = pos_milieu[1] + police.get_height() * (i - (len(lignes)-1) / 2)
        rect = surf.get_rect(center=(pos_milieu[0], y_milieu))
        fenetre.blit(surf, rect)


def dessine_boutons():
    """
    Recouvre les boutons de la scene avec le background et redessine les boutons.
    """
    for bouton in boutons:
        bouton.dessine(fenetre, background)


def actualise_boutons():
    """
    Vérifie la collision des boutons avec la souris et si l'un d'eux est cliqué.

    Retourne
    --------
    result: str
        Chaine de caractère correspondant à l'action du bouton ou bien "pas_de_changement" si aucun bouton n'est cliqué.
    """
    result = "pas_de_changement"
    i = 0
    while i < len(boutons) and result == "pas_de_changement":
        if boutons[i].collision_souris() and click_souris:
            result = boutons[i].action
        i += 1
    return result


def dessine_zones_texte():
    """
    Recouvre les zones de texte de la scene avec le background et redessine les zones de texte.
    """
    for entree in entrees_texte:
        fenetre.blit(background, entree.rect, entree.rect)
        entree.dessine(fenetre)


def actualise_zones_texte():
    """
    Vérifie la collision des zones de texte avec la souris et si l'une d'elles est cliqué.
    """
    global entree_texte_activee
    i_collision_souris = -1
    for i in range(len(entrees_texte)):
        if entrees_texte[i].collision_souris():
            i_collision_souris = i

    if click_souris:
        if entree_texte_activee is not None:
            entree_texte_activee.texte = entree_texte_activee.texte[:-1]
            entree_texte_activee.couleur = COULEUR1_ENTREES_TEXTE

        if i_collision_souris != -1:
            entree_texte_activee = entrees_texte[i_collision_souris]
        else:
            entree_texte_activee = None

        if entree_texte_activee is not None:
            entree_texte_activee.texte += "|"
            entree_texte_activee.couleur = COULEUR2_ENTREES_TEXTE

    if i_collision_souris != -1:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def dessine_grilles():
    """
    Dessine les cases des grilles en fonction du joueur actuel.
    """
    # Défini les nuages à utiliser en fonction du joueur
    if joueur_actuel == joueur_gauche:
        nuages = NUAGES_GRILLE_DROITE
    else:
        nuages = NUAGES_GRILLE_GAUCHE

    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):

            # Grille du joueur.
            if joueur_actuel.grille[i][j] == "bateau_casse":
                fenetre.blit(bateau_casse, (case_grille_vers_pos_fenetre((j, i), origine_grille_j_actuel)))
            elif joueur_actuel.grille[i][j] == "tir_eau":
                fenetre.blit(tir_eau, (case_grille_vers_pos_fenetre((j, i), origine_grille_j_actuel)))

            # Grille de l'adversaire.
            if joueur_actuel.grille_adversaire[i][j] == "nuage":
                fenetre.blit(nuages[i][j], (case_grille_vers_pos_fenetre((j, i), origine_grille_j_adverse)))
            elif joueur_actuel.grille_adversaire[i][j] == "bateau_casse":
                fenetre.blit(bateau_casse, (case_grille_vers_pos_fenetre((j, i), origine_grille_j_adverse)))
            elif joueur_actuel.grille_adversaire[i][j] == "tir_eau":
                fenetre.blit(tir_eau, (case_grille_vers_pos_fenetre((j, i), origine_grille_j_adverse)))


def positions_aleatoires_bateaux(joueur, origine_grille):
    """
    Défini des positions aléatoires dans une pour les bateaux d'un joueur,
    de telle sorte que les bateaux ne se chevauchent pas.

    Parametres
    ----------
    joueur: Joueur
        Le joueur dont on doit placer les bateaux
    """
    cases_occupees = []

    for bateau in joueur.bateaux:
        cases_dispos = []

        orientation = randint(0, 3)
        for i in range(orientation):
            bateau.tourner_90()

        if orientation % 2 == 0:    # bateau à la verticale
            for i in range(0, TAILLE_GRILLE):
                for j in range(0, TAILLE_GRILLE - bateau.taille + 1):
                    dispo = True
                    k = 0
                    while k < len(cases_occupees) and dispo:
                        if cases_occupees[k][0] == i and cases_occupees[k][1] >= j and cases_occupees[k][1] <= j + bateau.taille:
                            dispo = False
                        k += 1
                    if dispo:
                        cases_dispos.append((i, j))

            case_bateau = cases_dispos[randint(0, len(cases_dispos) - 1)]

            # Placement du bateau.
            bateau.rect.topleft = case_grille_vers_pos_fenetre(case_bateau, origine_grille)

            for i in range(bateau.taille):
                cases_occupees.append((case_bateau[0], case_bateau[1]+i))

        else:   # bateau à l'horizontale
            for i in range(0, TAILLE_GRILLE - bateau.taille + 1):
                for j in range(0, TAILLE_GRILLE):
                    dispo = True
                    k = 0
                    while k < len(cases_occupees) and dispo:
                        if cases_occupees[k][0] >= i and cases_occupees[k][0] <= i + bateau.taille and cases_occupees[k][1] == j:
                            dispo = False
                        k += 1
                    if dispo:
                        cases_dispos.append((i, j))

            case_bateau = cases_dispos[randint(0, len(cases_dispos) - 1)]

            # Placement du bateau.
            bateau.rect.topleft = case_grille_vers_pos_fenetre(case_bateau, origine_grille)

            for i in range(bateau.taille):
                cases_occupees.append((case_bateau[0] + i, case_bateau[1]))


def placer_bateaux(joueur, origine_grille):
    """
    Inscrit les cases où sont situé les bateaux du joueur comme des cases bateaux dans la grille de ce dernier.
    Les cases où un bateau est situé sont de la forme "bateau:i" avec i l'index du bateau dans la liste de bateaux du joueur.
    Ces cases ne servent qu'à retrouver le bateau lorsque l'on tire dessus puis à être remplacée par une case "bateau_casse".

    Parametres
    ----------
    joueur: Joueur
        Joueur dont on doit placer les bateaux.
    origine_grille: tuple de 2 int
        Origine de la grille (case 0, 0) où placer les bateaux sur la fenetre.
    """
    for i in range(len(joueur.bateaux)):
        bateau_actuel = joueur.bateaux[i]
        xpixel, ypixel = bateau_actuel.rect.topleft
        x, y = pos_vers_case_grille((xpixel, ypixel), origine_grille)
        if bateau_actuel.rect.w > bateau_actuel.rect.h:
            decalage_x = 1
            decalage_y = 0
        else:
            decalage_x = 0
            decalage_y = 1
        for j in range(bateau_actuel.taille):
            joueur.grille[y + j * decalage_y][x + j * decalage_x] = f"bateau:{i}"


def bateau_dans_grille(bateau, origine_grille):
    """
    bateau: Bateau
        Bateau dont on doit tester la position.
    origine_grille: tupple de 2 int
        Origine de la grille que l'on doit considérer.

    Retourne
    --------
    bool
        True si le bateau est dans la grille et False sinon.
    """
    x_min = origine_grille[0]
    y_min = origine_grille[1]
    x_max = origine_grille[0] + TAILLE_GRILLE * TAILLE_CASE
    y_max = origine_grille[1] + TAILLE_GRILLE * TAILLE_CASE

    return bateau.rect.x >= x_min and bateau.rect.x + bateau.rect.width <= x_max and bateau.rect.y >= y_min and bateau.rect.y + bateau.rect.height <= y_max


def bateau_collision_autres_bateaux(bateau, autres_bateaux):
    """
    Parametres
    -----------
    bateau: Bateau
        Bateau dont on doit tester la collision.
    autres_bateaux: list de Bateau
        Bateaux avec lequels on doit tester la collision. Peut contenir bateau qui sera alors non testé.

    Retourne
    --------
    result: bool
        True si le bateau est en collision avec au moins un des autres bateaux (lui même exclu) et False sinon.
    """
    result = False
    i = 0
    while i < len(autres_bateaux) and not result:
        if autres_bateaux[i] != bateau and bateau.rect.colliderect(autres_bateaux[i].rect):
            result = True
        i += 1

    return result


def pos_vers_case_grille(pos, origine_grille):
    """
    Parametres
    ----------
    pos: tuple de 2 int
        Position que l'on doit transformer en case de grille.
    origine_grille: tupple de 2 int
        Origine de la grille que l'on doit considérer.

    Retourne
    --------
    tuple de 2 int
        L'équivalent en position de case dans la grille des coordonées de pos.
    """
    return (pos[0] - origine_grille[0]) // TAILLE_CASE, (pos[1] - origine_grille[1]) // TAILLE_CASE


def case_grille_vers_pos_fenetre(case, origine_grille):
    """
    Parametres
    ----------
    case: tuple de 2 int
        Coordonées de la case dans la grille.
    origine_grille: tupple de 2 int
        Origine de la grille que l'on doit considérer.

    Retourne
    --------
    tuple de 2 int
        Position dans la fenêtre du point en haut à gauche de la case.
    """
    return origine_grille[0] + case[0] * TAILLE_CASE, origine_grille[1] + case[1] * TAILLE_CASE


pygame.init()

carte = pygame.image.load(os.path.join("images", "fonds", "Carte.png"))
WIDTH, HEIGHT = carte.get_size()

# Création de la fenêtre.
fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
# fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bataille navale")

carte = carte.convert()

ORIGINE_GRILLE_GAUCHE = (171, 55)
ORIGINE_GRILLE_DROITE = (866, 55)
TAILLE_CASE = 62
TAILLE_GRILLE = 10
POSITION_JOUEUR_GAUCHE = (10, 655)
POSITION_JOUEUR_DROITE = (1512, 655)
ORIGINE_RANGEMENT_BATEAUX_GAUCHE = (4, 58)
# ORIGINE_RANGEMENT_DROITE = (1591, 58)


# Création des cases nuages servant à cacher la grille de l'adversaire

nuages_image = pygame.image.load(os.path.join("images", "fonds", "Nuages.png")).convert()
# convert: Change le format de pixel pour celui de la fenetre pour que l'affichage soit plus rapide.
nuages_bordure = pygame.image.load(os.path.join("images", "cases", "Nuages_bordure.png")).convert_alpha()
# convert_alpha: Même chose mais permet d'avoir la transparence.

NUAGES_GRILLE_GAUCHE = []
NUAGES_GRILLE_DROITE = []

x_gauche, y_gauche = ORIGINE_GRILLE_GAUCHE
x_droite, y_droite = ORIGINE_GRILLE_DROITE

for i in range(TAILLE_GRILLE):
    NUAGES_GRILLE_GAUCHE.append([])
    NUAGES_GRILLE_DROITE.append([])

    for j in range(TAILLE_GRILLE):
        surface = pygame.Surface((TAILLE_CASE, TAILLE_CASE))
        surface.blit(nuages_image, (0, 0), (x_gauche, y_gauche, TAILLE_CASE, TAILLE_CASE))
        surface.blit(nuages_bordure, (0, 0))
        NUAGES_GRILLE_GAUCHE[i].append(surface)

        surface = pygame.Surface((TAILLE_CASE, TAILLE_CASE))
        surface.blit(nuages_image, (0, 0), (x_droite, y_droite, TAILLE_CASE, TAILLE_CASE))
        surface.blit(nuages_bordure, (0, 0))
        NUAGES_GRILLE_DROITE[i].append(surface)

        x_gauche += TAILLE_CASE
        x_droite += TAILLE_CASE

    x_gauche = ORIGINE_GRILLE_GAUCHE[0]
    y_gauche += TAILLE_CASE
    x_droite = ORIGINE_GRILLE_DROITE[0]
    y_droite += TAILLE_CASE

# Images utilisées dans le jeu
menu_background = pygame.image.load(os.path.join("images", "fonds", "background.png")).convert()

bateau_casse = pygame.image.load(os.path.join("images", "cases", "bateau_casse.png")).convert_alpha()
tir_eau = pygame.image.load(os.path.join("images", "cases", "tir_eau.png")).convert_alpha()
viseur = pygame.image.load(os.path.join("images", "cases", "viseur.png")).convert_alpha()
viseur_rect = viseur.get_rect()

# Création des bateaux et des joueurs
bateaux_rouges = []
POSITIONS_RANGEMENT_BATEAUX_GAUCHE = []
POSITIONS_RANGEMENT_BATEAUX_DROITE = []
nb_cases_colonne = 0
x, y = ORIGINE_RANGEMENT_BATEAUX_GAUCHE
for nom_fichier in os.listdir(os.path.join("images", "joueur_rouge", "bateaux")):
    if nom_fichier[-4:] == ".png":
        img = pygame.image.load(os.path.join("images", "joueur_rouge", "bateaux", nom_fichier)).convert_alpha()
        taille_bateau = round(img.get_height() / img.get_width())
        hauteur_case = int(img.get_height() / taille_bateau)

        nb_cases_colonne += taille_bateau
        if nb_cases_colonne > 9:
            nb_cases_colonne = taille_bateau
            x += TAILLE_CASE
            y = ORIGINE_RANGEMENT_BATEAUX_GAUCHE[1]
        POSITIONS_RANGEMENT_BATEAUX_GAUCHE.append((x, y))
        POSITIONS_RANGEMENT_BATEAUX_DROITE.append((WIDTH - x - TAILLE_CASE, y))  # Car la carte est symétrique

        bateaux_rouges.append(Bateau(taille_bateau, img, (x, y)))

        y += taille_bateau * hauteur_case


joueur_gauche = Joueur("Joueur1", bateaux_rouges,
                       pygame.image.load(os.path.join("images", "joueur_rouge", "Joueur.png")).convert_alpha(),
                       TAILLE_GRILLE)

bateaux_verts = []
nb_cases_colonne_droite = 0
for nom_fichier in os.listdir(os.path.join("images", "joueur_vert", "bateaux")):
    if nom_fichier[-4:] == ".png":
        img = pygame.image.load(os.path.join("images", "joueur_vert", "bateaux", nom_fichier)).convert_alpha()
        taille_bateau = round(img.get_height() / img.get_width())
        bateaux_verts.append(Bateau(taille_bateau, img, POSITIONS_RANGEMENT_BATEAUX_DROITE[len(bateaux_verts)]))


joueur_droite = Joueur("Joueur2", bateaux_verts,
                       pygame.image.load(os.path.join("images", "joueur_vert", "Joueur.png")).convert_alpha(),
                       TAILLE_GRILLE)

# Définition de toutes les polices d'écriture, toutes les couleurs ainsi que de différents éléments (boutons, titres, entrées textes)

POLICE_BOUTONS = pygame.font.Font(os.path.join("polices", "arialbd.ttf"), 50)
COULEUR_TEXTE_BOUTONS = (75, 30, 20)
IMAGE_BOUTONS = pygame.image.load(os.path.join("images", "bouton.png")).convert_alpha()
bouton_2_joueurs = Bouton(IMAGE_BOUTONS, "2 Joueurs", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                          (WIDTH / 2, HEIGHT * 3 / 7), "creation_2_joueurs")
bouton_1_joueur = Bouton(IMAGE_BOUTONS, "1 Joueur", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS, (WIDTH / 2, HEIGHT * 7 / 11),
                         "creation_1_joueur")
bouton_quitter = Bouton(IMAGE_BOUTONS, "Quitter", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS, (WIDTH / 2, HEIGHT * 6 / 7),
                        "quitter")
bouton_retour = Bouton(IMAGE_BOUTONS, "Retour", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                       (WIDTH * 1 / 3, HEIGHT * 5 / 6), "menu")
bouton_cest_parti = Bouton(IMAGE_BOUTONS, "C'est parti !", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                           (WIDTH * 2 / 3, HEIGHT * 5 / 6), "placement_bateaux")
bouton_fini = Bouton(IMAGE_BOUTONS, "Fini !", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS, (WIDTH / 2, HEIGHT * 9 / 10),
                     "changement_joueur")
bouton_cest_bon = Bouton(IMAGE_BOUTONS, "C'est Bon !", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                         (WIDTH / 2, HEIGHT * 3 / 4), "jeu")
bouton_ok = Bouton(IMAGE_BOUTONS, "OK", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS, (WIDTH / 2, HEIGHT * 9 / 10),
                   "changement_joueur")
bouton_rejouer = Bouton(IMAGE_BOUTONS, "Rejouer", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                        (WIDTH / 2, HEIGHT * 3 / 9), "placement_bateaux")
bouton_menu = Bouton(IMAGE_BOUTONS, "Menu", POLICE_BOUTONS, COULEUR_TEXTE_BOUTONS,
                     (WIDTH / 2, HEIGHT * 5 / 9), "menu")

POLICE_ENTREES_TEXTE = pygame.font.Font(os.path.join("polices", "arialbd.ttf"), 55)
COULEUR1_ENTREES_TEXTE = (255, 255, 255)
COULEUR2_ENTREES_TEXTE = (200, 200, 200)
COULEUR_TEXTE_ENTREES_TEXTE = (0, 0, 0)
entree_nom_joueur_g = EntreeTexte(COULEUR1_ENTREES_TEXTE, joueur_gauche.nom, POLICE_ENTREES_TEXTE,
                                  COULEUR_TEXTE_ENTREES_TEXTE, 11, 375, 100, (WIDTH / 3, HEIGHT * 4 / 7))
entree_nom_joueur_d = EntreeTexte(COULEUR1_ENTREES_TEXTE, joueur_droite.nom, POLICE_ENTREES_TEXTE,
                                  COULEUR_TEXTE_ENTREES_TEXTE, 11, 375, 100, (WIDTH * 2 / 3, HEIGHT * 4 / 7))

POLICE_NOM_JOUEURS = pygame.font.Font(os.path.join("polices", "arialbd.ttf"), 65)
POLICE_SCORE = pygame.font.Font(os.path.join("polices", "arialbd.ttf"), 65)
POLICE_EXPLICATIONS = pygame.font.Font(os.path.join("polices", "arialbd.ttf"), 50)
POLICE_TITRES = pygame.font.Font(os.path.join("polices", "KOMTIT__.ttf"), 100)

NOIR = (0, 0, 0)
ROUGE = (200, 0, 0)
BLEU = (0, 20, 150)
SABLE = (186, 127, 61)

# Effets sonores et musiques
son_plouf = pygame.mixer.Sound(os.path.join("sons", "Plouf.wav"))
son_explosion = pygame.mixer.Sound(os.path.join("sons", "Explosion.wav"))
son_transition = pygame.mixer.Sound(os.path.join("sons", "Orage.wav"))

pygame.mixer.music.load(os.path.join("sons", "Ken Arai - Next to you (from Parasyte).mp3"))
pygame.mixer.music.play(loops=-1)

# Horloge servant à limiter les fps
clock = pygame.time.Clock()

# Initialisation des différentes variables utilisées
running = True
click_souris = False    # Sert d'indicateur pour savoir si le bouton gauche de la souris est cliqué
scene = "menu"
mode_de_jeu = "2_joueurs"
boutons = []            # Contient les différents boutons présents sur la scène actuelle.
entrees_texte = []      # Contient les différentes entrée textes présentes sur la scène actuelle.
background = menu_background    # Sert pour redessiner le fond après qu'un élément ai changé d'état.
entree_texte_activee = None
bateau_selectionne = None

record_nb_coups = TAILLE_GRILLE * TAILLE_GRILLE
joueur_actuel = joueur_gauche
joueur_adverse = joueur_droite
origine_grille_j_actuel = ORIGINE_GRILLE_GAUCHE
origine_grille_j_adverse = ORIGINE_GRILLE_DROITE
pos_rangement_bateaux = POSITIONS_RANGEMENT_BATEAUX_GAUCHE

change_scene("menu")

while running:
    click_souris = False  # On remet click souris à False ici car si on le faisait dans la boucle suivante avec un else,
    # s'il ny avait pas d'event (si on ne bouge pas la souris), click_souris resterait à True.

    # Gestion des événement pygame.
    for event in pygame.event.get():
        # Fermerture de la fenêtre
        if event.type == pygame.QUIT:
            running = False

        # Clique de la souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:    # Clique gauche
                click_souris = True

            if bateau_selectionne is not None:  # Clique droit
                if event.button == 3:
                    fenetre.blit(background, bateau_selectionne.rect, bateau_selectionne.rect)
                    bateau_selectionne.tourner_90()

        # Appui d'une touche
        elif event.type == pygame.KEYDOWN:
            if entree_texte_activee is not None:
                entree_texte_activee.texte = entree_texte_activee.texte[:-1]
                if event.key == pygame.K_BACKSPACE:
                    entree_texte_activee.texte = entree_texte_activee.texte[:-1]
                    entree_texte_activee.texte += "|"
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    entree_texte_activee.couleur = COULEUR1_ENTREES_TEXTE
                    entree_texte_activee = None
                else:
                    if len(entree_texte_activee.texte) < entree_texte_activee.nb_char_max:
                        entree_texte_activee.texte += event.unicode
                    entree_texte_activee.texte += "|"

            if bateau_selectionne is not None:
                if event.key == pygame.K_r:
                    fenetre.blit(background, bateau_selectionne.rect, bateau_selectionne.rect)
                    bateau_selectionne.tourner_90()

    actualise_zones_texte()
    dessine_zones_texte()

    nouvelle_scene = actualise_boutons()
    dessine_boutons()

    if scene == "placement_bateaux":
        tous_place = True
        # On va vérifier si un des bateaux n'est pas à sa position initiale et qu'il n'y a pas de bateau sélectionné
        # car c'est à ces conditions que l'on active le bouton fini.
        for i in range(len(joueur_actuel.bateaux)):
            if joueur_actuel.bateaux[i].rect.topleft == pos_rangement_bateaux[i]:
                tous_place = False

            if joueur_actuel.bateaux[i].collision_souris() and click_souris and bateau_selectionne is None:
                bateau_selectionne = joueur_actuel.bateaux[i]
                background.blit(carte, bateau_selectionne.rect, bateau_selectionne.rect)
                pygame.mouse.set_visible(False)
                click_souris = False

        if bateau_selectionne is not None:
            # Efface la position précédente du bateau sélectionné.
            fenetre.blit(background, bateau_selectionne.rect, bateau_selectionne.rect)

            # Actualise la position du bateau sélectionné.
            x, y = pygame.mouse.get_pos()
            bateau_selectionne.img.set_alpha(180)

            # Effectue un décalage pour que les coins de cases du bateau soient sur la grille et pas les milieu
            # de celles ci. Le décalage est différent si le bateau possède un nombre pair ou impair de cases.
            d_x, d_y = TAILLE_CASE / 2, TAILLE_CASE / 2
            if bateau_selectionne.taille % 2 == 0:
                if bateau_selectionne.rect.width > bateau_selectionne.rect.height:
                    d_x = 0
                else:
                    d_y = 0
            case = pos_vers_case_grille((x, y), origine_grille_j_actuel)
            bateau_selectionne.rect.center = (origine_grille_j_actuel[0] + TAILLE_CASE * case[0] + d_x,
                                              origine_grille_j_actuel[1] + TAILLE_CASE * case[1] + d_y)

            if bateau_dans_grille(bateau_selectionne, origine_grille_j_actuel):

                if not bateau_collision_autres_bateaux(bateau_selectionne, joueur_actuel.bateaux):
                    bateau_selectionne.img.set_alpha(255)
                    if click_souris:
                        bateau_selectionne.dessine(fenetre)
                        bateau_selectionne.dessine(background)
                        bateau_selectionne = None
                        pygame.mouse.set_visible(True)
            else:
                # Corrige la postition si le bateau est dans la grille
                bateau_selectionne.rect.center = (x, y)

            # Permet d'afficher le bouton derrière le bateau s'il y a collision.
            if bateau_selectionne is not None:
                for bouton in boutons:
                    if bateau_selectionne.rect.colliderect(bouton.rect):
                        bouton.dessine(fenetre, background)

                # Dessine le bateau avec sa nouvelle position.
                bateau_selectionne.dessine(fenetre)
                tous_place = False

            if not tous_place:
                bouton_fini.disabled = True
            else:
                bouton_fini.disabled = False

        if nouvelle_scene == "changement_joueur":
            placer_bateaux(joueur_actuel, origine_grille_j_actuel)

    if scene == "jeu" and len(boutons) == 0:  # Test si on est dans la scène jeu et que ce n'est pas la fin du tour.
        fenetre.blit(background, viseur_rect, viseur_rect)
        x, y = pygame.mouse.get_pos()   # Variables x, y = coordonées de la souris.
        viseur_rect.center = x, y       # Place le centre de l'image à l'endroit de la souris.
        pygame.mouse.set_visible(False)
        viseur.set_alpha(180)

        # Vérifie si le centre de la souris est bien dans la grille.
        if origine_grille_j_adverse[0] < x and x < origine_grille_j_adverse[0] + TAILLE_GRILLE * TAILLE_CASE \
                and origine_grille_j_adverse[1] < y and y < origine_grille_j_adverse[1] + TAILLE_GRILLE * TAILLE_CASE:

            # Corrige la position du viseur dans la grille
            xgrille, ygrille = pos_vers_case_grille((x, y), origine_grille_j_adverse)
            viseur_rect.topleft = (origine_grille_j_adverse[0] + xgrille * TAILLE_CASE,
                                   origine_grille_j_adverse[1] + ygrille * TAILLE_CASE)

            if joueur_actuel.grille_adversaire[ygrille][xgrille] == "nuage":  # Vérifie que le viseur est sur un nuage.
                viseur.set_alpha(255)  # Rend le viseur non transparent.

                if click_souris:  # Repère si la souris est cliquée.

                    joueur_actuel.nb_coups += 1

                    if mode_de_jeu == "2_joueurs":
                        boutons.append(bouton_ok)
                        pygame.mouse.set_visible(True)
                    elif mode_de_jeu == "1_joueur":
                        change_scene("jeu")

                    contenu_grille_adverse = joueur_adverse.grille[ygrille][xgrille].split(":")

                    if len(contenu_grille_adverse) == 2:    # S'il y a un bateau sur la case.
                        # Seules les cases bateaux possèdent le caractère : et contenu_grille_adverse a donc une taille de 2.
                        son_explosion.play()
                        bateau_touche = joueur_adverse.bateaux[int(contenu_grille_adverse[1])]
                        bateau_touche.nombre_parties_non_detruites -= 1

                        joueur_actuel.grille_adversaire[ygrille][xgrille] = "bateau_casse"
                        joueur_adverse.grille[ygrille][xgrille] = "bateau_casse"
                        fenetre.blit(bateau_casse, viseur_rect)
                        background.blit(bateau_casse, viseur_rect)

                        bouton_ok.action = "jeu"

                        if bateau_touche.nombre_parties_non_detruites == 0:
                            if mode_de_jeu == "2_joueurs":
                                dessine_texte("Touché Coulé !", POLICE_TITRES, ROUGE, (WIDTH / 2, HEIGHT / 7))
                            elif mode_de_jeu == "1_joueur":
                                dessine_texte("Touché Coulé !", POLICE_TITRES, ROUGE, (WIDTH * 2 / 7, HEIGHT * 4 / 9))
                                background = fenetre.copy()

                            gagne = True
                            i = 0
                            while i < len(joueur_adverse.bateaux) and gagne:
                                if joueur_adverse.bateaux[i].nombre_parties_non_detruites != 0:
                                    gagne = False
                                i += 1

                            if gagne:
                                if mode_de_jeu == "2_joueurs":
                                    joueur_actuel.score += 1
                                    bouton_ok.action = "menu_fin"
                                elif mode_de_jeu == "1_joueur":
                                    nouvelle_scene = "menu_fin"
                                    pygame.mouse.set_visible(True)

                        else:
                            if mode_de_jeu == "2_joueurs":
                                dessine_texte("Touché !", POLICE_TITRES, NOIR, (WIDTH / 2, HEIGHT / 7))
                            elif mode_de_jeu == "1_joueur":
                                dessine_texte("Touché !", POLICE_TITRES, NOIR, (WIDTH * 2 / 7, HEIGHT * 4 / 9))
                                background = fenetre.copy()

                    else:
                        son_plouf.play()
                        joueur_actuel.grille_adversaire[ygrille][xgrille] = "tir_eau"
                        joueur_adverse.grille[ygrille][xgrille] = "tir_eau"

                        fenetre.blit(carte, viseur_rect, viseur_rect)
                        fenetre.blit(tir_eau, viseur_rect)

                        # Au cas où la case se retrouve ensuite derrière le bouton.
                        background.blit(carte, viseur_rect, viseur_rect)
                        background.blit(tir_eau, viseur_rect)

                        if mode_de_jeu == "2_joueurs":
                            dessine_texte("Dans l'eau !", POLICE_TITRES, BLEU, (WIDTH / 2, HEIGHT / 7))
                            bouton_ok.action = "changement_joueur"
                        elif mode_de_jeu == "1_joueur":
                            dessine_texte("Dans l'eau !", POLICE_TITRES, BLEU, (WIDTH * 2 / 7, HEIGHT * 4 / 9))
                            background = fenetre.copy()

        if len(boutons) == 0:
            # Dessine le viseur avec sa nouvelle position.
            fenetre.blit(viseur, viseur_rect)

    if nouvelle_scene != "pas_de_changement":
        change_scene(nouvelle_scene)

    pygame.display.update()  # Actualise ce qui est affiché sur la fenêtre.
    clock.tick(60)  # Limite à 60 images par secondes.

pygame.quit()
