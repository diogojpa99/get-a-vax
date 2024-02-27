<%inherit file="../page/base.mako"/>
<%%>
<section class="row">
  <div class="col-12">
    <div class="card shadow mb-4">
      <div class="card-header">
<%
  request.environ['db'].execute("""SELECT v.* FROM
    vaccine v
    INNER JOIN vaccine_user_schedule_event vse ON v.id_vaccine=vse.id_vaccine
    WHERE vse.id_vaccine_user_schedule_event=%s""", (id_vse,))
  r = request.environ['db'].fetchone()
%>
        <h4 class="mt-2">Agendar vacina: ${r['name']}</h4>
      </div>
      <div class="card-body">
% if step == 0:
<%
     request.environ['db'].execute("""SELECT * FROM
       clinic c
       ORDER BY name_group, name""",)
     rows = request.environ['db'].fetchall()
     import itertools
     d = itertools.groupby(rows, lambda x: x['name_group'])
%>
        <form method="POST">
          <input type="hidden" name="id_vse" value="${id_vse}">
          <input type="hidden" name="step" value="1" required/>
          <fieldset>
            <div class="row">
              <div class="col">
                <select name="clinic" class="form-control form-select-lg mb-3" required>
                  <option value="">Escolha um centro</option>
%    for group,rows in d:
                  <optgroup label="${group}">
%      for r in rows:
                    <option value="${r['id_clinic']}" ${'selected' if str(r['id_clinic'])==clinic else ''}> ${r['name']}</option>
%      endfor
                  </optgroup>
%    endfor
                </select>
              </div>
              <div class="col">
<% className = 'is-invalid' if error and 'at' in error else '' %>
                <input type="date" name="at" id="at"
                    class="form-control ${className}"
                    value="${at}" min="${scheduling_date_min}"
                    aria-describedby="at-invalid-feedback"
                    required />
                <div id="at-invalid-feedback" class="invalid-feedback">
%    if 'at' in error:
                  ${ error['at'] }
%    endif
                </div>
              </div>
            </div>
          </fieldset>
          <button class="btn btn-primary">Próximo</button>
        </form>
% else:
<%
  request.environ['db'].execute("""SELECT c.*
    FROM clinic c
    WHERE c.id_clinic=%s""", (clinic,))
  r = request.environ['db'].fetchone()
%>
        <fieldset disabled>
          <div class="form-row">
            <div class="col-6 form-group">
              <label for="cName" class="form-label">Clinica</label>
              <input type="text" value="${r['name']}" class="form-control" id="cName">
            </div>
          </div>
          <div class="form-row">
            <div class="col-6 form-group">
              <label for="at" class="form-label">Data</label>
              <input type="text" value="${at}" class="form-control" id="at">
            </div>
          </div>
        </fieldset>
%  endif
      </div>
    </div>
  </div>
</section>
% if step == 1:
<section class="row">
  <div class="col-12">
    <form method="POST">
      <input type="hidden" name="id_vse" value="${id_vse}">
      <input type="hidden" name="clinic" value="${clinic}" required/>
      <input type="hidden" name="at" value="${at}" required/>
      <input type="hidden" name="step" value="2" required/>
      <fieldset class="card shadow mb-4">
        <div class="card-header">
          <h4 class="mt-2">Disponibilidade</h4>
        </div>
        <div class="card-body">
% if error:
          <div class="alert alert-danger" role="alert">
            ${ error }
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        </div>
% endif
%   if availability:
          <table class="table table-striped">
%       for mdict in availability.values():
            <tr>
%         for isodt, hm, av in mdict.values():
              <td>
                <div class="form-check">
                <input name="timeslot" value="${isodt}" type="radio" required
                        class="form-check-input" ${'disabled' if not av else ''}>
                <label class="form-check-label">${hm}</label>
                </div>
              </td>
%         endfor
            </tr>
%       endfor
          </table>
        </div>
%   else:
      <h4>Não existe disponibilidade para o local e data indicados</h4>
%   endif
      </fieldset>
      <input name="back" type="submit" class="btn btn-secondary" value="Voltar" />
%   if availability:
      <input name="ok" type="submit" class="btn btn-primary" value="Agendar" />
%   endif
    </form>
  </div>
</section>
%  endif

