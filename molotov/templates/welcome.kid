<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Next-Touch Wiki</title>
  </head>
  <body>
    <h2>Bienvenue !</h2>
    <p>
      Vous venez d'installer le wiki <strong>MoloTov</strong> de la Next-Touch.
      Vous pouvez dès à présent créer la
      <a href="${tg.url('/edit', pagename='FrontPage')}">page d'accueil</a>
      <img alt="Accueil" src="${tg.url ('/static/images/home-16x16.png')}" />
      en tant que point de départ de votre wiki.
      Celle-ci possède le nom
      <a class="wikiname" href="${tg.url('/FrontPage')}">FrontPage</a>
      et est affichée par défaut lors de l'accès à votre site.
    </p>
    <p>
      N'hésitez pas à consulter la documentation fournie sous forme de page
      wiki dans votre installation, en particulier la page
      <a class="wikiname"
	 href="${tg.url('/ContenuDeLAide')}">ContenuDeLAide</a>
      <img alt="Aide" src="${tg.url ('/static/images/help-16x16.png')}" />,
      ainsi que notre site web sur
      <a href="http://molotov.next-touch.com/">http://molotov.next-touch.com</a>.
    </p>
  </body>
</html>
