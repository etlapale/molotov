<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
  <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'"
	py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"
	  py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
    <link rel="stylesheet" type="text/css" href="/static/css/next.css"/>
  </head>
  
  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'"
	py:attrs="item.items()">
    <div id="body">
      
      <div id="head">
	<div id="headtitle" py:content="molotov_title">Website Title</div>
	<ul id="cocktails" py:if="len (molotov_cocktails) > 1">
	  <li py:for="(cocktail, url) in molotov_cocktails" py:if="url != '/user'">
	    <a href="${url}" py:content="cocktail">CocktailName</a>
	  </li>
	</ul>
      </div>
      
      <div id="userbox" py:if="('Controller', '/user') in molotov_cocktails">
	<div py:if="molotov_user is None">
	  <form action="/user/login" method="post">
	    <input type="hidden" name="from_url" value="/"/>
	    <input type="text" size="6" name="username"/>
	    <input type="password" size="6" name="password"/>
	    <input type="submit" value="Identification"/>
	  </form>
	  <a href="/user/register">Inscription</a>
	</div>
	<div py:if="molotov_user != None">
	  <p>
	    Connecté en tant que <strong py:content="molotov_user"
					 class="username">username</strong>
	  </p>
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
	  Copyright &copy; 2002-2006 The Next-Touch Organization<br/>
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
