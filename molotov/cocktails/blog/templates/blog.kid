<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>
  <body>
    <div py:for="b in billets" class="blog_billet">
      <h1><a href="${mltv.url ('billet', billet=b.id)}"
	     py:content="b.title">Billet title</a></h1>
      <p class="blog_billet_info">
	Posté le
	<span py:content="b.creation_date.strftime ('%A %d %B %Y à %Hh%M')"
	      class="datetime">Billet datetime</span>
	par
	<span class="user" py:if="b.user is None">Anonyme</span>
	<span class="user" py:if="not b.user is None"
	      py:content="b.user.display_name">Utilisateur</span>
	<a href="${mltv.url ('billet', billet=b.id) + '#comments'}">
	  <span class="comments"
		py:if="len (b.comments) == 1">1 commentaire</span>
	  <span class="comments"
		py:if="len (b.comments) != 1"
		py:content="'%d commentaires' % len (b.comments)">#n</span>
	</a>
      </p>
      <div py:replace="XML (rst2html (b.data))">Billet text goes here.</div>
      <ul class="toolbar"
	  py:if="(b.user and (b.user.name == mltv_user)) or 'wiki_admin' in mltv_groups">
	<li><a class="edit" href="${mltv.url ('modify', billet=b.id)}">Modifier le billet</a></li>
      </ul>
    </div>
    <p><a href="new_billet">Poster un billet</a></p>
  </body>
</html>
