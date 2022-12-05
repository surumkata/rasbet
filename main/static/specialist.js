//Specialist button to save games odds
function save(elem){
  //quando carregou no botao cancelar retorna a pagina aos valores originais (reload)
  if (elem.value.localeCompare('Cancel') == 0){
    window.location.replace('/')
  }else if (elem.value.localeCompare('Save') == 0){
    var games = document.getElementsByClassName('odds')
    gamesDict = {}
    

    for(var i=0; i<games.length; i++){
      let game = games[i]
      let game_id = game.getAttribute("id")
      gameDict = {}
      try{
        if(game.getAttribute('original-value').localeCompare(game.getAttribute('value')) != 0){
          gameDict['state'] = game.getAttribute('value')
        }
        for(var j = 0; j < game.children.length -1; j++){
          odd_input = game.children[j].children[0]
          if(odd_input.getAttribute('original-value').localeCompare(odd_input.value) != 0){
            gameDict[odd_input.getAttribute('data-type')] = odd_input.value
          }
        }
        if(Object.keys(gameDict).length > 0){
          gamesDict[game_id] = gameDict
        }
      }
      catch{}
    }

    $.ajax({
      type: 'POST',
      url: '/game/specialist_update_games/',
      dataType: "json",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
      },
      data: JSON.stringify({games : gamesDict})
    })
    
    $(document).ajaxStop(function(){
      window.location.reload();
    });
    
  }
}

function change_state_to_open(elem){
  game_id = elem.getAttribute("game_id")
  game = document.getElementById(game_id)
  game.setAttribute("value","open")
}