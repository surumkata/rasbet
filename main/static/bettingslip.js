// Handles button check/uncheck logic, add game to slip and update counter in the form
function button_handler(elem){
  checked = elem.getAttribute("data-checked")
  if(checked == "false"){
    // Button check
    elem.setAttribute("data-checked","true")
    elem.style.background = "#af7537"
    elem.style.color = "#ffdf7b"

    // Increase same game counter in the form
    game_on_slip = document.getElementById(elem.name)
    if(game_on_slip != null && typeof(game_on_slip) != 'undefined'){
        sameGcounter = parseInt(slipform.getAttribute("data-sameGcounter"))
        sameGcounter++;
        slipform.setAttribute("data-sameGcounter",String(sameGcounter))
    }

    // Get data atributes from tag
    let slip = document.querySelector('.slip');
    var home = elem.getAttribute("data-home")
    var away = elem.getAttribute("data-away")
    var bet = elem.getAttribute("data-bet")
    //Add game to slip in the html
    slip.outerHTML = '<div id='+elem.name+'><input type="hidden" name='+ elem.name + '>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet +'</input> <br><br></div>' + slip.outerHTML;

    // Increase total games counter in the form
    slipform = document.getElementById("slipform")
    counter = parseInt(slipform.getAttribute("data-counter"))
    counter++
    slipform.setAttribute("data-counter",String(counter))

  }else{
    // Button uncheck
    elem.setAttribute("data-checked","false")
    elem.style.background = "#ffdf7b"
    elem.style.color = "#af7537"

    // Remove game from slip
    game_on_slip = document.getElementById(elem.name)
    if(game_on_slip != null && typeof(game_on_slip) != 'undefined'){
      console.log("AQUI")
      game_on_slip.remove()

      //Decrase counter in the form
      slipform = document.getElementById("slipform")
      counter = parseInt(slipform.getAttribute("data-counter"))
      counter--;
      slipform.setAttribute("data-counter",String(counter))

      // Decrease same game counter
      game_on_slip = document.getElementById(elem.name)
      if(game_on_slip != null && typeof(game_on_slip) != 'undefined'){
          sameGcounter = parseInt(slipform.getAttribute("data-sameGcounter"))
          sameGcounter--;
          slipform.setAttribute("data-sameGcounter",String(sameGcounter))
      }

    }
  }
}

// Change to simple bet
function change_to_simple(){
  //Simple bet checked
  simplebtt = document.getElementById("simplebtt")
  simplebtt.setAttribute("data-checked","true")
  simplebtt.style.background = "#ffaa80"

  //Multiple bet uncheck
  multibtt = document.getElementById("multibtt")
  multibtt.setAttribute("data-checked","false")
  multibtt.style.background = "white"
}

// Change to multi bet
function change_to_multi(){
  //Multiple bet check
  multibtt = document.getElementById("multibtt")
  multibtt.setAttribute("data-checked","true")
  multibtt.style.background = "#ffaa80"

  //Simple bet uncheck
  simplebtt = document.getElementById("simplebtt")
  simplebtt.setAttribute("data-checked","false")
  simplebtt.style.background = "white"
}

function slip_handler(elem){
  slipform = document.getElementById("slipform")
  counter = parseInt(slipform.getAttribute("data-counter"))
  sameGcounter = parseInt(slipform.getAttribute("data-sameGcounter"))

  if(sameGcounter>=1 || counter<=1){
      change_to_simple()
  }else if(counter>1){
      change_to_multi()
  }

}
