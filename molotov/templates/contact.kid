<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Next-Touch Panel - Contact</title>
  </head>
  <body>
    
    <h1>Contact</h1>

    <form action="contact" method="post">
      <input py:if="user"
	     type="hidden" name="username" value="${user.username}"/>
      <label for="name">Votre nom :</label>
      <input type="text" name="name" id="name" size="40"/>
      <label for="email">Adresse e-mail :</label>
      <input type="text" name="email" id="email" size="40"/>
      <textarea name="message" rows="10" cols="70"/>
      <input type="submit" value="Envoyer"/>
    </form>
  </body>
</html>
