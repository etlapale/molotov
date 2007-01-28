<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <h1>NXPanel</h1>
    <p>
      Bienvenue sur NXPanel, le centre de contrôle de vos services sur
      ce serveur. Le panel est encore en cours de développement actif,
      n'hésitez pas à râler s'il ne vous convient pas.
    </p>
    <h2>E-mail</h2>
    <p py:if="not emails">Vous ne possédez pas de compte e-mail!</p>
    <p py:if="emails">
      Vous avez ouvert <span py:replace="len(emails)"/> comptes emails.
    </p>
    <p py:if="not mailaliases">Vous n'avez pas créé d'alias e-mail.</p>
    <p py:if="mailaliases">Vous avez créé
      <span py:replace="len(mailaliases)"/> alias.</p>
    <p><a href="email">Gérer vos comptes e-mail</a></p>
    <h2>Hébergement</h2>
    <p>La création d'un compte web ne se fait qu'après validation
      des informations fournies. Le site doit respecter entièrement
      la charte Next-Touch.</p>
    <p><a href="webaccount">Ouvrir un compte</a></p>
  </body>
</html>
