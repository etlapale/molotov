<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <div class="blog_billet">
      <h1><a href="${mltv.url ('billet', billet=billet.id)}"
	     py:content="billet.title">Billet title</a></h1>
      <p class="blog_billet_info">
	Posté le
	<span py:content="billet.creation_date.strftime ('%A %d %B %Y à %Hh%M')"
	      class="datetime">Billet datetime</span>
	par
	<span class="user" py:if="billet.user is None">Anonyme</span>
	<span class="user" py:if="not billet.user is None"
	      py:content="billet.user.display_name">Utilisateur</span>
	<a href="#comments">
	  <span class="comments" py:content="len (billet.comments)">#n</span>
	  commentaires
	</a>
      </p>
      <div py:replace="XML (mltv.format_rst (billet.data)['html_body'])">Billet text goes here.</div>
    </div>
      
    <h2><a name="comments">Commentaires</a></h2>
    <div class="comment" py:for="c in billet.comments">
      <div class="text" py:content="XML (mltv.format_rst (c.data)['html_body'])">Comment text</div>
      <div class="info">
	Par
	<span class="user" py:if="c.user is None">Anonyme</span>
	<span class="user" py:if="not c.user is None"
	      py:content="c.user.display_name">User</span>
	le
	<span py:content="c.creation_date.strftime ('%A %d %B %Y à %Hh%M')"
	      class="datetime">Comment datetime</span>
      </div>
      <ul class="toolbar"
	  py:if="(c.user and (c.user.name == mltv_user)) or 'blog_admin' in mltv_groups">
	<li py:if="'blog_admin' in mltv_groups"><a class="delete" href="${mltv.url('delete_comment', comment=c.id)}">Supprimmer</a></li>
      </ul>
    </div>
    
    <h3>Ajouter un commentaire</h3>
    <form method="post" action="do_new_comment">
      <input type="hidden" name="billet" value="${billet.id}"/>
      <label>Utilisateur</label>
      <input type="text" disabled="disabled" py:if="not mltv_user is None" value="${mltv_user}"/>
      <p py:if="mltv_user is None">Vous n'êtes pas identifié.</p>
      <label>Texte</label>
      <textarea name="data" cols="50" rows="15"/>
      <input type="submit" value="poster"/>
    </form>
    
    <p><a href="new_billet">Poster un billet</a></p>
  </body>
</html>

