#### Pourquoi il manque ces valeurs ? (colonne par colonne)

#### lieu — 11 manquants

manquants = problèmes de parsing ou données très anciennes.

#### magnitude — 155 698 manquants

Tous les séismes n’ont pas de magnitude calculable.

Exemples :

- Séismes très faibles (micro-séismes), détectés par très peu de stations
- Événements trop proches d’une seule station
- Bruit mal séparé du signal
- Magnitude indisponible dans certaines bases historiques

Il est courant que 10–20% des séismes manquent une magnitude.

Une magnitude 0 correspond à un événement extrêmement faible, souvent non ressenti.

#### type_magnitude — 166 609 manquants

- certains réseaux ne donnent qu’une magnitude sans type
- magnitudes anciennes (pré-1980) souvent non typées

#### profondeur_km — 9 manquants

Les quelques cas manquants viennent généralement de :

- séismes très vieux (1970–1980)
- événements mal localisés (signal trop faible)
- erreurs de parsing dans certaines bases USGS

Si depth = 0 :

- Séisme très superficiel (< 1 km)
- Régulièrement, des explosions, tirs miniers etc...

#### mag_uniforme — 701 438 manquants

Magnitude uniformisée. On calcule une magnitude uniforme approximative mais réaliste à des fins statistiques. Certains types de magnitude ne se prêtent pas à cette normalisation d'où les valeurs manquantes parfois.

#### nb_stations_localisation — 1 204 826 manquants

nst = nombre réel de stations utilisées dans le calcul.

👉 La plupart des réseaux modernes ne donnent plus nst, ou ne le transmettent pas.

Donc :

- nst manquant = inconnu / non rapporté (pas une erreur)

Quand c’est 0, ça signifie « pas fourni », jamais « 0 station ».

#### nb_stations_magnitude — 1 091 476 manquants

Nombre de stations utilisées uniquement pour calculer la magnitude.

Très rarement fourni → normal qu'il manque à ~80%.

#### ecart_azimut — 834 294 manquants

Gap = une mesure de qualité du réseau autour de l’épicentre.

Pourquoi manquant ?

- non fourni par certains algorithmes automatiques
- certains réseaux n’utilisent pas cette mesure
- valeurs anciennes avant les années 2000 → souvent vides

#### rms — 210 659 manquants

RMS = qualité de l’ajustement des temps d’arrivée.

Manque lorsque :

- trop peu de stations
- calcul non effectué
- algorithme automatique qui échoue

#### erreur_horiz — 1 524 519 manquants

L’erreur horizontale n’est quasiment jamais fournie dans les catalogues USGS globaux.

Elle existe seulement pour :

- séismes bien localisés
- zones instrumentées
- données récentes

Très normal qu’elle soit manquante pour >90%.

#### erreur_profondeur — 603 806 manquants

- beaucoup de séismes n’ont pas d’estimation de l’incertitude

#### erreur_magnitude — 1 772 000 manquants

La plupart des magnitudes automatiques ne fournissent pas d’erreur.
C’est normal que 80–90% soit manquant.
