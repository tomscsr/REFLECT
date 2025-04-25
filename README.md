# REFLECT Project

## 🎯 Description
REFLECT est une application de recommandation beauté qui utilise le machine learning pour analyser votre visage et vous proposer des produits cosmétiques personnalisés.

## ✨ Fonctionnalités
* 📸 Détection en temps réel de la forme du visage
* 🎨 Analyse de la carnation de peau
* 💄 Recommandations personnalisées de produits
* 🛍️ Liste de courses avec liens d'achat
* 💾 Export des recommandations en fichier texte

## 🚀 Installation
1. Clonez le repository :
```bash
git clone https://github.com/votre-username/REFLECT.git
cd REFLECT
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📋 Prérequis
* Python 3.8+
* Webcam fonctionnelle
* Dépendances Python :
  - OpenCV
  - MediaPipe
  - NumPy
  - scikit-learn
  - Tkinter
  - Pillow
  - ttkthemes

## 💻 Utilisation
1. Lancez l'application :
```bash
python app.py
```
2. Positionnez-vous face à la caméra
3. Cliquez sur "Démarrer l'analyse"
4. Consultez vos recommandations personnalisées
5. Optionnel : exportez votre liste de produits

## 🔧 Technologies
* Face Mesh (MediaPipe) pour l'analyse faciale
* KMeans (scikit-learn) pour l'analyse de carnation
* OpenCV pour le traitement d'image
* Tkinter pour l'interface graphique
