// Global scope
  window.totalAmount = 0
  window.totalGains = 0


// Change to multi bet
function change_to_multi(){
  //Multiple bet check
  multibtt = document.getElementById("multibtt")
  multibtt.setAttribute("data-checked","true")
  multibtt.style.color = "#000"
  multibtt.style.fontFamily = "MarlinGeoBold"

  //Simple bet uncheck
  simplebtt = document.getElementById("simplebtt")
  simplebtt.setAttribute("data-checked","false")
  simplebtt.style.color = "#9aa1af"
  simplebtt.style.fontFamily = "MarlinGeoMedium"
}

// Change to simple bet
function change_to_simple(){
  //Simple bet checked
  simplebtt = document.getElementById("simplebtt")
  simplebtt.setAttribute("data-checked","true")
  simplebtt.style.color = "#000"
  simplebtt.style.fontFamily = "MarlinGeoBold"

  //Multiple bet uncheck
  multibtt = document.getElementById("multibtt")
  multibtt.setAttribute("data-checked","false")
  multibtt.style.color = "#9aa1af"
  multibtt.style.fontFamily = "MarlinGeoMedium"
}

function check_amount(elem){
  if(elem.value<0.10 && elem.value!="" && elem.value>0){
      elem.parentElement.outerHTML += "<div>A aposta mínima é 0.10€</div>"
  }else if(elem.value>500){
      elem.parentElement.outerHTML += "<div>A aposta máxima é 500€</div>"
  }
}

function remove_amount_warning(elem){

  if(elem.parentElement.nextSibling){
    elem.parentElement.nextSibling.remove()
  }

}

// Update multiple possible gains
function update_gains(elem,odd){
  if(elem.value!="" && elem.value>=0.10 && elem.value<=500){
    amount = parseFloat(elem.value)
    sessionStorage.setItem("amount",String(amount))
    gains = amount*odd
    $("#valorGanhos span").text(String(gains.toFixed(2)) + "€")
    $('.buttonApostar').prop('disabled', false);
  }else{
    $('.buttonApostar').prop('disabled', true);
    $("#valorGanhos span").text('0.00€')
    sessionStorage.setItem("amount","0")

  }
}

function update_simple_gains(){

      betboxesInputs = document.getElementsByClassName("betboxMontanteInput");
      gains = 0
      for(var i=0;i<betboxesInputs.length;i++){
        value = betboxesInputs[i].value
        betbox = betboxesInputs[i].parentNode.parentNode.parentNode
        if(value!=null){
          gains += value * parseFloat(betbox.getAttribute("data-odd"))
        }

      if(gains==0){
        $("#valorGanhos span").text("0,00€")
      }else{
        $("#valorGanhos span").text(String(gains.toFixed(2)) + "€")
      }
    }
}

function update_simple_amount(elem,amount){
  // get the div with the game id
  game_div = $(elem).parent().parent().parent()
  console.log(game_div)
  game_id = game_div.attr("id")
  odd_type = game_div.attr("data-oddType")

  game_data = sessionStorage.getItem(game_id)
  game_data_obj = JSON.parse(game_data)

  for(var i=0;i<game_data_obj.length;i++){
        if(game_data_obj[i].bet_outcome==odd_type){
            game_data_obj[i].amount = amount
        }
  }
  sessionStorage.setItem(game_id,JSON.stringify(game_data_obj))
}



function simpleAmount_handler(elem){

    var rowCimaValor = document.getElementById('rowCimaValor')

    slip_counter = $("#slipform").attr("data-counter")

    if(elem.value!="" && elem.value>=0.10 && elem.value<=500){
      value = parseFloat(elem.value)
      if(elem.oldvalue==""){
        window.totalAmount += value
      }else{
        oldvalue = parseFloat(elem.oldvalue)

        window.totalAmount -= oldvalue
        window.totalAmount += value
      }
      update_simple_amount(elem,value)
      $("#rowCimaValor span").text(String(window.totalAmount.toFixed(2)))
    }else{
      oldvalue = parseFloat(elem.oldvalue)
      if(elem.oldvalue!=""){
        window.totalAmount -= oldvalue
      }
      update_simple_amount(elem,"0")

      if(elem.value<0.10 || elem.value >500){
        $("#rowCimaValor span").text("0,00€")
        $("#valorGanhos span").text("0,00€")
      }else{
          $("#rowCimaValor span").text(String(window.totalAmount.toFixed(2)))
      }

  }
}

// Change every game in storage has simple (prev betType was multiple)
function storage_change_simple(){
  sessionStorage.clear();
  // Set bet type
  sessionStorage.setItem("betType","simple")

  betboxes = document.getElementsByClassName("betbox");

  for(var i=0;i<betboxes.length;i++){
    game_id = betboxes[i].getAttribute("id")
    odd_type = betboxes[i].getAttribute("data-oddtype")
    stored_value = sessionStorage.getItem(game_id)
    if(stored_value!=null){
      data_obj = JSON.parse(stored_value)
      new_store_value = {"bet_outcome" : odd_type, "amount" : 0}
      data_obj.push(new_store_value)
      sessionStorage.setItem(game_id,JSON.stringify(data_obj))
    }else{
      data_obj = [{"bet_outcome" : odd_type, "amount" : 0}]
      sessionStorage.setItem(game_id,JSON.stringify(data_obj));

    }
  }
}

// Change every game in storage has multiple
function storage_change_multiple(){
  sessionStorage.clear();
  // Set bet type
  sessionStorage.setItem("betType","multiple")

  betboxes = document.getElementsByClassName("betbox");

  for(var i=0;i<betboxes.length;i++){
    game_id = betboxes[i].getAttribute("id")
    odd_type = betboxes[i].getAttribute("data-oddtype")
    new_store_value = [{"bet_outcome" : odd_type}]
    sessionStorage.setItem(game_id,JSON.stringify(new_store_value))
  }

  sessionStorage.setItem("amount","0")


}

function slip_handler(bttChange){

  slipform = document.getElementById("slipform")
  counter = parseFloat(slipform.getAttribute("data-counter"))
  sameGcounter = parseFloat(slipform.getAttribute("data-sameGcounter"))
  prev_bettype = slipform.getAttribute("data-bettype")

  var betboxs = document.getElementsByClassName('betbox');
  total_odd = 1
  for(var i=0;i<betboxs.length;i++){
    total_odd *= parseFloat(betboxs[i].getAttribute("data-odd"))
  }

  // Simple
  if(sameGcounter>=1 || counter<=1 || bttChange=="simple"){

    change_to_simple()
    slipform.setAttribute("data-bettype","simple")
    sessionStorage.setItem("betType","simple")

    // disable bet button
    //$('.buttonApostar').prop('disabled', true);

    $(".betboxFooter").remove()
    $(".betboxHeader").after('<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Montante" type="tel" step="0.01" onfocus="this.oldvalue = this.value;remove_amount_warning(this)" oninput="update_simple_gains();simpleAmount_handler(this);this.oldvalue = this.value;check_amount(this);"><span class="betboxMontanteEuro">€</span></div></div>')

    // Simple bets needs to have a odds less then 1.20
    var betboxs = document.getElementsByClassName('betbox');
    for(var i=0;i<betboxs.length;i++){
        odd = parseFloat(betboxs[i].getAttribute("data-odd"))
        if(odd < 1.20){
          betboxs[i].children[1].innerHTML = "<p style='color:red'> Cota"+odd+"</p><p>A cota para esta selecção simples deve ser igual, ou superior, a 1,20</p>"
        }

    }

    $("#rowCimaNome span").text('Montante Total')
    $("#rowCimaValor span").text('0,00€')

    $("#rowBaixoNome span").text('Ganhos Possíveis')
    $("#valorGanhos span").text('0,00€')

    storage_change_simple()

  // Multiple
  }else if(counter>1 || bttChange=="multiple"){

    // Multiple bets max 10 slections
    if(counter<=10){
      change_to_multi()
      slipform.setAttribute("data-bettype","multiple")
      sessionStorage.setItem("betType","multiple")
      window.totalAmount = 0

      // enable bet button
      //$('.buttonApostar').prop('disabled', true);

      $(".betboxFooter").remove()


      $("#rowCimaNome span").text('Cota '+total_odd.toFixed(2))
      $("#rowCimaValor span").html('<div class="montante"><input class="montanteInput" type="number" placeholder="Montante" type="tel" step="0.01" onfocus="remove_amount_warning(this)"  oninput="update_gains(this,'+total_odd+');check_amount(this);"><span class="betboxMontanteEuro">€</span></div></div>')

      var betboxs = document.getElementsByClassName('betbox');
      for(var i=0;i<betboxs.length;i++){
          odd = parseFloat(betboxs[i].getAttribute("data-odd"))
          if(odd < 1.10){
            $("#rowCimaNome span").text("Esta aposta múltipla não é permitida, as cotas dos jogos tem de ser, pelo menos, 1,10")
            $("#rowCimaValor span").html('')
            // disable bet button
            $('.buttonApostar').prop('disabled', true);
          }

      }

      $("#rowBaixoNome span").text('Ganhos Possíveis')
      $("#valorGanhos span").text('0,00€')

      storage_change_multiple()
    }else{
      alert("Só podem ser feitas 10 seleções na modalidade múltipla");
      // disable bet button
      $('.buttonApostar').prop('disabled', true);
    }


    }
}

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
        sameGcounter = parseFloat(slipform.getAttribute("data-sameGcounter"))
        sameGcounter++;
        slipform.setAttribute("data-sameGcounter",String(sameGcounter))
    }

    // Get data atributes from tag
    let slip = document.querySelector('.slip');
    var home = elem.getAttribute("data-home")
    var away = elem.getAttribute("data-away")
    var bet = elem.getAttribute("data-bet")
    var odd = elem.getAttribute("data-odd")


    if(bet==home){
      odd_type = "home"
    }else if(bet==away){
      odd_type = "away"
    }else{
      odd_type = "draw"

    }
    $('#slipbodyMsg').remove()
    //Add game to slip in the html
    slip.innerHTML += '<div class="betbox" id='+elem.name+' data-odd='+odd+' data-oddType='+odd_type+'><div class="betboxHeader"><label>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet + '<br>Cota '+odd+' </div></label></div>';

    // Increase total games counter in the form
    slipform = document.getElementById("slipform")
    counter = parseFloat(slipform.getAttribute("data-counter"))
    counter++

    slipform.setAttribute("data-counter",String(counter))
    slip_handler("nobtt")
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
      counter = parseFloat(slipform.getAttribute("data-counter"))
      counter--;
      slipform.setAttribute("data-counter",String(counter))

      if(counter==0){
        let slip = document.querySelector('.slip');
        slip.innerHTML += "<div id='slipbodyMsg'>Adiciona a tua primeira aposta!</div>"
      }

      // Decrease same game counter
      game_on_slip = document.getElementById(elem.name)
      if(game_on_slip != null && typeof(game_on_slip) != 'undefined'){
          sameGcounter = parseFloat(slipform.getAttribute("data-sameGcounter"))
          sameGcounter--;
          slipform.setAttribute("data-sameGcounter",String(sameGcounter))

      }
      slip_handler("nobtt")
    }
  }
}
