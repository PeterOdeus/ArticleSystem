<%@ taglib prefix="vplf" uri="vplf"%>
<%@ taglib uri="http://www.opensymphony.com/sitemesh/page" prefix="page" %>

<page:applyDecorator name="onePanel">
	<page:param name="title">SpringWeb</page:param>
	<page:param name="heading">Web with SpringMVC/SiteMesh</page:param>
	<page:param name="body">
		<h1>Welcome to the crazy world of ${name} together with SpringMVC & SiteMesh.....</h1>
	</page:param>
</page:applyDecorator>