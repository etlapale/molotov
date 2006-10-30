<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'wiki.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Next-Touch Wiki - Prévisualisation</title>
  </head>
  <body>
    
    <h1>Prévisualisation</h1>

    <form action="save" method="post">
      <input type="hidden" name="pagename" value="${pagename}"/>
      <textarea name="data" py:content="data" rows="10" cols="70"/>
      <input type="text" name="title" id="title" size="70"
	     value="${modif_title}" />
      <input type="checkbox" name="major" checked="major">Révision
	majeure</input>
      <input type="submit" name="submit" value="Enregistrer"/>
      <input type="submit" name="submit" value="Previsualiser"/>
    </form>

    Retourner sur <a class="wikiname" href="${mltv.url ('/%s' % pagename)}">
      <span py:replace="pagename">Page Name</span></a>.
    
    <div class="preview" py:content="XML(html_data)">Page text goes here</div>
  </body>
</html>
