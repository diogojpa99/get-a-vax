<%page args="v,disabled=False" />
<fieldset class="card mb-4" ${'disabled' if disabled else ''}>
  <div class="card-header">
    Dados gerais
  </div>
  <div class="card-body">
    <div>
      <div class="form-row">
        <div class="col-6 form-group">
          <label for="vaccineName" class="form-label">Nome*</label>
          <input type="text" value="${v['name']}" class="form-control" name="vaccineName" id="vaccineName" required minlength="3" maxlength="256">
        </div>
      </div>
      <div class="form-row">
        <div class="col-6 form-group">
          <label for="ersCode" class="form-label">Código ERS*</label>
          <input type="text" value="${v['ersid_vaccine']}" class="form-control" name="ersCode" id="ersCode" required minlength="3" maxlength="36">
        </div>
      </div>
  </div>
</fieldset>
<fieldset class="card mb-4" ${'disabled' if disabled else ''}>
  <div class="card-header">
    Regras
  </div>
  <div class="card-body" ${'disabled' if disabled else ''}>
    <div class="form-row">
      <div class="col-6 form-group">
        <label for="ageMin" class="form-label">Idade Minima</label>
        <div class="input-group">
          <select class="col-2 custom-select" name="ageMinUnit">
% for (val,l) in [("0", "-"),("m","Meses"),("y", "Anos")]:
<option ${'selected' if v['agemin_unit'] == val else ''} value="${val}">${l}</option>
% endfor
          </select>
          <input type="number" class="col form-control" name="ageMin" id="ageMin" value="${v['agemin_value'] if v['agemin_value'] != -1 else ''}" required min="1">
        </div>
      </div>
    </div>
    <div class="form-row">
      <div class="col-6 form-group">
        <label for="ageMax" class="form-label">Idade Máxima</label>
        <div class="input-group">
          <select class="col-2 custom-select" name="ageMaxUnit">
% for (val,l) in [("0", "-"),("m","Meses"),("y", "Anos")]:
            <option ${'selected' if v['agemax_unit'] == val else ''} value="${val}">${l}</option>
% endfor
          </select>
          <input type="number" class="col form-control" name="ageMax" id="ageMax" value="${v['agemax_value'] if v['agemax_value'] != -1 else ''}" required min="1">
        </div>
      </div>
    </div>
  ${selectBoosterInterval("boosterVal", "Periodicidade", v['unit'], v['value'], True)}
  ${selectBoosterInterval("boosterVal1", "Reforço 1",  v['unit1'], v['value1'], True)}
  ${selectBoosterInterval("boosterVal2", "Reforço 2",  v['unit2'], v['value2'], True)}
  ${selectBoosterInterval("boosterVal3", "Reforço 3",  v['unit3'], v['value3'], True)}
  ${selectBoosterInterval("boosterVal4", "Reforço 4",  v['unit4'], v['value4'], True)}
  ${selectBoosterInterval("boosterVal5", "Reforço 5",  v['unit5'], v['value5'], True)}
  ${selectBoosterInterval("boosterVal6", "Reforço 6",  v['unit6'], v['value6'], True)}
  ${selectBoosterInterval("boosterVal7", "Reforço 7",  v['unit7'], v['value7'], True)}
  ${selectBoosterInterval("boosterVal8", "Reforço 8",  v['unit8'], v['value8'], True)}
  ${selectBoosterInterval("boosterVal9", "Reforço 9",  v['unit9'], v['value9'], True)}
  </div>
</fieldset>

<%def name="selectBoosterInterval(name, label, unit, value, visible)">\
    <div class="form-row" ${'' if visible else 'hidden'}>
      <div class="col-6 form-group">
        <label for="${name}" class="form-label">${label}</label>
        <div class="input-group">
          <select class="col-2 custom-select" name="${name}Unit">
% for (u,l) in [("0", "-"),("d", "Dias"), ("m","Meses"),("y", "Anos")]:
            <option ${'selected' if unit == u else ''} value="${u}">${l}</option>
% endfor
          </select>
          <input type="number" class="col form-control" name="${name}" id="${name}" value="${value if value != -1 else ''}" required min="1">
        </div>
      </div>
    </div>\
</%def>


## vi: set ft=html : 
