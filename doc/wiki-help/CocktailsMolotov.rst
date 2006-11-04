=================
Cocktails Molotov
=================

Les cocktails sont les modules constituant votre site web. Parmi les
cocktails de base on trouve un wiki, un gestionnaire de bug, ou encore un
visualiseur de repository subversion. Vous pouvez spécifier les cocktails
à utiliser dans votre site web en utilisant la clé de configuration globale
``molotov.cocktails``.

Un cocktail est simplement un module Python_ avec un controller CherryPy_
à l'intérieur. Certaines variables du module sont utilisées par Molotov
lors du chargement du cocktail. Au minimum la variable ``molotov_controller``
doit contenir la classe du controller du cocktail. ``molotov_name`` permet
de définir un nom d'affichage pour le cocktail.

.. _CherryPy: http://www.cherrypy.org/
.. _Python: http://www.python.org/
