PROJ0001-Projet 🚀

Projet de groupe en langage Python effectué dans le cadre du cours d'Introduction aux méthodes numériques et projet (PROJ0001).
L'énoncé du projet se trouve dans le fichier Enonce_2025.pdf.

📋 Table des matières

1. Qu'est-ce que Git?


2. Installation de Git

Sur Windows

Sur macOS

Sur Linux



3. Utilisation de Git via le Terminal

Cloner un dépôt

Pull (Mettre à jour votre dépôt local)

Commit (Enregistrer vos modifications)

Push (Envoyer vos modifications sur GitHub)



4. Utilisation de GitHub Desktop

Cloner un dépôt

Pull (Mettre à jour votre dépôt local)

Commit (Enregistrer vos modifications)

Push (Envoyer vos modifications sur GitHub)



5. Rapport

Installation

Utilisation

Attention



6. Conclusion




---

Qu'est-ce que Git? 🤔

Git est un système de contrôle de version qui permet de suivre les modifications apportées à des fichiers au fil du temps. Il est particulièrement utile pour les projets de développement logiciel, car il permet à plusieurs personnes de collaborer sur le même projet sans conflit.

Installation de Git 💻

Sur Windows

1. Téléchargez Git depuis git-scm.com


2. Suivez les instructions d'installation



Sur macOS

1. Ouvrez le Terminal


2. Installez Git avec Homebrew :

brew install git



Sur Linux

1. Ouvrez le Terminal


2. Installez Git avec la commande suivante :

sudo apt-get install git



Utilisation de Git via le Terminal ⌨️

Cloner un dépôt

git clone https://github.com/username/repository.git

Remplacez username par le nom d'utilisateur GitHub et repository par le nom du dépôt.

Pull (Mettre à jour votre dépôt local)

git pull origin main

Cela mettra à jour votre branche locale avec les dernières modifications de la branche main.

Commit (Enregistrer vos modifications)

1. Ajoutez les fichiers modifiés à l'index :

git add .


2. Enregistrez les modifications avec un message descriptif :

git commit -m "Votre message de commit ici"



Push (Envoyer vos modifications sur GitHub)

git push origin main

Cela enverra vos modifications sur la branche main du dépôt distant.

Utilisation de GitHub Desktop 🖥️

Cloner un dépôt

1. Ouvrez GitHub Desktop


2. Cliquez sur File > Clone Repository


3. Sélectionnez le dépôt et choisissez l'emplacement sur votre machine



Pull (Mettre à jour votre dépôt local)

1. Ouvrez GitHub Desktop


2. Sélectionnez le dépôt


3. Cliquez sur Fetch origin, puis sur Pull origin si des mises à jour sont disponibles



Commit (Enregistrer vos modifications)

1. Ouvrez GitHub Desktop


2. Ajoutez un message de commit


3. Cliquez sur Commit to main



Push (Envoyer vos modifications sur GitHub)

1. Après avoir commité vos modifications, cliquez sur Push origin



📝 Rapport

Le rapport se trouve dans le fichier :

PROJ0001-Projet/Rapport

Il s'agit d'un document LaTeX créé sur Overleaf. Pour le mettre à jour, il faut lier son compte Overleaf à GitHub pour ensuite pousser les modifications sur le dépôt.

📦 Installation

Pour cloner le rapport sur Overleaf et le modifier :

1. Lier son compte Overleaf à GitHub :

Aller dans Account -> Project Synchronisation -> GitHub Sync



2. Créer un nouveau projet :

New Project -> Import from GitHub -> benjamin-bock/PROJ0001-Projet



3. Changer le compilateur en XeLaTeX ou LuaLaTeX :

Menu -> Settings -> Compiler




🛠️ Utilisation

Pour sauvegarder des modifications sur Overleaf :

Menu -> Sync -> GitHub -> Push Overleaf changes to GitHub

⚠️ Attention

Toujours faire un pull avant de travailler sur le rapport !
Cela évite les conflits et les duplications de travail.

Pour faire un pull :

Menu -> Sync -> GitHub -> Pull changes from GitHub

Conclusion 🎉

Que vous utilisiez le terminal ou GitHub Desktop, Git est un outil puissant pour gérer vos projets de développement. Grâce à ce guide, vous devriez être en mesure de cloner, mettre à jour, enregistrer et envoyer vos modifications sur GitHub. Bon codage !

Si vous avez des questions, consultez la documentation officielle de Git ou posez vos questions sur les forums de la communauté GitHub.


---

Tu peux copier-coller ce fichier directement en tant que README.md dans ton projet GitHub

