// Global scope
  window.totalAmount = 0
  window.totalGains = 0
  window.games_on_slip = []
  window.game_counter = 0
  window.same_game_counter = 0
  window.bet_type = "simple"


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
      $('#buttonApostar').attr("disabled", true);
      elem.parentElement.outerHTML += "<div>The minimun bet is 0.10€</div>"
  }else if(elem.value>500){
      $('#buttonApostar').attr("disabled", true);
      elem.parentElement.outerHTML += "<div>The maximum bet is 500€</div>"
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
      emptyInput = false
      for(var i=0;i<betboxesInputs.length;i++){
        console.log(betboxesInputs[i].value)
        value = betboxesInputs[i].value
        betbox = betboxesInputs[i].parentNode.parentNode.parentNode
        if(value!=null && value!=""){
          gains += value * parseFloat(betbox.getAttribute("data-odd"))
        }else{
            emptyInput = true
        }

      if(gains==0){
          $('.buttonApostar').attr("disabled", true);
          $("#valorGanhos span").text("0,00€")
      }else{
        $('.buttonApostar').attr("disabled", false);
        $("#valorGanhos span").text(String(gains.toFixed(2)) + "€")
      }
    }
    console.log(emptyInput)
    if(emptyInput){
      $('.buttonApostar').attr("disabled", true);

    }
}

function update_simple_amount(elem,amount){
  // get the div with the game id
  game_div = $(elem).parent().parent().parent()
  slip_game_id = game_div.attr("id")
  odd_type = game_div.attr("data-oddType")
  //slip;game_id;betType => game_id
  slip_game_id_fields = slip_game_id.split(";");
  game_id = slip_game_id_fields[1]

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
  order_array = []
  for(var i=0;i<betboxes.length;i++){
    slip_id = betboxes[i].getAttribute("id")
    slip_id_fields = slip_id.split(";")
    game_id = slip_id_fields[1]

    odd_type = betboxes[i].getAttribute("data-oddtype")
    home = betboxes[i].getAttribute("data-home")
    away = betboxes[i].getAttribute("data-away")
    bet = betboxes[i].getAttribute("data-bet")
    odd = betboxes[i].getAttribute("data-odd")
    stored_value = sessionStorage.getItem(game_id)
    if(stored_value!=null){
      data_obj = JSON.parse(stored_value)
      new_store_value = {"home":home,"away":away,"bet":bet,"odd":odd,"bet_outcome" : odd_type, "amount" : 0}
      data_obj.push(new_store_value)
      sessionStorage.setItem(game_id,JSON.stringify(data_obj))
    }else{
      data_obj = [{"home":home,"away":away,"bet":bet,"odd":odd,"bet_outcome" : odd_type, "amount" : 0}]
      sessionStorage.setItem(game_id,JSON.stringify(data_obj));

    }
    order_array.push([game_id,odd_type])
  }
  sessionStorage.setItem("order",JSON.stringify(order_array))
}

// Change every game in storage has multiple
function storage_change_multiple(){
  sessionStorage.clear();
  // Set bet type
  sessionStorage.setItem("betType","multiple")

  betboxes = document.getElementsByClassName("betbox");
  order_array = []
  for(var i=0;i<betboxes.length;i++){
    slip_id = betboxes[i].getAttribute("id")
    slip_id_fields = slip_id.split(";")
    game_id = slip_id_fields[1]

    odd_type = betboxes[i].getAttribute("data-oddtype")
    home = betboxes[i].getAttribute("data-home")
    away = betboxes[i].getAttribute("data-away")
    bet = betboxes[i].getAttribute("data-bet")
    odd = betboxes[i].getAttribute("data-odd")
    new_store_value = [{"home":home,"away":away,"bet":bet,"odd":odd,"bet_outcome" : odd_type}]
    sessionStorage.setItem(game_id,JSON.stringify(new_store_value))
    order_array.push(game_id)
  }

  sessionStorage.setItem("order",JSON.stringify(order_array))

  sessionStorage.setItem("amount","0")


}


function slip_handler(bttchange,home,away,bet,odd){


  var betboxs = document.getElementsByClassName('betbox');
  total_odd = 1
  for(var i=0;i<betboxs.length;i++){
    total_odd *= parseFloat(betboxs[i].getAttribute("data-odd"))
  }

  // Simple
  if(window.same_game_counter>=1 || window.game_counter<=1 || bttchange=="simple"){

    change_to_simple()
    window.bet_type = "simple"
    sessionStorage.setItem("betType","simple")

    // disable bet button
    //$('.buttonApostar').prop('disabled', true);

    $(".betboxFooter").remove()
    $(".betboxHeader").after('<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Amount" type="tel" step="0.01" onfocus="this.oldvalue = this.value;remove_amount_warning(this)" oninput="check_amount(this);update_simple_gains();simpleAmount_handler(this);this.oldvalue = this.value;"><span class="betboxMontanteEuro">€</span></div></div>')

    // Simple bets needs to have a odds less then 1.20
    var betboxs = document.getElementsByClassName('betbox');
    for(var i=0;i<betboxs.length;i++){
        odd = parseFloat(betboxs[i].getAttribute("data-odd"))
        if(odd < 1.20){
          betboxs[i].children[1].innerHTML = "<p style='color:red'> Odd"+odd+"</p><p>The odds for the simple bets must be equal to or greater than 1.20</p>"
        }

    }

    $("#rowCimaNome span").text('Total Amount')
    $("#rowCimaValor span").text('0,00€')

    $("#rowBaixoNome span").text('Total Earnings')
    $("#valorGanhos span").text('0,00€')

    storage_change_simple(home,away,bet,odd)

  // Multiple
}else if(window.game_counter>1 || bttchange=="multiple" ){

    // Multiple bets max 20 slections
    if(window.game_counter<=20){
      change_to_multi()
      window.bet_type = "multiple"
      sessionStorage.setItem("betType","multiple")
      window.totalAmount = 0

      // enable bet button
      //$('.buttonApostar').prop('disabled', true);

      $(".betboxFooter").remove()


      $("#rowCimaNome span").text('Odd '+total_odd.toFixed(2))
      $("#rowCimaValor span").html('<div class="montante"><input class="montanteInput" type="number" placeholder="Amount" type="tel" step="0.01" onfocus="remove_amount_warning(this)"  oninput="check_amount(this);update_gains(this,'+total_odd+');"><span class="betboxMontanteEuro">€</span></div></div>')

      var betboxs = document.getElementsByClassName('betbox');
      for(var i=0;i<betboxs.length;i++){
          odd = parseFloat(betboxs[i].getAttribute("data-odd"))
          if(odd < 1.10){
            $("#rowCimaNome span").text("This multiple bet is not allowed, game odds must be at least 1.10")
            $("#rowCimaValor span").html('')
            // disable bet button
            $('.buttonApostar').prop('disabled', true);
          }

      }

      $("#rowBaixoNome span").text('Total Earnings')
      $("#valorGanhos span").text('0,00€')

    storage_change_multiple(home,away,bet,odd)
    }else{
      // disable bet button
      $("#rowCimaNome span").text("This multiple bet is not allowed, only 20 games for multiple bet")
      $("#rowCimaValor span").html('')
      $('.buttonApostar').prop('disabled', true);
    }


    }
}

// Handles button check/uncheck logic, add game to slip and update counter in the form
function button_handler(elem){
  checked = elem.getAttribute("data-checked")
  odd_id = elem.id.split(";")
  game_id = odd_id[0]

  if(checked == "false"){
    // Button check
    elem.setAttribute("data-checked","true")
    elem.style.background = "#af7537"
    elem.style.color = "#ffdf7b"

    // Increase same game counter in the form

    if(window.games_on_slip.includes(game_id)){
        window.same_game_counter++
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

    // If values have whitespaces  need to be a string
    str_home = "\""+home+"\""
    str_away = "\""+away+"\""
    str_bet = "\""+bet+"\""


    slip_id = "slip;"+elem.id

    str_slip_id = "\'"+slip_id+"\'"

    //Add game to slip in the html

    slip.innerHTML += '<div class="betbox" id='+slip_id+' data-odd='+odd+' data-oddType='+odd_type+' data-home='+str_home+' data-away='+str_away+' data-bet='+str_bet+' ><div class="betboxHeader"><button onclick="delete_selection('+str_slip_id+');" ><span>&times;</span></button><label>' + home + '-' + away + '<br>Result: ' + bet + '<br>Odd '+odd+' </div></label></div>';

    window.games_on_slip.push(game_id)
    window.game_counter++

    slip_handler("nobtt",home,away,bet,odd)
  }else{
    // Button uncheck
    elem.setAttribute("data-checked","false")
    elem.style.background = "#ffdf7b"
    elem.style.color = "#af7537"

    slip_id = "slip;"+elem.id
    game_on_slip = document.getElementById(slip_id)
    if(game_on_slip != null && typeof(game_on_slip) != 'undefined'){
      game_on_slip.remove()


      order_array = JSON.parse(sessionStorage.getItem("order"))
      index = order_array.indexOf(game_id);
      order_array.splice(index, 1);
      sessionStorage.setItem("order",JSON.stringify(order_array))


      index = window.games_on_slip.indexOf(game_id);
      window.games_on_slip.splice(index, 1);
      window.game_counter--

      if(window.game_counter==0){
        let slip = document.querySelector('.slip');
        slip.innerHTML += '<div class="betbox-msg" id="slipbodyMsg">Add your first bet!</div>'
      }

      // Decrease same game counter
      if(window.games_on_slip.includes(game_id)){
          window.same_game_counter--
        }

      slip_handler("nobtt")
    }
  }
}

function delete_selection(slip_game_id){
  //slip;gameId;betType
  slip_game_id_fields = slip_game_id.split(";")

  elem = document.getElementById(slip_game_id);
  elem.remove()

  window.game_counter--

  if(window.bet_type=="simple"){
    // Decrease same game counter
    for(var i=0;i<window.games_on_slip.length;i++){
        if(slip_game_id_fields[1]==window.games_on_slip[i]){
          index = window.games_on_slip.indexOf(slip_game_id_fields[1]);
          window.games_on_slip.splice(index, 1);
          window.same_game_counter--
          break

        }
    }
  }

  // Uncheck button if there is one

  btt_id = slip_game_id_fields[1] + ";" + slip_game_id_fields[2]
  btt_elem = document.getElementById(btt_id)
  // If the game is showed in the page then click th odd
  if(btt_elem){
    btt_elem.setAttribute("data-checked","false")
    btt_elem.style.background = "#ffdf7b"
    btt_elem.style.color = "#af7537"

  }
  slip_handler("nobtt")
}

// Onload build slip as saved in localStorage
window.onload = (event) =>{

    type = sessionStorage.getItem("betType");
    if(type){



      let slip = document.querySelector('.slip');

      order_array = JSON.parse(sessionStorage.getItem("order"))

      counter = 0

      if(type=="simple"){
        sameGameCounter = 0
          //update
          for(var i=0;i<order_array.length;i++){
              game_data_obj = JSON.parse(sessionStorage.getItem(order_array[i][0]))
              for(var j=0;j<game_data_obj.length;j++){
                if(game_data_obj[j].bet_outcome==order_array[i][1]){

                    if(window.games_on_slip.includes(order_array[i][0])){
                        sameGameCounter++
                    }
                    window.games_on_slip.push(order_array[i][0])

                    btt_id =  order_array[i][0] + ";" + game_data_obj[j].bet_outcome
                    btt_elem = document.getElementById(btt_id)
                    // If the game is showed in the page then click th odd
                    if(btt_elem){
                        btt_elem.setAttribute("data-checked","true")
                        btt_elem.style.background = "#af7537"
                        btt_elem.style.color = "#ffdf7b"
                      }
                    slip_id = "slip;"+btt_id
                    str_slip_id = "\'"+slip_id+"\'"
                    slip.innerHTML += '<div class="betbox" id='+slip_id+' data-odd='+game_data_obj[j].odd+' data-oddType='+game_data_obj[j].bet_outcome+' data-home='+game_data_obj[j].home+' data-away='+game_data_obj[j].away+' data-bet='+game_data_obj[j].bet+' ><div class="betboxHeader"><button onclick="delete_selection('+str_slip_id+');" ><span>&times;</span></button><label>'+game_data_obj[j].home+"-"+game_data_obj[j].away+'<br>Result: ' + game_data_obj[j].bet + '<br>Odd '+game_data_obj[j].odd+' </div></label></div>';

                    counter++

                  }

                }
              }

          window.game_counter = counter
          window.same_game_counter = sameGameCounter

          window.bet_type = "simple"
          change_to_simple()

          $(".betboxFooter").remove()
          $(".betboxHeader").after('<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Amount" type="tel" step="0.01" onfocus="this.oldvalue = this.value;remove_amount_warning(this)" oninput="check_amount(this);update_simple_gains();simpleAmount_handler(this);this.oldvalue = this.value;"><span class="betboxMontanteEuro">€</span></div></div>')

          $("#rowCimaNome span").text('Total Amount')
          $("#rowCimaValor span").text('0,00€')

          $("#rowBaixoNome span").text('Total Earnings')
          $("#valorGanhos span").text('0,00€')
      }else{

        for(var i=0;i<order_array.length;i++){
              game_data_obj = JSON.parse(sessionStorage.getItem(order_array[i]))
              btt_id =  order_array[i] + ";" + game_data_obj[0].bet_outcome
              btt_elem = document.getElementById(btt_id)
              // If the game is showed in the page then click th odd
              if(btt_elem){
                btt_elem.setAttribute("data-checked","true")
                btt_elem.style.background = "#af7537"
                btt_elem.style.color = "#ffdf7b"
              }
              // Build slip id
              slip_id = "slip;"+btt_id
              str_slip_id = "\'"+slip_id+"\'"
              let slip = document.querySelector('.slip');
              slip.innerHTML += '<div class="betbox" id='+slip_id+' data-odd='+game_data_obj[0].odd+' data-oddType='+game_data_obj[0].bet_outcome+' data-home='+game_data_obj[0].home+' data-away='+game_data_obj[0].away+' data-bet='+game_data_obj[0].bet+' ><div class="betboxHeader"><button onclick="delete_selection('+str_slip_id+');" ><span>&times;</span></button><label>'+game_data_obj[0].home+"-"+game_data_obj[0].away+'<br>Result: ' + game_data_obj[0].bet + '<br>Odd '+game_data_obj[0].odd+' </div></label></div>';
              counter++


        }

        window.game_counter = counter
        window.same_game_counter = 0

        var betboxs = document.getElementsByClassName('betbox');
        total_odd = 1
        for(var i=0;i<betboxs.length;i++){
          total_odd *= parseFloat(betboxs[i].getAttribute("data-odd"))
        }

        window.bet_type = "multiple"
        change_to_multi()
        $(".betboxFooter").remove()


        $("#rowCimaNome span").text('Odd '+total_odd.toFixed(2))
        $("#rowCimaValor span").html('<div class="montante"><input class="montanteInput" type="number" placeholder="Amount" type="tel" step="0.01" onfocus="remove_amount_warning(this)"  oninput="check_amount(this);update_gains(this,'+total_odd+');"><span class="betboxMontanteEuro">€</span></div></div>')

        $("#rowBaixoNome span").text('Total Earnings')
        $("#valorGanhos span").text('0,00€')
      }
      if(window.game_counter>0){
        $('#slipbodyMsg').remove()
      }
    }else{
      sessionStorage.setItem("order",JSON.stringify([]))
    }
}
