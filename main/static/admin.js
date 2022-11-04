// Admin button to save game state changes
function button_game_state(elem){
  //quando carregou no botao cancelar retorna a pagina aos valores originais (reload)
  if (elem.value.localeCompare('Cancelar') == 0){
    window.location.replace('/')
  }else if (elem.value.localeCompare('Gravar') == 0){
    console.log('Guardando')
    var games = document.getElementsByClassName('change_state')
    var games_state = []
    for(var i=0; i<games.length; i++){
      let state_select = games[i]
      games_state.push([state_select.value,state_select.getAttribute('game-id')])
    }
    games_state.forEach(k => console.log(k))
  }
}