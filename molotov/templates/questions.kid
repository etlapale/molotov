<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
      py:extends="'master.kid'">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"
	  py:replace="''"/>
    <title>Molotov::Questions</title>
  </head>
  <body>
    <h1 py:content="qtitle"/>
    <p py:content="qtext"/>
    <form action="do_questions" method="post">
      <input type="hidden" name="qid" value="${qid}"/>
      <div py:for="(label, itype, name, content) in inputs">
	<label py:if="label" py:content="label"/>
	<input py:if="itype != 'textarea'" type="${itype}" name="${name}"
	       py:content="content"/>
	<textarea py:if="itype == 'textarea'" name="${name}"/>
      </div>
      <input py:for="sub in submits" type="submit" name="submit"
	     value="${sub}"/>
    </form>
  </body>
</html>
