<%inherit file="../page/base.mako"/>

<!-- DataTales Example -->
<div class="card shadow mb-4">
  <div class="card-header py-3">
    <h6 class="m-0 font-weight-bold text-primary">${title}</h6>
  </div>
  <div class="card-body">
    <div class="table-responsive">
      <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
        <thead>
          <tr>
            <th>Data/hora</th>
            <th>Clínica</th>
            <th>Nº Utente</th>
            <th>Vacina</th>
          </tr>
        </thead>
        <tfoot>
          <tr>
            <th>Data/hora</th>
            <th>Clínica</th>
            <th>Nº Utente</th>
            <th>Vacina</th>
          </tr>
          <tr>
            <td colspan="4" style="text-align:center">
              <div class="btn-group" role="group" aria-label="Basic example">
                <form>
                  <input type="hidden" name="offset" value="${prev_offset}">
                  <button ${'disabled' if prev_offset is None else ''} class="btn btn-secondary">Anteriores</button>
                </form>

                <form>
                  <input type="hidden" name="offset" value="${next_offset}">
                  <button ${'disabled' if next_offset is None else ''} class="btn btn-secondary">Próximos</button>
                </form>
              </div>
            </td>
          </tr>
        </tfoot>
        <tbody>
%if records:
%  for v in records:
          <tr>
            <td style="width:25%">${v['s_at_date']}&nbsp;${v['s_at_time']}</td>
            <td>${v['s_where']}</td>
            <td>${v['ersid_user']}</td>
            <td>${v['s_what']}</td>
          </tr>
%  endfor
%endif
        </tbody>
      </table>
    </div>
  </div>
</div>

