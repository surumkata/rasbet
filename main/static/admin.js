// Admin button to save game state changes
function button_game_state(elem){
  //quando carregou no botao cancelar retorna a pagina aos valores originais (reload)
  if (elem.value.localeCompare('Cancelar') == 0){
    window.location.replace('/')
  }else if (elem.value.localeCompare('Gravar') == 0){
    console.log('Guardando')
    var games = document.getElementsByClassName('change_state')

    //buscar valor da query do url
    const params = new Proxy(new URLSearchParams(window.location.search), {
      get: (searchParams, prop) => searchParams.get(prop),
    })
    var sport = params.sport
    var url = '/game/change_games_state'
    url = url + '?sport=' + sport

    for(var i=0; i<games.length; i++){
      let state_select = games[i]
      try {
        if(state_select.getAttribute('original-value').localeCompare(state_select.value)!=0){
          url = url + "&"+state_select.getAttribute('game-id')+"="+state_select.value
        }
      }
      catch{

      }
    }
    window.location.href = url
  }
}