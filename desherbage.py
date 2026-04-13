# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:14:57 2026
@author: User

Utilisation :
    python desherbage.py -i data/ -o resultats/ -p 500
"""
import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
 
# Gestion des arguments en ligne de commande

parser = argparse.ArgumentParser(description="Projet 2026 - Plantes / Adventices")
parser.add_argument("-i", "--input",           required=True, help="Dossier d'entrée")
parser.add_argument("-o", "--output",          required=True, help="Dossier de sortie")
parser.add_argument("-p", "--plant_threshold", required=True, type=int,
                    help="Seuil de taille (pixels) pour différencier plantes/adventices")
args = parser.parse_args()

input_dir  = args.input
output_dir = args.output
taille     = args.plant_threshold

# Création du dossier de sortie
os.makedirs(output_dir, exist_ok=True)


# Récupération de toutes les images du dossier d'entrée
noms_images = sorted([
    f for f in os.listdir(input_dir)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"))
])

images = []
images_hsv = []
masks = []
plt.figure(figsize=(10,8))
results=[]
csv_data = []
# Chargement et conversion des images en HSV + flou pour réduire le bruit
for image in noms_images:
    img = cv2.imread(os.path.join(input_dir, image))
    images.append(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (1,1), 0)
    images_hsv.append(hsv)

# Création du masque vert : on isole les pixels correspondant à la végétation
# puis on applique une ouverture/fermeture pour supprimer le bruit et boucher les trous
for hsv in images_hsv:
    mask = cv2.inRange(hsv, (30, 50, 50), (80, 255, 255))
    kernel = np.ones((8,8), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    masks.append(mask)

# Traitement image par image
for i in range(len(images)):
    plantes = []
    adventices = []
    result = images[i].copy()

    # Masques séparés pour visualiser plantes et adventices individuellement
    mask_plantes    = np.zeros_like(masks[i])
    mask_adventices = np.zeros_like(masks[i])

    # Détection des contours sur le masque vert
    contours, _ = cv2.findContours(masks[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for objet in contours:
        surface = cv2.contourArea(objet)
        M = cv2.moments(objet)
        if M["m00"] == 0:
            continue
        
        # Calcul du centre de gravité
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Classification : grande surface = plante, petite surface = adventice
        if (surface >= taille):
            plantes.append((cx, cy))
            cv2.circle(result, (cx, cy), 6, (0,255,0), -1)  # vert
            cv2.drawContours(mask_plantes, [objet], -1, 255, -1)  
            csv_data.append({
            "image": noms_images[i],
            "type": "plante",
           "x": cx,
           "y": cy
        })
        else:
            adventices.append((cx, cy))
            cv2.circle(result, (cx, cy), 4, (0,0,255), -1)  # rouge
            cv2.drawContours(mask_adventices, [objet], -1, 255, -1)  
            csv_data.append({
            "image": noms_images[i],
            "type": "adventice",
            "x": cx,
            "y":cy
        })
    results.append(result)

    # Affichage des 6 vues pour chaque image
    plt.subplot(len(images),6,6*i+1)
    plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    plt.title("image initiale")

    plt.subplot(len(images),6,6*i+2)
    plt.imshow(images_hsv[i])
    plt.title("image HSV")

    plt.subplot(len(images),6,6*i+3)
    plt.imshow(cv2.cvtColor(results[i], cv2.COLOR_BGR2RGB))
    plt.title("resultat")

    plt.subplot(len(images),6,6*i+4)
    plt.imshow(masks[i], cmap="gray")
    plt.title("Mask vert")
    
    plt.subplot(len(images),6,6*i+5) 
    plt.imshow(mask_plantes, cmap="gray")  
    plt.title("Mask plantes") 
    
    
    plt.subplot(len(images),6,6*i+6)  
    plt.imshow(mask_adventices, cmap="gray") 
    plt.title("Mask adventices")  
    plt.tight_layout()

    # Sauvegarde des images de résultat dans le dossier de sortie
    base = os.path.splitext(noms_images[i])[0]
    cv2.imwrite(os.path.join(output_dir, f"{base}_resultat.png"), results[i])
    cv2.imwrite(os.path.join(output_dir, f"{base}_masque.png"),   masks[i])
    cv2.imwrite(os.path.join(output_dir, f"{base}_mask_plantes.png"),    mask_plantes)     
    cv2.imwrite(os.path.join(output_dir, f"{base}_mask_adventices.png"), mask_adventices)

    # Export CSV global avec les coordonnées de tous les objets détectés  
    df = pd.DataFrame(csv_data)
    csv_path = os.path.join(output_dir, "resultats.csv")
    df.to_csv(csv_path, index=False)
    print(" CSV généré !")
    print(f"[OK] {noms_images[i]} -> sauvegardé dans {output_dir}/")

plt.show()
