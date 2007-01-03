<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
  <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'"
	py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"
	  py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
    <link rel="stylesheet" type="text/css" href="/static/css/molotov.css"/>
  </head>
  
  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'"
	py:attrs="item.items()">
    <div id="body">
      
      <div id="head">
	<div id="headtitle" py:content="molotov_title">Website Title</div>
	<ul id="cocktails" py:if="len (molotov_cocktails) > 1">
	  <li py:for="(cocktail, name, url) in molotov_cocktails" py:if="cocktail != 'user'">
	    <a href="${url}" py:content="name">CocktailName</a>
	  </li>
	</ul>
      </div>
      
      <div id="userbox" py:if="mltv.has_user_cocktail ()">
	<div py:if="molotov_user is None">
	  <form action="${mltv.cocktail_prefix ('user') + '/login'}" method="post">
	    <input type="hidden" name="from_url" value="/"/>
	    <input type="text" size="6" name="username"/>
	    <input type="password" size="6" name="password"/>
	    <input type="submit" value="Identification"/>
	  </form>
	  <a href="${mltv.cocktail_prefix ('user') + '/register'}">Inscription</a>
	</div>
	<div py:if="molotov_user != None">
	  <p>
	    Connecté en tant que <strong py:content="molotov_user"
					 class="username">username</strong>
	  </p>
	  <a py:if="'molotov_admin' in molotov_groups"
	     href="/user/admin">Administration</a>
	  <a href="/user/logout">Déconnexion</a>
	</div>
      </div>
      
      <div id="main">
	
	<!-- Flash message -->
	<div class="flash"
	     py:if="mltv.has_flash ()"
	     py:content="mltv.get_flash ()">
	  Flash message!
	</div>

	<!-- Main page content -->
	<div py:replace="[item.text]+item[:]"/>

	<!-- Footer -->
	<hr class="spacer"/>
	<div id="footer">
	  Copyright &copy; 2002-2007 The Next-Touch Organization<br/>
          Ce site utilise :
          <ul class="uselist">
            <li><a href="http://molotov.next-touch.com/">Molotov</a></li>
            <li><a href="http://www.cherrypy.org/">CherryPy</a></li>
            <li><a href="http://www.icon-king.com/">Nuvola</a></li>
          </ul>
	</div>
      </div>
    </div>
  </body>
</html>
