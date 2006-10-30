<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Next-Touch Panel - Register</title>
  </head>
  <body>
    <h1>Inscription</h1>
    <p>
      Ce formulaire vous permet d'accéder au <em>Control Panel</em> de la
      Next-Touch vous permettant de gérer les services que vous utilisez.
    </p>
    <form action="doregister" method="post">
      <label for="username">Nom d'utilisateur</label>
      <input type="textfield" id="username" name="username" size="30"/>
      <label for="realname">Nom réel</label>
      <input type="textfield" id="realname" name="realname" size="30"/>
      <label for="pwd1">Mot de passe</label>
      <input type="password" id="pwd1" name="pwd1" size="30"/>
      <label for="pwd2">Encore une fois</label>
      <input type="password" id="pwd2" name="pwd2" size="30"/>
      <input type="submit" value="Inscription"/>
    </form>
  </body>
</html>
