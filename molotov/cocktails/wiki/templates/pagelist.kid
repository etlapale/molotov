<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'wiki.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <h2>Liste des Pages</h2>
    <ul>
      <li py:for="pagename in pages">
	<a href="${'/' + pagename}"
	   py:content="pagename">PageName Here</a></li>
    </ul>
  </body>
</html>
