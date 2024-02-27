
const __selectA = ['ageMin', 'ageMax']
const __selectB = [ 'boosterVal', 'boosterVal1',
  'boosterVal2', 'boosterVal3', 'boosterVal4', 'boosterVal5',
  'boosterVal6', 'boosterVal7', 'boosterVal8', 'boosterVal9',
]

function FormContentsInit(form) {
  function setDisabled(elValue, elSelectUnit) {
    const opt = elSelectUnit.selectedOptions
    const is_disabled = opt.length === 0 || opt[0].value === "0"
    elValue.disabled = is_disabled
    return
  }
  form.addEventListener('submit', function(event) {
    if (form.checkValidity() === false) {
      event.preventDefault()
      event.stopPropagation()
    }
    form.classList.add('was-validated')
    return
  }, false)

  for (let elName of [ ...__selectA, ...__selectB ]) {
    const elValue = form[elName]
    const elSelectUnit = form[elName+'Unit']
    if ( !elValue || ! elSelectUnit ) {
      continue
    }
    // setSelectUnitBehavior
    setDisabled(elValue, elSelectUnit)
    elSelectUnit.addEventListener('input', ev => setDisabled(elValue, ev.target))
  }
  return
}

## vi: set ft=javascript : 
