<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'tickets.kid'">

  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>

  <body>
    <p>Il y a <strong py:content="len (tickets)">n</strong> tickets
      sur le cocktail.</p>
    <table>
      <tr>
	<th>ID</th>
	<th>Titre</th>
	<th>Rapporteur</th>
	<th>Modification</th>
	<th>Création</th>
	<th>Affecté à</th>
	<th>Type</th>
	<th>Priorité</th>
	<th>Statut</th>
      </tr>
      <tr py:for="t in tickets">
	<td><a href="${mltv.url ('/ticket', ticket=t.id)}" py:content="'#%s' % t.id">#id</a></td>
	<td><a href="${mltv.url ('/ticket', ticket=t.id)}" py:content="t.title">Titre</a></td>
	<td py:content="t.reporter.name">Rapporteur</td>
	<td py:content="t.change_date">Dernier changement</td>
	<td py:content="t.creation_date">Création</td>
	<td py:if="t.owner is None">(Personne)</td>
	<td py:if="t.owner != None" py:content="t.owner.name">username</td>
	<td py:content="t.ticket_type">t.ticket_type</td>
	<td py:content="t.ticket_priority">t.ticket_priority</td>
	<td py:content="t.status">t.status</td>
      </tr>
    </table>
  </body>
</html>
