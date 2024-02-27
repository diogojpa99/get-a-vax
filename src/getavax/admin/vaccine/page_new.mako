<%inherit file="../page/base.mako"/>

<%
  v = {
    'id_vaccine': "",
    'name': "",
    'ersid_vaccine': "",
    'agemin_value': -1,
    'agemin_unit': '0',
    'agemax_value': -1,
    'agemax_unit': '0',
    'value': -1,
    'unit': '0',
    'value1': -1,
    'unit1': '0',
    'value2': -1,
    'unit2': '0',
    'value3': -1,
    'unit3': '0',
    'value4': -1,
    'unit4': '0',
    'value5': -1,
    'unit5': '0',
    'value6': -1,
    'unit6': '0',
    'value7': -1,
    'unit7': '0',
    'value8': -1,
    'unit8': '0',
    'value9': -1,
    'unit9': '0',
  }
%>


<form method="post" action="/admin/vaccines" novalidate  autocomplete="off">
  <%include file="form_contents.mako" args="v=v"/>
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


