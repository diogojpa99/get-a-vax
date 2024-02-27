<%inherit file="../page/base.mako"/>
<section class="row">
  <div class="col-8">
    <div class="card shadow mb-4">
      <div class="card-header">
        Vacinas por agendar
      </div>
      <div class="card-body">
<%
  request.environ['db'].execute("""SELECT v.*,vse.* FROM
    vaccine_user_schedule_event vse
    INNER JOIN vaccine v ON v.id_vaccine = vse.id_vaccine
    LEFT JOIN vaccine_user_schedule_event_scheduled vsed ON vse.id_vaccine_user_schedule_event = vsed.id_vaccine_user_schedule_event
    WHERE vse.id_user_ers = %s AND vsed.id_vaccine_user_schedule_event IS NULL
    ORDER BY vse.reference_date""", (request.authenticated_userid,))
  rows = request.environ['db'].fetchall()
%>
% if rows:
        <ul class="list-group">
%   for r in rows:
          <li class="list-group-item d-flex w-100 justify-content-between">
            <h4>${r['name']}</h4>
              <a href="${request.route_url('customer.schedule', id_vse=r['id_vaccine_user_schedule_event'])}"
                  class="btn btn-primary" href="">Agendar</a>
          </li>
%   endfor
        </ul>
% else:
        Não existem Vacinas por agendar
% endif
      </div>
    </div>
  </div>
  <div class="col-4">
    <div class="card shadow mb-4">
      <div class="card-header">
        Agendamentos
      </div>
      <div class="card-body">
<%
  request.environ['db'].execute("""SELECT vsed.* FROM
    vaccine_user_schedule_event vse
    INNER JOIN vaccine_user_schedule_event_scheduled vsed ON vse.id_vaccine_user_schedule_event = vsed.id_vaccine_user_schedule_event
    LEFT JOIN vaccine_user_schedule_event_log vsel ON vse.id_vaccine_user_schedule_event = vsel.id_vaccine_user_schedule_event
    WHERE vse.id_user_ers = %s AND vsel.id_vaccine_user_schedule_event IS NULL
    ORDER BY vse.reference_date""", (request.authenticated_userid, ))
  rows = request.environ['db'].fetchall()
%>
% if rows:
        <ul class="list-group">
%   for r in rows:
          <li class="list-group-item ${borderof(r['s_at_date'])|trim}"
              data-bs-toggle="tooltip" title="${tooltip_message(r['s_at_date'])|h}">
            <h4>${r['s_at_date']}&nbsp;${r['s_at_time']}</h4>
            <p>${r['s_what']}</p>
            <p class="">${r['s_where']}</p>
          </li>
%   endfor
        </ul>
% else:
  Não existem ajendamentos
% endif
      </div>
    </div>
  </div>
</section>
<section class="row">
  <div class="col">
    <div class="card shadow mb-4">
      <div class="card-header">
        Histórico
      </div>
      <div class="card-body">
<%
  request.environ['db'].execute("""SELECT v.name as vname,vse.*,vsel.*,c.* FROM
    vaccine_user_schedule_event vse
    INNER JOIN vaccine_user_schedule_event_scheduled vsed ON vse.id_vaccine_user_schedule_event = vsed.id_vaccine_user_schedule_event
    INNER JOIN vaccine_user_schedule_event_log vsel ON vse.id_vaccine_user_schedule_event = vsel.id_vaccine_user_schedule_event
    INNER JOIN vaccine v ON v.id_vaccine = vse.id_vaccine
    LEFT JOIN clinic c ON c.id_clinic = vsed.id_clinic
    WHERE vse.id_user_ers = %s
    ORDER BY vsel.vaccine_shot_date DESC""", (request.authenticated_userid,))
  rows = request.environ['db'].fetchall()
%>
% if rows:
        <ul class="list-group">
%   for r in rows:
          <li class="list-group-item">
            <span class="h4">${r['vaccine_shot_date']}</span>, ${r['name']} &dash; ${r['name_group']}, ${r['vname']}
            <p class="">${r['vaccine_batch_number']}</p>
          </li>
%   endfor
        </ul>
% else:
        Não existem vacinas por agendar
% endif
      </div>
    </div>
  </div>
</section>
<%def name="borderof(x)"><%
  import datetime
  diff = (x - today).days
%>\
% if diff <= 3:
border-left-danger\
% elif diff <= 5:
border-left-warning\
% else:
border-left-info\
% endif
</%def>
<%def name="tooltip_message(x)">\
<%
  import datetime
  diff = (x - today).days
%>\
Faltam ${diff} dias\
</%def>

<%block name="pagescripts">
  let tooltips = document.querySelectorAll('[data-bs-toggle=tooltip]')
  tooltips.forEach(el => new window.bootstrap.Tooltip(el, {
    placement: 'left',
  }))
</%block>
