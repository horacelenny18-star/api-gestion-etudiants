📋 Rapport Technique : API REST - Gestion des Étudiants
1. Description du projet et Diagramme de cas d'utilisation
Ce projet a pour objectif de concevoir et déployer une API REST sous Python (Flask) connectée à une base de données relationnelle MySQL (ciel2027), hébergée sur un Raspberry Pi. L'API permet d'interagir avec les données des étudiants de manière sécurisée.

Plaintext
                  +-------------------------------------------------+
                  |                   UTILISATEUR                   |
                  |          (Postman / Client Externe)             |
                  +-------------------------------------------------+
                                       |
                                       | Envoie des requêtes HTTP 
                                       | (GET, POST, PUT, DELETE) + Basic Auth
                                       v
                  +-------------------------------------------------+
                  |              SERVEUR API (Flask)                |
                  |                - api_v4.py                      |
                  +-------------------------------------------------+
                                       |
                                       | Valide l'authentification & 
                                       | exécute les requêtes SQL
                                       v
                  +-------------------------------------------------+
                  |          BASE DE DONNÉES (MySQL)                |
                  |          - Table 'user' (Auth)                  |
                  |          - Table 'etudiants'                    |
                  +-------------------------------------------------+
2. Récapitulatif des 4 versions de l'API
api_v1.py : Version initiale de base, mise en place des routes fondamentales pour l'affichage de données simples.

api_v2.py : Ajout et structuration des opérations CRUD (endpoints pour l'insertion et la suppression de données d'étudiants).

api_v3.py : Évolution des routes vers la version 3 et intégration d'une logique de base pour la gestion des connexions.

api_v4.py : Version finale et stable. Intégration d'un système de sécurité robuste par Basic Auth via la table user, et connexion optimisée avec la base de données ciel2027 sur le Raspberry Pi.

3. Diagramme de classes (Généré par pyreverse)
Pour générer automatiquement le diagramme de classes de la classe Database (contenue dans db.py), les commandes suivantes ont été exécutées dans le terminal du Raspberry Pi :

Bash
python3 -m pip install pylint
pyreverse -o jpg db.py
Cette manipulation génère un fichier image (classes_db.png) illustrant les attributs et méthodes de la classe Database interagissant avec MySQL.

4. Fiche des tests de l'API (Postman)
Outil utilisé : Postman

Mode d'authentification : Basic Auth (extern_user / Bt5@c13l972)

Endpoint testé : GET [http://192.168.14.153:5000/v4/etudiants/](http://192.168.14.153:5000/v4/etudiants/)

Résultat obtenu :

Code HTTP : 200 OK

Corps de la réponse : Restitution au format JSON de la liste complète des étudiants enregistrés en base de données.

5. Conclusion et Améliorations en Cybersécurité
Le déploiement de cette API sur Raspberry Pi a permis de valider l'ensemble du cycle de développement d'une application connectée (du code Flask à la base de données MySQL et aux tests d'intégration).

Plusieurs pistes d'amélioration en termes de cybersécurité peuvent être envisagées pour les versions futures :

Hachage des mots de passe : Remplacer le stockage des mots de passe en clair par des fonctions de hachage sécurisées (ex: bcrypt ou Argon2).

Utilisation de JSON Web Tokens (JWT) : Remplacer ou compléter la Basic Auth par un système de jetons JWT pour une gestion des sessions plus granulaire et sécurisée.

Chiffrement des flux (HTTPS) : Implémenter un certificat SSL/TLS (via Let's Encrypt ou un certificat auto-signé) pour chiffrer les échanges HTTP et éviter l'interception des identifiants en clair sur le réseau local.

Validation stricte des entrées : Mettre en place des mécanismes avancés de nettoyage et de validation des données pour prémunir l'API contre les injections SQL et les failles XSS.
