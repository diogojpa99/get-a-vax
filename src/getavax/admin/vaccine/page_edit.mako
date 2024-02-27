<%inherit file="../page/base.mako"/>
<%
  request.environ['db'].execute("""SELECT v.*, vra.*, vrb.*
  FROM vaccine v
    INNER JOIN vaccine_rules_age vra ON vra.id_vaccine = v.id_vaccine
    INNER JOIN vaccine_rules_booster vrb ON vrb.id_vaccine = v.id_vaccine
  WHERE v.id_vaccine=%s""", (request.matchdict['id'],))
  row = request.environ['db'].fetchone()
%>


<form method="post" novalidate  autocomplete="off">
  <%include file="form_contents.mako" args="v=row"/>
  <div class="row">
    <div class="col d-flex justify-content-end">
      <a href="/admin/vaccines" class="btn btn-lg btn-secondary">Voltar</a>
      <button type="submit" class="btn btn-lg btn-primary">Gravar</button>
    </div>
  </div>
</form>

<%block name="pagescripts">
<%include file="form_contents.js.mako" />
  document.addEventListener("DOMContentLoaded", function(event) {
    FormContentsInit(document.forms[0])
  })
</%block>
