<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <div py:for="b in billets" class="blog_billet">
      <h2 py:content="b.title">Billet title</h2>
      <div py:replace="XML (rst2html (b.data))">Billet text goes here.</div>
    </div>
    <p><a href="new_billet">Poster un billet</a></p>
  </body>
</html>
    
