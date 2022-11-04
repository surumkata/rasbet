//Specialist button to save games odds
function button_change_odd(elem){
  //quando carregou no botao cancelar retorna a pagina aos valores originais (reload)
  if (elem.value.localeCompare('Cancelar') == 0){
    window.location.replace('/')
  }else if (elem.value.localeCompare('Gravar') == 0){
    console.log('Guardando')
    var odds = document.getElementsByClassName('odd_input')

    //buscar valor da query do url
    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    })
    var sport = params.sport
    var url = '/game/change_games_odds'
    url = url + '?sport=' + sport

    for(var i=0; i<odds.length; i++){
      let odd_input = odds[i]
      try {
        if(odd_input.getAttribute('original-value').localeCompare(odd_input.value)){
          let odd_query = odd_input.getAttribute('game_id')+';'+odd_input.getAttribute('data-type')
          let value = odd_input.value
          if(!value){
            value = '0'
          }
          url = url + "&"+odd_query+"="+value
        }
      }
      catch{

      }
    }
    window.location.href = url
  }
}