<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  
  <head>
    <title>Molotov - Register</title>
  </head>

  <body>
    <h2>Inscription</h2>
    <p>
      Indications pour l'inscription :
      <ul>
	<li>Le nom d'utilisateur doit avoir entre 3 et 20 caractères
	  alphanumériques en minuscule et débuter par une lettre
	  (caractères spéciaux autorisés : <code>.</code>, <code>_</code>,
	  <code>-</code>) ;</li>
	<li>Le mot de passe choisit doit être suffisamment complexe ;</li>
	<li>Entrez une adresse e-mail valide.</li>
      </ul>
    </p>
    <form action="do_register" method="post">
      <label>Nom d'utilisateur</label>
      <input type="text" name="name" size="20" value="${name}"/>
      <label>Mot de passe (2 fois)</label>
      <input type="password" name="pass1" size="20" value="${pass1}"/>
      <input type="password" name="pass2" size="20" value="${pass2}"/>
      <label>Adresse e-mail</label>
      <input type="text" name="email" size="20" value="${email}"/>
      <input type="submit" value="Inscription"/>
    </form>
  </body>
</html>
