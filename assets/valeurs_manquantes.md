#### Pourquoi il manque ces valeurs ? (colonne par colonne)

#### magnitude

Tous les séismes n’ont pas de magnitude calculable.

Exemples :

- Séismes très faibles (micro-séismes), détectés par très peu de stations
- Événements trop proches d’une seule station
- Bruit mal séparé du signal
- Magnitude indisponible dans certaines bases historiques

Il est courant que 10–20% des séismes manquent une magnitude.

Une magnitude 0 correspond à un événement extrêmement faible, souvent non ressenti.

#### type_magnitude

- certains réseaux ne donnent qu’une magnitude sans type
- magnitudes anciennes (pré-1980) souvent non typées

#### mag_uniforme

Magnitude uniformisée. On calcule une magnitude uniforme approximative mais réaliste à des fins statistiques. Certains types de magnitude ne se prêtent pas à cette normalisation d'où les valeurs manquantes parfois.

#### nb_stations_localisation

La plupart des réseaux modernes ne donnent plus l'information, ou ne la transmettent pas.

manquant = inconnu / non rapporté (pas une erreur)

Quand c’est 0, ça signifie « pas fourni », jamais « 0 station ».

#### nb_stations_magnitude

Très rarement fourni → normal qu'il manque à ~80%.

#### ecart_azimut

- non fourni par certains algorithmes automatiques
- certains réseaux n’utilisent pas cette mesure
- valeurs anciennes avant les années 2000 → souvent vides

#### rms

Manque lorsque :

- trop peu de stations
- calcul non effectué
- algorithme automatique qui échoue

#### erreur_horiz

L’erreur horizontale n’est quasiment jamais fournie dans les catalogues USGS globaux.

Elle existe seulement pour :

- séismes bien localisés
- zones instrumentées
- données récentes

Très normal qu’elle soit manquante pour >90%.

#### erreur_profondeur

beaucoup de séismes n’ont pas d’estimation de l’incertitude

#### erreur_magnitude

La plupart des magnitudes automatiques ne fournissent pas d’erreur.
C’est normal que 80–90% soit manquant.

#### ressenti

La colonne "ressenti" est vide principalement lorsque la magnitude uniformisée (mag_uniforme) est manquante car nous basons notre prédiction dessus.
