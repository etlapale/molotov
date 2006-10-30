<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'wiki.kid'">

  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
  </head>

  <body>
    <!-- Page content -->
    <div py:replace="XML(data)">Page text goes here.</div>

    <!-- Page metadata -->
    <p class="pageinfo">
      Révision <span py:content="revision.rev">#revid</span>
      <span py:content="revision.date.strftime ('%A %d %B %Y à %Hh%M')"
	    class="datetime">DateDernièreÉdition</span>
      par
      <span py:if="revision.user"
	    class="user"
	    py:content="revision.user.display_name">Utilisateur</span>
      <span py:if="not revision.user" class="user">Anonyme</span>
    </p>
  </body>
</html>
