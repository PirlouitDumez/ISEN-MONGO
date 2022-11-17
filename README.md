# ISEN-MONGO

il reste à faire :
- deactivate all station in an area (ajouter 1 colonne available qui vaut False qd on desactive des stations (avec la recherche par area))
=> Utiliser find-in-area(affichage=False) ou find_in_polygon(affichage=False) pour obtenir la liste des stations à desactiver


- give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday) (faut stocker qq part les resultats des update de la table data et laisser tourner un peu pour avoir qq donnees)
=> Ca parait un peu complexe je sais pas trop comment ça fonctionne...


- Menu dans la console (pour selectionner l'action à realiser, les paramètres associés, etc.)
