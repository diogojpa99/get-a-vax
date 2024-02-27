<div class="text-center">
  <h1 class="h4 text-gray-900 mb-4">Bem vindo</h1>
</div>
<form class="user" method="post" action="${request.current_route_path()}" autocomplete="off">
  <div class="form-group">
    <input class="form-control form-control-user" name="email"
        id="exampleInputEmail" aria-describedby="emailHelp"
        placeholder="Email utilizador" type="email" required>
  </div>
  <div class="form-group">
    <input type="password" class="form-control form-control-user"
      name="secret" required
          id="exampleInputPassword" placeholder="Password">
  </div>
  <button class="btn btn-primary btn-user btn-block">
      Login
  </button>
</form>
<hr>

