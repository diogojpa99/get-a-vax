<div class="text-center">
  <h1 class="h4 text-gray-900 mb-4">Bem vindo</h1>
</div>
<form class="user" method="post" action="${request.current_route_path()}" autocomplete="off">
  <div class="form-group">
    <input class="form-control form-control-user" name="ersid"
        id="exampleInputEmail" aria-describedby="emailHelp"
        placeholder="Número de Utente" required>
  </div>
  <div class="form-group">
    <input type="date" class="form-control form-control-user"
      name="born_at" required
          id="exampleInputPassword" placeholder="data de nascimento">
  </div>
  <button class="btn btn-primary btn-user btn-block">
      Login
  </button>
</form>
<hr>
<div class="text-center">
    <a class="small" href="/admin/login">É colaborador?</a>
</div>

