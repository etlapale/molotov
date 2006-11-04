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
    <!-- Path to the directory -->
    <p class="repo_path">
      <a class="root" href="${mltv.url ('/', revision=revision)}">Root</a> /
      <span py:for="(dir,dirp) in parents">
	<a href="${mltv.url ('/', directory=dirp, revision=revision)}"
	   py:content="dir">parent</a> /
      </span>
    </p>
    
    <!-- Switch to another revision -->

    <!-- Directory content -->
    <table class="repo_file">
      <tr>
	<th>Line</th><th>&nbsp;</th>
      </tr>
      <?python ln = 0 ?>
      <tr py:for="line in lines">
	<td class="line_number" py:content="ln">#ln</td>
	<td class="line_data odd"
	    py:content="line" py:if="ln % 2 == 0">Line data</td>
	<td class="line_data even"
	    py:content="line" py:if="ln % 2 == 1">Line data</td>
	<?python ln += 1 ?>
      </tr>
    </table>
  </body>
</html>
