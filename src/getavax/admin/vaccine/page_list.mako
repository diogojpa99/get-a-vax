<%inherit file="../page/base.mako"/>
<%block name="tools">
            <a href="/admin/vaccines/new" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
              <span class="icon text-white-50">
                <i class="fas fa-plus-circle fa-sm text-white-50"></i>
              </span>
              <span class="text">Adicionar</span>
            </a>
</%block>

          <!-- DataTales Example -->
          <div class="card shadow mb-4">
              <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Vacinas</h6>
              </div>
              <div class="card-body">
                  <div class="table-responsive">
                      <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                          <thead>
                              <tr>
                                  <th>Id. interno</th>
                                  <th>Nome</th>
                                  <th>Código ERS</th>
                                  <th>Acções</th>
                              </tr>
                          </thead>
                          <tfoot>
                              <tr>
                                  <th>Id. interno</th>
                                  <th>Nome</th>
                                  <th>Código ERS</th>
                                  <th>Acções</th>
                              </tr>
                          </tfoot>
                          <tbody>
<%
  request.environ['db'].execute("SELECT * FROM vaccine ORDER BY name ASC")
  records = request.environ['db'].fetchall()
%>
% for v in records:
                              <tr>
                                  <td style="width:35%">
                                    <a
                                      href="${request.route_path('admin.vaccine.item', id=v['id_vaccine'])}">
                                        ${ v['id_vaccine'] }
                                    </a>
                                  </td>
                                  <td>${ v['name'] }</td>
                                  <td>${ v['ersid_vaccine'] }</td>
                                  <td>
                                    <a
                                      href="${request.route_path('admin.vaccine.edit', id=v['id_vaccine']) }"
                                      class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                                        Editar
                                    </a>
                                  </td>
                              </tr>
% endfor
                          </tbody>
                      </table>
                  </div>
              </div>
          </div>

