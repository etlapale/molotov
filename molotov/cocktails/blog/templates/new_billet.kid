<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <h1>New blog billet</h1>
    <form action="do_new_billet" method="post">
      <label>Titre</label>
      <input type="text" name="title" size="20"/>
      <label>Texte</label>
      <textarea name="data" cols="50" rows="15"/>
      <input type="submit" value="poster"/>
    </form>
  </body>
</html>

