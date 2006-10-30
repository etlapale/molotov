<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'tickets.kid'">

  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>

  <body>
    <h1>Ticket <span py:replace="'#%s' % ticket.id">#id</span></h1>
    <h2 py:content="u'« %s »' % ticket.title">« Titre du ticket »</h2>

    <div class="ticket_info">
      <strong>Création :</strong> <span py:content="ticket.creation_date"/><br/>
      <strong>Modification :</strong> <span py:content="ticket.change_date"/><br/>
      <strong>Rapporteur :</strong> <span py:content="ticket.reporter.name"/><br/>
      <strong>Type :</strong> <span py:content="type"/><br/>
      <strong>Priorité :</strong> <span py:content="priority"/><br/>
      <strong>Affecté à :</strong>
      <span py:if="ticket.owner is None">(Personne)</span>
      <span py:if="ticket.owner != None" py:content="ticket.owner.name"/>
      <br/>
      <strong>Statut :</strong> <span py:content="status"/><br/>
    </div>

    <p>Il y a <strong py:content="len (ticket.comments)">n</strong>
      commentaires sur ce ticket.</p>
    
    <div py:for="comment in ticket.comments">
      <div class="comment" py:content="comment.data">
	Ceci est un commentaire.
      </div>
      <div class="comment_info">
	Par <span class="user" py:content="comment.user.name">username</span>
	le <span class="datetime" py:content="comment.creation_date">datetime</span>
      </div>
    </div>
  </body>
</html>
