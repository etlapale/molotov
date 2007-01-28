<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <h1>NXPanel -- Email</h1>

    <p py:if="not emails">Vous ne possédez pas de compte e-mail!</p>
    <p py:if="emails">
      Vous avez ouvert <strong py:replace="len(emails)"/> comptes emails.
      Vous pouvez les consulter via le
      <a href="http://webmail.next-touch.com/">webmail</a> ou en configurant
      un client email (vous pourrez consultez le wiki pour
      plus d'informations).
    </p>
    
    <strong>Comptes</strong>
    <ul>
      <li py:for="email in emails" py:content="email.email"/>
    </ul>
    
    <strong>Alias</strong>
    <ul>
      <li py:for="alias in mailaliases"
	  py:content="alias.email + ' => ' + alias.target"/>
    </ul>
	
    <h2>Créer un alias</h2>
    <p>
      Vous pouvez créer une addresse d'alias. Tous les emails envoyés à
      cette adresse seront renvoyés vers une adresse de votre choix.
    </p>

    <form method="post" action="create_alias">
      <label>Adresse d'alias (la nouvelle)</label>
      <input type="text" name="alias"/>
      <label>Addresse cible (l'existante)</label>
      <input type="text" name="target"/>
      <input type="submit" value="OK"/>
    </form>
    
    <h2>Créer un compte e-mail</h2>
    <p>
      Les comptes créés sur le serveur doivent impérativement être
      de la forme <code>user@domain.nm</code> où <code>user</code>
      est un nom d'utilisateur simple (n'utilisez que des caractères
      alphanumériques et l'un des <code>.-_</code>) et <code>domain.nm</code>
      doit être choisi parmis :
      <ul class="simplelist">
	<li py:for="host in domains" py:content="host">domain.nm</li>
      </ul>
    </p>
    <form method="post" action="create_email">
      <label>Adresse e-mail (2 fois)</label>
      <input type="text" name="address1" size="20"/>
      <input type="text" name="address2" size="20"/>
      <label>Entrez deux fois le mot de passe</label>
      <input type="password" name="pass1" size="20"/>
      <input type="password" name="pass2" size="20"/>
      <input type="submit" value="OK"/>
    </form>
    
    <p><a href="nxpanel">Retourner au centre de contrôle</a></p>
  </body>
</html>
