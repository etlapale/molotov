<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'wiki.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Molotov - Wiki - Edition</title>
  </head>
  <body>

    <h2>Édition de « <span py:replace="pagename">Page Name</span> »</h2>
    
    <p py:if="not page">La page n'existe pas encore. Elle sera créée
      lors de l'enregistrement.</p>
    <p>La première zone de texte contient le texte de la page. Le champ
      en dessous permet de nommer la modification (optionnel).</p>

    <form action="save" method="post">
      <input type="hidden" name="pagename" value="${pagename}"/>
      <textarea name="data" py:content="data" rows="10" cols="70"/>
      <input type="text" name="title" id="title" size="70" />
      <input type="checkbox" name="major" checked="major">Révision
	majeure (<a href="/PagesWiki#r-visions">à propos
	  des révisions</a>)</input><br/><br/>
      <input type="submit" name="submit" value="Previsualiser"/>
      <input type="submit" name="submit" value="Enregistrer"/>
    </form>

    Retourner sur <a class="wikiname" href="${'/%s' % pagename}">
      <span py:replace="pagename">Page Name</span></a>.
  </body>
</html>
