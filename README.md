# desherbage-vision
# 🌿 Détection automatique de plantes et adventices

Projet académique — Université Clermont Auvergne | L3 EEA | 2025

## Description

Script Python de détection et classification automatique de végétation 
dans des images agricoles, dans le cadre d'un banc d'essais INRAE pour 
des systèmes de désherbage alternatifs aux herbicides.

## Pipeline de traitement
1. Conversion BGR → HSV pour robustesse aux variations d'éclairage
2. Filtrage par plage de teinte (H: 30–80) pour isoler la végétation
3. Nettoyage morphologique (ouverture + fermeture)
4. Détection de contours et calcul des centres de gravité
5. Classification par surface : plante (vert) ou adventice (rouge)
6. Export CSV + images annotées

## Utilisation

```bash
python desherbage.py -i data/ -o resultats/ -p 500
```

| Argument | Description |
|----------|-------------|
| `-i` | Dossier contenant les images d'entrée |
| `-o` | Dossier de sortie pour les résultats |
| `-p` | Seuil de taille en pixels (plante vs adventice) |

## Résultats

| Image | Plantes détectées | Adventices détectées |
|-------|:-----------------:|:--------------------:|
| im000 | ✅ | ✅ |
| im001 | ✅ | ✅ |
| im002 | ✅ | ✅ |
| im003 | ✅ | ✅ |

## Stack technique

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![NumPy](https://img.shields.io/badge/NumPy-latest-orange)
![Pandas](https://img.shields.io/badge/Pandas-latest-purple)

## Auteur

**Houda Karouite** — karouitehouda@gmail.com  
Étudiante en L3 EEA — Recherche alternance Master Systèmes Embarqués (Sept. 2026)
