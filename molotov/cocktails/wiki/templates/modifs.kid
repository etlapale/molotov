<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'wiki.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Next-Touch Wiki - Edition</title>
  </head>
  <body>

    <h2>Historique de « <span py:replace="page.pagename">Page Name</span> »</h2>

    <form action="diff" class="modifs">
      <ul class="modifs">
      <li py:for="revision in page.revisions">
	<p>
	  <input type="radio" name="rev1" value="${revision.id}"/>
	  <input type="radio" name="rev2" value="${revision.id}"/>
	    <strong py:content="u'Révision ' + revision.rev">Rev #id</strong>
	    <span py:if="revision.comment"
		  py:replace="'(%s)' % revision.comment"/>
	    <a href="${mltv.url ('/revision', modif=revision.id)}">Voir</a>
	    <a href="${mltv.url ('/preview_revision', modif=revision.id)}">Éditer</a>
	  </p>
	  <span class="datetime"
		py:content="revision.date.strftime ('Le %A %d %B %Y à %Hh%M')"/>
	  par <a py:if="revision.user" class="user wikiname"
		 href="${mltv.url ('/user/view', user=revision.user.name)}"
		 py:content="revision.user.display_name"/>
	  <span class="user" py:if="revision.user == None" py:content="'Anonyme'"/>
	</li>
      </ul>
      <input type="submit" name="submit" value="Comparer"/>
    </form>
    
    Retourner sur <a class="wikiname" href="${mltv.url ('/%s' % page.pagename)}">
      <span py:replace="page.pagename">PageName</span></a>.
  </body>
</html>
