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
    <div py:if="not data is None" class="blog_billet">
      <h1 py:content="title">Billet title</h1>
      <div py:replace="XML (rst2html (data))">Billet text goes here.</div>
    </div>
    <form action="do_new_billet" method="post">
      <label>Titre</label>
      <input type="text" name="title" size="20" value="${title}"/>
      <label>Utilisateur</label>
      <input type="text" disabled="disabled" py:if="not mltv_user is None" value="${mltv_user}"/>
      <p py:if="mltv_user is None">Vous n'êtes pas identifié.</p>
      <label>Texte</label>
      <textarea name="data" cols="50" rows="15">
	<span py:if="data" py:replace="data"/>
      </textarea>
      <div py:if="data is None">
	<input type="submit" name="submit" value="preview"/>
	<input type="submit" name="submit" value="poster"/>
      </div>
      <div py:if="not data is None">
	<input type="submit" name="submit" value="poster"/>
	<input type="submit" name="submit" value="preview"/>
      </div>
    </form>
  </body>
</html>

