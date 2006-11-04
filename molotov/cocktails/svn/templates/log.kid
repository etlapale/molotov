<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'../../../templates/master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Molotov - Repository</title>
  </head>
  <body>
    <p class="submenu">
      <a href="${mltv.url ('/')}">Repository Tree</a>
    </p>
    
    <table class="svn_repo">
      <tr><th>Rev</th><th>Date</th><th>Auteur</th><th>Log</th></tr>
      <tr py:for="(rev,date,author,log) in revisions">
	<td><a href="${mltv.url ('/', revision = rev)}"
	       py:content="rev">num</a></td>
	<td py:content="date.strftime ('%c')">date</td>
	<td py:content="author">author</td>
	<td class="log" py:content="log">log message</td>
      </tr>
    </table>
  </body>
</html>
