<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'tickets.kid'">

  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>

  <body>
    <form action="do_new" method="post">
      <label>Titre (bref résumé)</label>
      <input type="text" name="title" value="${title}" size="30"/>
      <label>Raporteur</label>
      <input disabled="disabled" type="text" value="${mltv_user}"/>
      <label>Type</label>
      <select name="type">
	<span py:for="t in types">
	  <option py:if="type != t" value="${t}" py:content="types[t]"/>
	  <option py:if="type == t" value="${t}" py:content="types[t]" selected="true"/>
	</span>
      </select>
      <label>Priorité</label>
      <select name="priority">
	<span py:for="p in priorities">
	  <option py:if="priority != p" value="${p}" py:content="priorities[p]"/>
	  <option py:if="priority == p" value="${p}" py:content="priorities[p]" selected="true"/>
	</span>
      </select>
      <label>Affectée à (optionel)</label>
      <input type="text" name="owner" value="${owner}" size="30"/>
      <label>Commentaire (description détaillée)</label>
      <textarea name="comment" cols="60" rows="10"
		py:content="comment"></textarea>
      <input type="submit" value="Créer"/>
    </form>
  </body>
</html>
