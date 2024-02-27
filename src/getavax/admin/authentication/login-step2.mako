<div class="text-center">
  <h1 class="h4 text-gray-900 mb-4">Bem vindo</h1>
  Foi-lhe enviado um código por sms
</div>
<form class="user" method="post" action="${request.current_route_path()}" autocomplete="off">
  <div class="form-group">
    <input name="code" type="text" minlength="6" maxlength="6" pattern="[0-9]{6}"
        class="form-control form-control-user"
        id="exampleInputEmail" aria-describedby="emailHelp"
        placeholder="Código">
  </div>
  <button class="btn btn-primary btn-user btn-block">
      Login
  </button>
</form>
<hr>
<div class="text-center">
  <form class="user" method="post" action="${request.current_route_path()}" autocomplete="off">
    <button class="btn btn-outline-secondary small">reenviar código</button>
  </form>
</div>

