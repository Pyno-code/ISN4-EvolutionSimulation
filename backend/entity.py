import random
import math
import time
import tkinter as tk

class Entity:
    

    def __init__(self, id, width, height, fps, x=0, y=0, pos_random = True, level=random.randint(1, 3)):
        self.id = id
        self.level = level
        
        if pos_random:
            self.x, self.y = random.randint(20, width - 20), random.randint(20, height - 20)
        else:
            self.x, self.y = x, y

        self.update_speed()
        self.angle = random.uniform(0, 360)  # Direction aléatoire

        self.width = width
        self.height = height

        
        self.entities = []
        self.nourritures = []

        self.detection_range = (4 - self.level) * 40

        self.exist = True
        self.updating = False

        self.energy = 100 * self.level**1.5


        self.fps = fps
        self.time_step = 1 / fps
        
        self.dx = 0
        self.dy = 0

        self.kv = 1


    def get_energy(self):
        """
        Retourne l'énergie actuelle de l'entité.

        Returns:
            float: La quantité d'énergie de l'entité.
        """
        return self.energy

    def check_collision(self):
        """
        Vérifie et gère les collisions entre cette entité, les autres entités et les nourritures.

        Pour chaque entité présente :
            - Si une autre entité est détectée à une distance inférieure à 50 unités :
                - Si l'autre entité a un niveau supérieur, elle absorbe l'énergie de cette entité, supprime cette entité et augmente son niveau.
                - Sinon, cette entité absorbe l'énergie de l'autre, supprime l'autre entité et augmente son niveau.

        Pour chaque nourriture présente :
            - Si la nourriture est détectée à une distance inférieure à 50 unités :
                - Cette entité absorbe l'énergie de la nourriture, augmente son niveau et supprime la nourriture.

        Cette méthode permet de simuler les interactions de prédation et de collecte de ressources dans l'environnement.
        """
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < 50:
                    if other.level > self.level:  # Rayon de détection de collision
                        other.update_energy(self.energy)
                        self.delete()
                        other.update_level()
                    else:
                        self.update_energy(other.energy)
                        other.delete()
                        self.update_level()
        for nourriture in self.nourritures:
            distance = math.sqrt((self.x - nourriture.x) ** 2 + (self.y - nourriture.y) ** 2)
            if distance < 50:
                self.update_energy(nourriture.energy)
                self.update_level()
                nourriture.delete()

    def set_entities(self, entities):
        """
        Définit la liste des entités pour cet objet.

        Paramètres :
            entities (list) : La nouvelle liste d'entités à assigner.
        """
        self.entities = entities

    def set_nourritures(self, nourritures):
        """
        Définit la liste des nourritures pour l'entité.

        Paramètres :
            nourritures (list) : La nouvelle liste de nourritures à associer à l'entité.
        """
        self.nourritures = nourritures

    def delete(self):
        """
        Supprime cette entité de la liste des entités si elle y est présente,
        puis marque l'entité comme n'existant plus.

        Cette méthode vérifie si l'entité courante est présente dans la liste
        `entities`. Si c'est le cas, elle la retire de la liste et définit
        l'attribut `exist` à False pour indiquer que l'entité a été supprimée.
        """
        if self in self.entities:
            self.entities.remove(self)
            self.exist = False

    def update(self):
        """
        Met à jour l'état de l'entité pour un cycle de simulation.

        Cette méthode vérifie si l'entité est déjà en cours de mise à jour afin d'éviter les conflits.
        Elle détecte les entités et nourritures à proximité, met à jour la direction de l'entité en fonction
        de ces éléments, puis met à jour sa position. Enfin, elle réinitialise le statut de mise à jour.

        """
        if not self.updating:
            self.updating = True
            entities_in_scope = self.scope_detection_entity()
            nourritures_in_scope = self.scope_detection_nourriture()
            self.update_direction(entities_in_scope, nourritures_in_scope)
            self.update_position()
            self.updating = False
        pass

    def update_direction(self, entities_in_scope, nourritures_in_scope):
        """
        Met à jour la direction de l'entité en fonction des entités et nourritures à proximité.
        Cette méthode calcule un vecteur d'attraction basé sur la position des nourritures et des autres entités dans le champ de vision.
        - L'entité est attirée vers les nourritures proches, avec une force inversement proportionnelle au carré de la distance.
        - Pour les autres entités, l'attraction ou la répulsion dépend de la différence de niveau : 
          si l'entité courante a un niveau supérieur, elle est attirée, sinon elle est repoussée.
        - Si aucune attraction n'est détectée, la direction de l'entité est modifiée aléatoirement.
        Args:
            entities_in_scope (list): Liste des entités visibles par l'entité courante.
            nourritures_in_scope (list): Liste des nourritures visibles par l'entité courante.
        Effets de bord:
            Modifie l'attribut `angle` de l'entité pour refléter la nouvelle direction.
        """
        attracted = False
        attract_x, attract_y = 0, 0
        
        for nourriture in nourritures_in_scope:
            attracted = True

            dx = nourriture.x - self.x
            dy = nourriture.y - self.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-6
            direction_angle = math.atan2(dy, dx)
            weight = 1 / (distance**2)

            # Attirance proportionnelle à la distance
            attract_x += weight * math.cos(direction_angle)
            attract_y += weight * math.sin(direction_angle)


        for entity in entities_in_scope:
            dx = entity.x - self.x
            dy = entity.y - self.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-6  # Évite la division par zéro
            direction_angle = math.atan2(dy, dx)

            level_difference = self.level - entity.level
            weight = level_difference / (distance**2)  # Poids basé sur la différence de niveau et la distance
            
            attract_x += weight * math.cos(direction_angle)
            attract_y += weight * math.sin(direction_angle)

            if level_difference != 0:
                attracted = True

        

        
        if attracted and (attract_x != 0 or attract_y != 0):
            self.angle = math.degrees(math.atan2(attract_y, attract_x))
        else:
            self.angle += random.gauss(0, 15)
        
        self.angle %= 360



    def check_position_limit(self):
        """
        Vérifie et ajuste la position de l'entité pour s'assurer qu'elle reste dans les limites autorisées de la zone.
        Si la position x ou y dépasse les bornes définies (20 et width/height - 20), elle est corrigée pour rester à l'intérieur.
        """
        if self.x > self.width - 20:
            self.x = self.width - 20 - 1
        elif self.x < 20:
            self.x = 20 + 1
        
        if self.y < 20:
            self.y = 20 + 1
        elif self.y > self.height - 20:
            self.y = self.height - 20 - 1

    def update_position(self):
        """
        Met à jour la position de l'entité en fonction de sa vitesse, de son angle et du temps écoulé.
        Vérifie d'abord les collisions et les limites de position, puis calcule le déplacement (dx, dy).
        Applique le déplacement uniquement si la nouvelle position reste dans les bornes autorisées du cadre.
        """
        self.check_collision()
        self.check_position_limit()


        self.dx = self.speed * self.time_step * self.kv * math.cos(math.radians(self.angle))
        self.dy = self.speed * self.time_step * self.kv * math.sin(math.radians(self.angle))


        new_x = self.x + self.dx
        new_y = self.y + self.dy

        if 20 < new_x < self.width - 20 and 20 < new_y < self.height - 20:

            self.x += self.dx
            self.y += self.dy

    def scope_detection_entity(self):
        """
        Détecte et retourne la liste des entités à portée de détection.

        Parcourt toutes les entités présentes dans l'environnement, calcule la distance
        entre l'entité courante et les autres, puis ajoute à la liste celles qui se trouvent
        dans la portée de détection définie par `self.detection_range`.

        Retourne :
            list : Liste des entités détectées à portée.
        """
        entity_seen = []
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < self.detection_range:
                    entity_seen.append(other)
        return entity_seen
    
    def scope_detection_nourriture(self):
        """
        Détecte et retourne la liste des nourritures à portée de détection de l'entité.

        Parcourt toutes les nourritures disponibles et calcule la distance entre l'entité et chaque nourriture.
        Si la nourriture se trouve dans le rayon de détection (`detection_range`), elle est ajoutée à la liste des nourritures détectées.

        Retourne :
            list : Liste des objets nourriture détectés à portée.
        """
        nourriture_seen = []
        for nourriture in self.nourritures:
            distance = math.sqrt((self.x - nourriture.x) ** 2 + (self.y - nourriture.y) ** 2)
            if distance < self.detection_range:
                nourriture_seen.append(nourriture)
        return nourriture_seen

    def update_kv(self, kv):
        """
        Met à jour la valeur de l'attribut du coeficient de vitesse 'kv' de la simulation.

        Paramètres :
            kv : La nouvelle valeur à assigner à l'attribut 'kv'.
        """
        self.kv = kv

    def update_level(self):
        """
        Met à jour le niveau de l'entité en fonction de son énergie.

        Si le niveau actuel est inférieur à 3, le niveau est recalculé en fonction de l'énergie,
        limité entre 1 et 3. Met également à jour la vitesse de l'entité et ajuste la portée de détection
        en fonction du nouveau niveau.

        """
        if self.level < 3:
            self.level = int(max(1, min(3, int(self.energy / 7000**(1/1.5)))))
            self.update_speed()
            self.detection_range = (4 - self.level) * 40

    def update_speed(self):
        """
        Met à jour la vitesse de l'entité en fonction de son niveau.

        La vitesse est calculée selon la formule : (4 - niveau) * 50.
        Un niveau plus élevé réduit la vitesse de l'entité.
        """
        self.speed = (4 - self.level)*50
    
    def update_energy(self, energy):
        """
        Met à jour l'énergie de l'entité en ajoutant la valeur spécifiée.

        Si l'énergie totale devient inférieure ou égale à zéro, l'entité est supprimée.
        Sinon, le niveau de l'entité est recalculé en fonction de sa nouvelle énergie,
        avec une valeur comprise entre 1 et 3.

        Paramètres
        ----------
        energy : float
            La quantité d'énergie à ajouter (ou à soustraire si négative).
        """
        self.energy += energy
        if self.energy <= 0:
            self.delete()
        else:
            self.level = int(max(1, min(3, int(self.energy / 7000**(1/1.5)))))