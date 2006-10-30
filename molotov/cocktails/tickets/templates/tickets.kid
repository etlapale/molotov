<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  
  <head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'"
	py:attrs="item.items()">
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Molotov - Tickets</title>
    <meta py:replace="item[:]"/>
  </head>

  <body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'"
	py:attrs="item.items()">

    <!-- Tickets toolbox -->
    <div class="toolbox">
      <strong>Tickets</strong>
      <ul>
	<li><a href="${mltv.url ('/')}">Tous les tickets</a></li>
	<li><a href="${mltv.url ('/new')}">Nouveau ticket</a></li>
      </ul>
    </div>

    <!-- Main page content -->
    <div py:replace="[item.text]+item[:]"/>
  </body>
</html>
