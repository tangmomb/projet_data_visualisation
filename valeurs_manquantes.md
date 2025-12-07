## 🧨 Pourquoi il manque ces valeurs ? (colonne par colonne)

### ⭐ depth (profondeur) — 9 manquants

Très rare.
Les quelques cas manquants viennent généralement de :

- séismes très vieux (1970–1980)
- événements mal localisés (signal trop faible)
- erreurs de parsing dans certaines bases USGS

Si depth = 0 :

- Profondeur inconnue, non déterminée
- Certains catalogues forcent la profondeur à 0 lorsqu'il n’y a pas assez de stations (nst faible).
- Séisme très superficiel (< 1 km)
- Régulièrement, des explosions, tirs miniers etc...

### ⭐ mag (magnitude) — 156 449 manquants

La raison n°1 est simple :

👉 Tous les séismes n’ont pas de magnitude calculable.

Exemples :

- Séismes très faibles (micro-séismes), détectés par très peu de stations
- Événements trop proches d’une seule station
- Bruit mal séparé du signal
- Magnitude indisponible dans certaines bases historiques

Il est courant que 10–20% des séismes manquent une magnitude.

Une magnitude 0 correspond à un événement extrêmement faible, souvent non ressenti.

### ⭐ magType (type de magnitude) — 167 407 manquants

Directement lié à mag :

- pas de magnitude → pas de magType
- certains réseaux ne donnent qu’une magnitude sans type
- magnitudes anciennes (pré-1980) souvent non typées

### ⭐ nst (nombre de stations) — 881 566 manquants

Très normal.
nst = nombre réel de stations utilisées dans le calcul.

👉 La plupart des réseaux modernes ne donnent plus nst, ou ne le transmettent pas.

Donc :

- nst manquant = inconnu / non rapporté (pas une erreur)

Quand c’est 0, ça signifie « pas fourni », jamais « 0 station ».

### ⭐ gap (azimuthal gap) — 838 549 manquants

Gap = une mesure de qualité du réseau autour de l’épicentre.

Pourquoi manquant ?

- non fourni par certains algorithmes automatiques
- certains réseaux n’utilisent pas cette mesure
- valeurs anciennes avant les années 2000 → souvent vides

### ⭐ dmin (distance minimale à une station) — 1 346 742 manquants

Très souvent non disponible, parce que :

- dépend de la géométrie du réseau local
- inutilisée dans beaucoup de catalogues
- certains séismes utilisent un algorithme qui ne calcule pas dmin

👉 Très courant que la majorité soit manquante.

### ⭐ rms (root-mean-square de l’erreur de temps) — 211 653 manquants

RMS = qualité de l’ajustement des temps d’arrivée.

Manque lorsque :

- trop peu de stations
- calcul non effectué
- algorithme automatique qui échoue

### ⭐ place (description du lieu) — 11 manquants

Quasi parfait → manquants = problèmes de parsing ou données très anciennes.

### ⭐ horizontalError — 1 531 963 manquants

L’erreur horizontale n’est quasiment jamais fournie dans les catalogues USGS globaux.

Elle existe seulement pour :

- séismes bien localisés
- zones instrumentées
- données récentes

Très normal qu’elle soit manquante pour >90%.

### ⭐ depthError — 606 685 manquants

Similaire :

- beaucoup de séismes n’ont pas d’estimation de l’incertitude

### ⭐ magError — 1 781 012 manquants

La plupart des magnitudes automatiques ne fournissent pas d’erreur.
C’est normal que 80–90% soit manquant.

### ⭐ magNst — 988 917 manquants

Nombre de stations utilisées uniquement pour calculer la magnitude.

Très rarement fourni → normal qu'il manque à ~80%.

### ⭐ status (automatic / reviewed) — 1 manquant

Un enregistrement mal formé ou égaré.
Pas grave.
