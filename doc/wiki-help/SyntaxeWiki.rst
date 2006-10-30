============
Syntaxe Wiki
============

Une syntaxe wiki se doit d'être simple afin que la source des pages wiki soit
facilement lue et modifiée. Dans cette optique Molotov_ a choisit d'utiliser
la syntaxe reStructuredText_, définie par docutils_, pour ses pages. Ceci
permet d'utiliser directement le moteur docutils_ et d'avoir une syntaxe
standard et simple pour l'édition des pages.

Ce document ne décrit qu'une partie de la syntaxe de reStructuredText_.
N'hésitez pas à consulter la source reStructuredText_ des pages de la
documentation.

Formatage basique
-----------------

Le formatage en-ligne regroupe des attributs appliqués à des portions,
générallement petite, d'un texte. Quelques exemples d'utilisation :

    ``*texte en italique*``  *texte en italique*
                             
    ``**texte en gras**``    **texte en gras**
                             
    ````Code en ligne````    ``Code en ligne``

Les pages wiki en reStructuredText_ sont simplement constitués de paragraphes
séparés par des lignes vides. Ainsi le saut de ligne est considéré comme un
espace classique afin de permettre, par exemple, de n'utiliser que 80 colonnes.

Le texte::

    Ce paragraphe possède une source
    s'étalant sur plusieurs lignes
    sans que cela affecte le rendu.
    
    Ce paragraphe est le second

Va être rendu par :

    Ce paragraphe possède une source
    s'étalant sur plusieurs lignes
    sans que cela affecte le rendu.
    
    Ce paragraphe est le second

Titres et sections
------------------

Les documents reStructuredText_, en particulier les pages wiki Molotov,
peuvent être découpé hiérarchiquement en différentes sections et sous-sections.
Chacune des section possède un titre qui permet donc de les séparer. Pour
définir un titre de section il suffit de le souligner (ou de le surligner
et le souligner) à l'aide de caractères spécifiques (par exemple ``-``
ou ``=``). On peut par exemple avoir ::

    ================
    Titre de ma page
    ================
    
    Texte d'introduction à placer ici.
    
    Première section
    ----------------
    
    Texte de la première section.
    
    Seconde section
    ---------------
    
    Sous-section a
    ~~~~~~~~~~~~~~
    
    Bla bla
    
    Sous-section b
    ~~~~~~~~~~~~~~
    
    Alb alb

Comme vous pouvez le constater, les sections peuvent s'emboîter de façon
à former une structure hiérarchique. L'ornement des titre (qui est soit un
soulignage soit un surlignage et un soulignage) est librement choisit mais
deux titres de section au même niveau hiérarchique (par exemple deux titres
de chapitres) doivent posséder les mêmes ornements. Le titre de la page
possède un ornement différent de tous les autres.

Notez que si vous faites immédiatemment suivre le titre de la page d'un
autre titre (avec une soulignement différent) celui-ci sera considéré comme
un sous-titre de la page.

Les caractères d'ornement sont à choisir de préférence parmis ::

    = - ` : ' " ~ ^ _ * + # < >

Références
----------

Les références en-ligne à d'autres pages wiki se font simplement en insérant
leur nom dans le texte. Elle seront reconnues au fait qu'elles sont sous
forme de WikiName (plusieurs mots débutant chacun par une majuscule et collés
entre eux sans espaces), par exemple SyntaxeWiki, FrontPage ou ContenuDeLAide.
Ces liens wiki sont une extension par rapport à la syntaxe reStructuredText_
standard.

Notez que des liens implicites sont formés lors de l'utilisation d'URL ou
d'adresse e-mails, par exemple http://www.next-touch.com/ ou
neil-nospam@next-touch.com.

Pour d'autres types de références, on utilise la syntaxe reStructuredText_,
en suffixant simplement un *underscore* ``_`` à la référence. On peut ensuite
spécifier l'adresse vers laquelle pointe cette référence. Un simple exemple :
TurboGears est écrit en Python_.
::

    TurboGears est écrit en Python_.
    
    .. _ Python: http://www.python.org/

Notez que la deuxième ligne est une directive reStructuredText_ définissant
le lien et peut être placée n'importe où dans le texte (par exemple avec
d'autres références en fin de document).

Il est possible de faire des références en précisant en même temps dans le
texte l'URL vers laquelle elle pointe, mais cela présente l'incovénient de
nuire à la lisibilité. Allez voir la documentation de reStructuredText_ si
vous souhaitez le faire.

Les titres du document peuvent aussi être référencés, par exemple pour avoir
un lien vers les section `Formatage basique`_ ou Références_.
::

    lien vers les section `Formatage basique`_ ou Références_

Vous pouvez constater qu'il est possible d'utiliser à la fois des mots
mais aussi des chaînes de caractères plus complexes, contenant par exemple
des espaces ou de la ponctuation, en les encadrant de *backquotes* `````.

Les notes de pied de page sont définie en utilisant la forme ``[n]_`` où ``n``
est le numéro de la note. Elle est ensuite définie de façon classique à l'aide
d'une directive telle que ``.. [n] Texte de la note``. Pour utiliser
l'auto-numérotation, utilisez ``#`` plutôt qu'un numéro. Si vous utilisez
une astérisque ``*``, différents symboles seront utilisé plutôt que des
numéros. Exemple de rendu [#]_.

Les citations peuvent être utilisées de la même manière que les notes de
pied de page en spécifiant un label plutôt que ``#``, ``*`` ou qu'un numéro.
Par exemple ``[BLA05]_`` va donner [BLA05]_.

Images et Substitutions
-----------------------

Les substitutions s'utilisent en encadrant du texte par des *pipes* ``|``
puis en définissant la valeur de substitution en tant que directive. Ces
substitutions sont notamment utilisées avec des images. Un exemple ::

    |work| Travail à faire
    
    .. |work| image:: static/images/work-32x32.png

va donner :

    |work| Travail à faire.
    
    .. |work| image:: static/images/work-32x32.png

Listes
------

Les listes simples sont définies en préfixant chaque élément d'un symbole
parmis ``-``, ``*`` et ``+``. L'identation d'un élément doit être respecté
s'il est multiligne. Un exemple ::

    - premier élément de la liste ;
    - second élément de la liste qui
      est lui multi-ligne ;
    - troisième et dernier élément.

qui va donner :

    - premier élément de la liste ;
    - second élément de la liste qui
      est lui multi-ligne ;
    - troisième et dernier élément.

Les listes énumérées sont préfixées d'un dièse suivit d'un point ``#.``,
pour une auto-numérotation, ou d'un numéro suivit d'un point pour une
numérotation explicite.
::

    3. premier élément de la liste ;
    #. second élément de la liste qui
       est lui multi-ligne ;
    #. troisième et dernier élément.

aura pour résultat :

    3. premier élément de la liste ;
    #. second élément de la liste qui
       est lui multi-ligne ;
    #. troisième et dernier élément.

Une liste de définition peut être obtenue de la façon suivante ::

    D'où vient Molotov_ ?
      Molotov_ est une création de la Next-Touch destiné
      initialement à servir de wiki ainsi que de *Control Panel*
      pour aider les membres à gérer leur services.
    
    Puis-je utiliser Molotov_ ?
      Molotov_ est évidemment librement utilisable et modifiable
      dès lors que vous respectez sa licence libre. Il a été conçu
      de façon à être facilement modulable.

Pour avoir :

    D'où vient Molotov_ ?
      Molotov_ est une création de la Next-Touch destiné
      initialement à servir de wiki ainsi que de *Control Panel*
      pour aider les membres à gérer leur services.
    
    Puis-je utiliser Molotov_ ?
      Molotov_ est évidemment librement utilisable et modifiable
      dès lors que vous respectez sa licence libre. Il a été conçu
      de façon à être facilement modulable.

Tableaux
--------

Il existe deux types de tableaux en reStructuredText_ : les tableaux *en grille*
et les tableaux simples. Les tableaux en grille possède une apparence textuelle
plus travaillée mais sont donc plus long à écrire. Les tableaux simples sont
plus rapide à écrire mais aussi plus limités. Un petit exemple ::

    +----------+----------+---------------+
    |  Offset  |  Taille  |  Description  |
    +==========+==========+===============+
    |    0     |    24    | Magic number  |
    +----------+----------+---------------+
    |    24    |     8    |    Taille     |
    +----------+----------+---------------+
    |    32    | Tableau spammé ! (SPAM)  |
    +----------+----------+---------------+
    |    36    |    28    |  Non utilisé  |
    +----------+----------+---------------+

Qui va donner :

    +----------+----------+---------------+
    |  Offset  |  Taille  |  Description  |
    +==========+==========+===============+
    |    0     |    24    | Magic number  |
    +----------+----------+---------------+
    |    24    |     8    |    Taille     |
    +----------+----------+---------------+
    |    32    | Tableau spammé ! (SPAM)  |
    +----------+----------+---------------+
    |    36    |    28    |  Non utilisé  |
    +----------+----------+---------------+

.. [#] Exemple de note de pied de page.
.. [BLA05] Blatahut, 2005, *De l'utilisation du bla en société*
.. _Molotov: http://molotov.next-touch.com/
.. _Python: http://www.python.org/
.. _docutils: http://docutils.sourceforge.net/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
