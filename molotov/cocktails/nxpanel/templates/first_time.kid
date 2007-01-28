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
      L'utilisation du NXPanel requiert la validation de la charte des
      services disponible sur le wiki. Nous vous demandons de plus un
      certain nombre d'informations personnelles. En aucun cas nous ne
      les utiliserons à des fins commerciales ou malicieuse, elles sont
      destinées à la légalité des services. Ces informations ne sont
      destinées qu'à l'administrateur du serveur et ne seront, hors cas
      de décision de Justice, fournies à une tierce personne.
      Toute information fausse ou incomplète entrainera la suspension
      du compte.
    </p>
    <form action="do_first_time" method="post">
      <label>Vos noms et prénoms réels</label>
      <input type="text" name="name" size="20" value="${name}"/>
      <label>Votre addresse (rue, ville, ...)</label>
      <textarea rows="3" cols="20" name="address" py:content="address"/>
      <label>Adresse email personnelle</label>
      <input type="text" name="email" size="20" value="${email}"/>
      <br/>
      <label>Captcha : recopiez le texte de l'image</label>
      <br/>
      <img alt="Captcha" src="${captcha_src}"/>
      <br/>
      <input type="text" name="captcha_answer" size="10"/>
      <input type="checkbox" name="chart">
	J'ai lu et j'accepte la Charte du serveur.
      </input>
      <input type="hidden" name="captcha_id" value="${captcha_id}"/>
      <br/>
      <input type="submit" value="OK"/>
    </form>
  </body>
</html>
