<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  
  <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'"
	py:attrs="item.items()">
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Molotov - Wiki</title>
    <meta py:replace="item[:]"/>
  </head>

  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'"
	py:attrs="item.items()">

    <!-- Wiki toolbox -->
    <div class="toolbox">
      <strong>Wiki</strong>
      <ul>
	<li><a href="${mltv.url ('/')}">Page d'Accueil</a></li>
	<li><a href="/ContenuDeLAide">Contenu de l'Aide</a></li>
	<li><a href="/pagelist">Liste des Pages</a></li>
      </ul>
      <div py:if="page">
	<strong>Page</strong>
	  <ul>
	    <li><a href="${'/edit?pagename=%s' % page.pagename}">Éditer la Page</a></li>
	    <li><a href="${'/modifs?pagename=%s' % page.pagename}">Modifications</a></li>
	    <li>Formats :
	      <a href="${mltv.url ('/', pagename=page.pagename, format='plain')}">Plain</a> |
	      <a href="${mltv.url ('/', pagename=page.pagename, format='xml')}">XML</a>
	    </li>
	  </ul>
	</div>
    </div>

    <!-- Main page content -->
    <div py:replace="[item.text]+item[:]"/>
  </body>
</html>
