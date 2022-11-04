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
    var odd = elem.getAttribute("data-odd")

    console.log(home)
    console.log(away)
    console.log(bet)
    console.log(odd)

    //Add game to slip in the html
    slip.innerHTML += '<div class="betbox" id='+elem.name+' data-odd='+odd+'><label>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet + '<br>'+ odd +'</label><input type="hidden" name='+ elem.name + '> </input></div>';

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
function update_gains(elem,odd){
  gainslb = document.getElementById("gains")
  if(elem.value!=""){
    amount = parseFloat(elem.value)
    gains = amount*odd
    gainslb.innerHTML = 'Ganhos possíveis: ' + String(gains.toFixed(2))
  }else{
    gainslb.innerHTML = 'Ganhos possíveis: 0.00'
  }
}
function slip_handler(elem){
  slipform = document.getElementById("slipform")
  counter = parseInt(slipform.getAttribute("data-counter"))
  sameGcounter = parseInt(slipform.getAttribute("data-sameGcounter"))
  total_odd = 1

  // Get data atributes from tag
  let slip = document.querySelector('.slip');
  var home = elem.getAttribute("data-home")
  var away = elem.getAttribute("data-away")
  var bet = elem.getAttribute("data-bet")
  var odd = elem.getAttribute("data-odd")

  if(sameGcounter>=1 || counter<=1){
      change_to_simple()
      slipform.setAttribute("data-bettype","simple")
      // Get all elements with id = betbox
      var betboxs = document.getElementsByClassName('betbox');
      // Iterate throw all betbox
      for(var i=0;i<betboxs.length;i++){
        if(i==counter){
          // Get children elements in betbox
          var children = betboxs[i].children;
          // Iterate throw children elements
          for(var j=0; j<children.length; j++){
              // Only add after
              if(j==1){
                  var child = children[j];
                  child.outerHTML += '<br><input type="number" placeholder="Montante"> </input>'
              }

          }

        }

      }
      var slipfooter = document.getElementById('slipfooter')
      slipfooter.innerHTML = '</label><br> <input type="submit" value="Apostar"> </input>'

  }else if(counter>1){
      change_to_multi()
      slipform.setAttribute("data-bettype","multiple")

      var elements = document.getElementsByClassName('betbox');

      for(var i=0;i<elements.length;i++){
        total_odd = total_odd * parseFloat(elements[i].getAttribute("data-odd"))
        if(i==counter){
            var children = elements[i].children;
          for(var j=0; j<children.length; j++){
              var child = children[j];
              if(j==1){
                  child.outerHTML = '<label>'+odd+'</label>'
              }


          }

        }
      }
      var slipfooter = document.getElementById('slipfooter')
      slipfooter.innerHTML = '<br><label>Cota:' + String(total_odd.toFixed(2)) + '</label><input type="number" placeholder="Montante" oninput="update_gains(this,'+total_odd.toFixed(2)+')"><br><label id="gains">Ganhos possíveis:  </label> <br></input> <input type="submit" value="Apostar"> </input>'

  }
}
