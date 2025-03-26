# PROJ0001-Projet 🚀
Projet de groupe en langage Python effectué dans le cadre du cours d'Introduction aux méthodes numériques et projet (PROJ0001).
L'énoncé du project se trouve dans le fichier Enonce_2025.pdf

## Guide d'utilisation de Git: Pull, Commit et Push 🔄

Ce guide est conçu pour vous aider à comprendre les bases de Git et comment effectuer les opérations courantes comme `pull`, `commit` et `push`, à la fois via le terminal et GitHub Desktop. Parfait pour les débutants!

### 📋 Table des matières
1. [Qu'est-ce que Git?](#quest-ce-que-git)
2. [Installation de Git](#installation-de-git)
3. [Utilisation de Git via le Terminal](#utilisation-de-git-via-le-terminal)
   - [Cloner un dépôt](#cloner-un-dépôt)
   - [Pull (Mettre à jour votre dépôt local)](#pull-mettre-à-jour-votre-dépôt-local)
   - [Commit (Enregistrer vos modifications)](#commit-enregistrer-vos-modifications)
   - [Push (Envoyer vos modifications sur GitHub)](#push-envoyer-vos-modifications-sur-github)
4. [Utilisation de GitHub Desktop](#utilisation-de-github-desktop)
   - [Cloner un dépôt](#cloner-un-dépôt-1)
   - [Pull (Mettre à jour votre dépôt local)](#pull-mettre-à-jour-votre-dépôt-local-1)
   - [Commit (Enregistrer vos modifications)](#commit-enregistrer-vos-modifications-1)
   - [Push (Envoyer vos modifications sur GitHub)](#push-envoyer-vos-modifications-sur-github-1)
5. [Conclusion](#conclusion)

---

## Qu'est-ce que Git? 🤔

Git est un système de contrôle de version qui permet de suivre les modifications apportées à des fichiers au fil du temps. Il est particulièrement utile pour les projets de développement logiciel, car il permet à plusieurs personnes de collaborer sur le même projet sans conflit.

## Installation de Git 💻

### Sur Windows
1. Téléchargez Git depuis [git-scm.com](https://git-scm.com/)
2. Suivez les instructions d'installation

### Sur macOS
1. Ouvrez le Terminal
2. Installez Git avec Homebrew:
   ```bash
   brew install git
   ```

### Sur Linux
1. Ouvrez le Terminal
2. Installez Git avec la commande suivante:
   ```bash
   sudo apt-get install git
   ```

## Utilisation de Git via le Terminal ⌨️

### Cloner un dépôt

Pour commencer à travailler sur un projet, vous devez d'abord cloner le dépôt (repository) sur votre machine locale.

```bash
git clone https://github.com/username/repository.git
```

Remplacez `username` par le nom d'utilisateur GitHub et `repository` par le nom du dépôt.

### Pull (Mettre à jour votre dépôt local)

Avant de commencer à travailler, il est important de s'assurer que votre dépôt local est à jour avec le dépôt distant.

```bash
git pull origin main
```

Cela mettra à jour votre branche locale avec les dernières modifications de la branche `main` (ou `master` selon le dépôt).

### Commit (Enregistrer vos modifications)

Après avoir apporté des modifications à vos fichiers, vous devez les enregistrer (commit) dans l'historique de Git.

1. Ajoutez les fichiers modifiés à l'index:
   ```bash
   git add .
   ```
   Cela ajoute tous les fichiers modifiés. Vous pouvez aussi ajouter des fichiers spécifiques en remplaçant `.` par le nom du fichier.

2. Enregistrez les modifications avec un message descriptif:
   ```bash
   git commit -m "Votre message de commit ici"
   ```

### Push (Envoyer vos modifications sur GitHub)

Une fois que vous avez commité vos modifications, vous pouvez les envoyer (push) sur le dépôt distant.

```bash
git push origin main
```

Cela enverra vos modifications sur la branche `main` du dépôt distant.

## Utilisation de GitHub Desktop 🖥️

GitHub Desktop est une application graphique qui simplifie l'utilisation de Git. Voici comment effectuer les mêmes opérations avec GitHub Desktop.

### Cloner un dépôt

1. Ouvrez GitHub Desktop
2. Cliquez sur `File > Clone Repository`
3. Sélectionnez le dépôt que vous souhaitez cloner et choisissez l'emplacement sur votre machine

### Pull (Mettre à jour votre dépôt local)

1. Ouvrez GitHub Desktop
2. Sélectionnez le dépôt que vous souhaitez mettre à jour
3. Cliquez sur `Fetch origin` pour vérifier les mises à jour
4. Si des mises à jour sont disponibles, cliquez sur `Pull origin` pour les appliquer

### Commit (Enregistrer vos modifications)

1. Après avoir modifié des fichiers, ouvrez GitHub Desktop
2. Les fichiers modifiés apparaîtront dans la section `Changes`
3. Ajoutez un message de commit dans la zone de texte en bas à gauche
4. Cliquez sur `Commit to main` (ou la branche sur laquelle vous travaillez)

### Push (Envoyer vos modifications sur GitHub)

1. Après avoir commité vos modifications, cliquez sur `Push origin` en haut à droite
2. Vos modifications seront envoyées sur le dépôt distant

## Conclusion 🎉

Que vous utilisiez le terminal ou GitHub Desktop, Git est un outil puissant pour gérer vos projets de développement. Avec ce guide, vous devriez être en mesure de cloner, mettre à jour, enregistrer et envoyer vos modifications sur GitHub. Bon codage!

Si vous avez des questions ou des problèmes, n'hésitez pas à consulter la [documentation officielle de Git](https://git-scm.com/doc) ou à poser des questions sur les forums de la communauté GitHub.


# 📝 **Rapport**

Le Rapport se trouve dans le fichier 
```bash
PROJ0001-Projet/Rapport
```
Il s'agit d'un document LaTeX fait sur Overleaf. Pour le mettre à jour il faut lier son compte Overleaf à GitHub pour pouvoir ensuite push les modifications sur le repo ci-présent.

## 📦 **Installation**

Pour cloner le Rapport sur Overleaf afin de pouvoir le modifier confortablement il faut :

```bash
1. Lier son compte Overleaf à GitHub :
  Account -> Project Synchronisation -> GitHub Sync

2. Créer un nouveau projet:
  New Project -> Import from GitHub -> benjamin-bock/PROJ0001-Projet

3. Changer le compilateur en XeLaTeX ou LuaLaTeX :
  Menu -> Settings -> Compiler
```
## 🛠️ **Utilisation**

Pour sauvegarder des modifications, tout se fait sur Overleaf :

```bash
Dans le projet,

Menu -> Sync -> GitHub -> Push Overleaf changes to GitHub
```

## ⚠️ **Attention**
N'oubliez pas de pull à chaque fois que vous allez travailler sur le rapport. Cela évite de refaire ce qu'un autre a peut-être déjà fait et cela évite les collisions. La marche à suivre pour faire un pull est la même que pour push, il suffit de choisir pull sur la fenêtre de synchronisation.