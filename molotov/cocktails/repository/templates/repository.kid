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
      <a href="${mltv.url ('/log')}">Revision Log</a>
    </p>

    <!-- Path to the directory -->
    <p class="repo_path">
      <a class="root" href="${mltv.url ('/', revision=revision)}">Root</a> /
      <span py:for="(dir,dirp) in parents">
	<a href="${mltv.url ('/', directory=dirp, revision=revision)}"
	   py:content="dir">parent</a> /
      </span>
    </p>
    
    <!-- Switch to another revision -->
    <form class="select_revision" action="index">
      <input type="hidden" name="directory" value="${directory}"/>
      <label>View revision:</label>
      <input type="text" size="2" name="revision" value="${revision}"/>
      of <a href="${mltv.url ('/', directory=directory)}"
	    py:content="last_revision">#n</a>
      <!--<input type="submit" value="Go"/>-->
    </form>

    <!-- Directory content -->
    <table class="svn_repo">
      <tr><th>Name</th><th>Size</th><th>Rev</th><th>Date</th><th>Last Change</th></tr>
      <tr py:if="parent">
	<td colspan="5" class="parent">
	  <a href="${mltv.url ('/', directory=parent,revision=revision)}">..</a>
        </td>
      </tr>
      <tr class="dir" py:for="(name, rev, age, log) in dirs">
	<td>
	  <a class="name" py:content="name"
	     href="${mltv.url ('/', directory=directory + '/' + name,revision=revision)}">Dirname</a>
	</td>
	<td>&nbsp;</td>
	<td py:content="rev"/>
	<td class="age" py:content="age"/>
	<td class="log" py:content="log"/>
      </tr>
      <tr class="file" py:for="(name, size, rev, age, log) in files">
	<td>
	  <a class="name" py:content="name"
	     href="${mltv.url ('/view', path=directory + '/' + name,revision=revision)}">Filename</a>
	</td>
	<td py:content="size"/>
	<td py:content="rev"/>
	<td class="age" py:content="age"/>
	<td class="log" py:content="log"/>
      </tr>
    </table>
  </body>
</html>
