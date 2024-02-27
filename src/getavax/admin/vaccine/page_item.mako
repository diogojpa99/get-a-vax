<%inherit file="../page/base.mako"/>
<%
  request.environ['db'].execute("""SELECT v.*, vra.*, vrb.*
  FROM vaccine v
    INNER JOIN vaccine_rules_age vra ON vra.id_vaccine = v.id_vaccine
    INNER JOIN vaccine_rules_booster vrb ON vrb.id_vaccine = v.id_vaccine
  WHERE v.id_vaccine=%s""", (request.matchdict['id'],))
  row = request.environ['db'].fetchone()
%>


<form>
  <%include file="form_contents.mako" args="v=row,disabled=True"/>
</form>

<%block name="pagescripts">
</%block>
