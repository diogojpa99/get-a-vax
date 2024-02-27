<%inherit file="../page/base.mako"/>
<!-- Content Row -->
<div class="row">
  <div class="col-xl-4 col-md-6 mb-4">
    <div class="card border-left-primary shadow h-100 py-2">
      <div class="card-body">
        <div class="row no-gutters align-items-center">
          <div class="col mr-2">
            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
              Vagas disponíveis (próximas ${delta}h)
            </div>
            <div id="vagas" class="h5 mb-0 font-weight-bold text-gray-800">${dashboard['vagas']}</div>
          </div>
          <div class="col-auto">
            <i class="fas fa-calendar fa-2x text-gray-300"></i>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="col-xl-4 col-md-6 mb-4">
   <div class="card border-left-success shadow h-100 py-2">
     <div class="card-body">
       <div class="row no-gutters align-items-center">
         <div class="col mr-2">
           <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
             Agendamentos (30 dias)
           </div>
           <div id="agendamentos" class="h5 mb-0 font-weight-bold text-gray-800">${dashboard['agendamentos']}</div>
         </div>
         <div class="col-auto">
            <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
         </div>
       </div>
     </div>
   </div>
  </div>

  <!-- Earnings (Monthly) Card Example -->
  <div class="col-xl-4 col-md-6 mb-4">
    <div class="card border-left-info shadow h-100 py-2">
      <div class="card-body">
        <div class="row no-gutters align-items-center">
          <div class="col mr-2">
           <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
            Tasks
           </div>
           <div class="row no-gutters align-items-center">
             <div class="col-auto">
               <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">50%</div>
             </div>
             <div class="col">
              <div class="progress progress-sm mr-2">
                  <div class="progress-bar bg-info" role="progressbar"
                      style="width: 50%" aria-valuenow="50" aria-valuemin="0"
                      aria-valuemax="100"></div>
              </div>
             </div>
           </div>
          </div>
          <div class="col-auto">
              <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>


<!-- Content Row -->
<div class="row">
    <!-- Content Column -->
    <div class="col-lg-6 mb-4">

        <!-- Project Card Example -->
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Agendamentos por clínica/vacina desde ínicio do mês</h6>
            </div>
            <div class="card-body">
% for r in dashboard['top']['data']:

                <h4 class="small font-weight-bold">${r[0]} &nbsp;(${r[1]})<span
                        class="float-right">${r[2]}</span></h4>
                <div class="progress mb-4">
                    <div class="progress-bar" role="progressbar" style="width: ${r[3]}%"
                        aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
% endfor
            </div>
        </div>
    </div>
</div>

<%block name="pagescripts">
  const at = (new Date()).toISOString()
  const url = "${request.route_path('admin.dashboard.data.get')}?at=" + at + "&delta=${delta}"
  fetch(url)
    .then(x => x.json())
    .then(x => {
      const elVagas = document.querySelector('#vagas');
      const vagas = x['vagas']
      if ( elVagas && vagas ) {
        elVagas.innerHTML = vagas
      }
    })
    .catch(x => console.error(x))
</%block>

