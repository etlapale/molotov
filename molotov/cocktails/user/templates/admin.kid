<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  
  <head>
    <title>Molotov::Administration</title>
  </head>

  <body>
    <h1>Administration</h1>
    <h2>Groupes</h2>
    <p>
      Légende : <img alt="Remove" src="/static/images/cancel-16x16.png"/>
      Enlève un utilisateur du groupe
    </p>
    <div py:for="g in groups" class="mltv_group_info">
      <h3 py:content="g.name">GroupName</h3>
      <p>
	<strong py:if="len (g.users)">Vous ne pouvez pas supprimmer
	  un groupe non vide</strong>
	<a href="${mltv.url ('delete_group', group=g.name)}"
	   py:if="len (g.users) == 0">Supprimmer le groupe
	  <span py:replace="g.name">GroupName</span></a>
      </p>
      <strong>Membres :</strong>
      <ul>
	<li py:for="u in g.users">
	  <a href="${mltv.url ('/remove_member', group=g.name, user=u.name)}">
	    <img alt="Remove" src="/static/images/cancel-16x16.png"/>
	  </a>
	  <span py:replace="u.name">MemberName</span>
	</li>
      </ul>
      <strong>Ajouter un membre :</strong>
      <form action="add_member" method="post">
	<input type="hidden" name="group" value="${g.name}"/>
	<input type="text" name="user" size="10"/>
	<input type="submit" value="Ajouter"/>
      </form>
    </div>
    
    <h3>Créer un nouveau groupe</h3>
    <form action="create_group" method="post">
      <input type="text" name="group" size="20"/>
      <input type="submit" value="Créer"/>
    </form>
    
    <h2>Utilisateurs</h2>
    <div py:for="u in users" class="mltv_user_info">
      <h3 py:content="u.name">GroupName</h3>
      <strong>Display name</strong>
      <form action="modify_user" method="post">
	<input type="hidden" name="user" value="${u.name}"/>
	<input type="text" name="display_name" value="${u.display_name}"/>
	<input type="submit" value="Modifier"/>
      </form>
      <strong>Groupes :</strong>
      <ul>
	<li py:for="g in u.groups" py:content="g.name">Group</li>
      </ul>
    </div>
  </body>
</html>
