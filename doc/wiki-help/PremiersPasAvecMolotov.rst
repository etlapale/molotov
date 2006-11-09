=========================
Premiers pas avec Molotov
=========================

Ce document va vous permettre de vous familiariser avec le gestionnaire
de site Molotov_. Molotov a été conçu de façon à simplifier la création et la
gestion de sites web pour des projets informatiques. Il inclut ainsi
un blog (pour les news sur le projet), un wiki (pour la documentation),
un gestionnaire de bugs, différents visualiseurs de repositories
(subversion, bazaar-ng), ...

Installation
------------

Molotov a besoin de quelques programmes et autres bibliothèques pour être
utilisé. Vous avez évidemment besoin de Python mais aussi de CherryPy_,
SQLObject_ (un ORM), de Buffet_ (une interface aux moteurs de templates)
et de Kid_ (un moteur de templates).

Molotov étant simplement une application Python, il n'est donc pas nécessaire
de le compiler pour l'utiliser. Une fois l'archive décompressé, ajoutez son
chemin dans le ``PATH`` (ou utilisez son chemin complet à chaque exécution).
Une fois installé il suffit, comme nous allons le voir, d'utiliser la
commande ``start-start.py`` pour le démarrer.

Premier lancement
-----------------

Pour créer votre site web avec Molotov, commencez par créer un répertoire
qui contiendra les fichiers. Nous dénoterons le chemin y accédant par
``/path/to/mywebapp``. Molotov a besoin d'un fichier de configuration pour
chaque application. Vous pouvez lui donner le nom que vous souhaitez
puisqu'il sera toujours passé en argument au lanceur de Molotov. Notre
configuration initiale sera la suivante ::

  [global]
  molotov.title = "My Website!"
  molotov.sql_engine = "sqlite:///path/to/mywebapp/webapp.sql"

Si vous connaissez CherryPy_, sur lequel Molotov est basé, vous avez pu
remarquer qu'il s'agit un simple fichier de configuration CherryPy. Nous
indiquons qu'il s'agit d'éléments de la configuration globale (par la
première ligne). Les options de configuration sont simplement des paires
clés/valeurs séparés par des symboles ``=``. Dans ce cas nous indiquons
un titre pour notre site ainsi qu'une base de données pour le stockage
des informations (une base sqlite_ dans cet exemple).

Vous pouvez enfin lancer votre application. Par défaut le mode de
développement très verbeux est activé. Vous allez donc voir apparaître un
certain nombre de lignes sur la console, nous ne les affichons pas toutes
ici ::

  /path/to/mywebapp $ molotov-start.py my_app.conf
  2006-11-06 23:28:10,974 [molotov] DEBUG: Loading cocktails: ['wiki', 'user']
  2006-11-06 23:28:10,974 [molotov] DEBUG:   Init cocktail blog
  ...
  06/Nov/2006:23:28:12 CONFIG INFO   server.thread_pool: 10
  06/Nov/2006:23:28:12 HTTP INFO Serving HTTP on http://localhost:8080/

Comme vous pouvez le constater, le serveur écoute par défaut sur le port
8080 de l'interface ``localhost``. Il ne vous reste plus qu'à entrer l'URL
dans votre navigateur favori. Vous accèderez alors directement à l'aide
en-ligne de Molotov au travers du cocktail wiki.

Cocktails
---------

Les cocktails sont les modules de Molotov. Ils sont dynamiquement chargés
en fonction de vos besoins. Par défaut, dans notre application précédente
par exemple, Molotov charge uniquement les cocktails **wiki** et **user**
(le second étant une interface au gestionnaire d'utilisateurs). Si vous
vouliez aussi charger un cocktail pour gérer les bugs de votre programme
vous pourriez utiliser la ligne suivante dans votre fichier de
configuration ::
  
  molotov.cocktails = "wiki, tickets, user"

Certains cocktails peuvent aussi avoir besoin de paramètres. Par exemple
le cocktail subversion nécessite le chemin vers la repository ::
  
  molotov.cocktails = "wiki, svn, tickets, user"
  molotov.cocktails.svn.repo_path = "/var/svn/helloworld"


Look and Feel
-------------

Il est possible de modifier l'apparence de sites web basé sur Molotov à
différents niveaux. Le niveau le plus simple consiste à modifier les
feuilles de style utilisées par le template par défaut. Le template standard
indique au de chercher les feuilles CSS dans l'URL ``/static``
qui mappe directement le répertoire ``static`` de l'installation de Molotov.
Il vous suffit de remapper cette URL vers votre propre répertoire de feuilles
de style et de les créer. Dans l'exemple suivant nous copions et modifions
les feuilles CSS standard ::

  $ cp -r /path/to/molotov/share/static /path/to/mywebapp
  $ cat >> /path/to/mywebapp/my_app.conf << EOF
  [/static]
  static_filter.on = True
  static_filter.dir = "/path/to/mywebapp/static"
  EOF
  $ vi /path/to/mywebapp/static/css/colors.css

Nous avons recopié, modifié et remappé le répertoire ``static`` par défaut
de Molotov qui contient des CSS, des images et autres fichiers JavaScript.
Nous aurions aussi pu nous contenter de remapper l'URL ``/static/css``.
Le paramètre ``static_filter.on`` est ici redondant puisque déjà présent
dans la configuration de base, mais nous l'ajoutons pour plus de clarté.
Évidemment il s'agit d'une configuration CherryPy standard et vous êtes
invité à en lire la documentation pour plus d'informations.

Le fichier ``colors.css`` que nous avons ici édité est celui qui définit les
couleurs utilisées par défaut. Il est inclus dans la CSS ``molotov.css`` du
même répertoire, elle-même liée par la page de template maître à
l'aide d'une ligne de la forme ::

  <link rel="stylesheet" type="text/css" href="/static/css/molotov.css"/>

.. _Buffet: http://www.buffet.org/
.. _CherryPy: http://www.cherrypy.org/
.. _Kid: http://www.kid-templating.org/
.. _Molotov: http://molotov.next-touch.com/
.. _SQLObject: http://www.sqlobject.org/
.. _sqlite: http://www.sqlite.org/
