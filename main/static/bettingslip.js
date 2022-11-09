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

function update_gains(elem,odd){
  gainslb = document.getElementById("valorGanhos")
  if(elem.value!=""){
    amount = parseFloat(elem.value)
    sessionStorage.setItem("amount",String(amount))
    gains = amount*odd
    gainslb.innerHTML = String(gains.toFixed(2)) + "€"
  }else{
    gainslb.innerHTML = '0.00€'
    sessionStorage.setItem("amount","0")

  }
}


function update_simple_amount(elem,amount){
  // get the div with the game id
  game_div = $(elem).parent().parent()
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

    if(elem.value!=""){
      value = parseInt(elem.value)
      if(elem.oldvalue==""){
        window.totalAmount += value
      }else{
        oldvalue = parseInt(elem.oldvalue)

        window.totalAmount -= oldvalue
        window.totalAmount += value
      }
      update_simple_amount(elem,value)
    }else{
      oldvalue = parseInt(elem.oldvalue)
      if(elem.oldvalue!=""){
        window.totalAmount -= oldvalue
      }
      update_simple_amount(elem,"0")
    }

    if (window.totalAmount==0){
        rowCimaValor.innerHTML = '0,00€'
    }else{
        rowCimaValor.innerHTML = String(window.totalAmount) + "€"

    }
}

// Session store simple bet
function store_simple(game_id,odd_type){
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

// Session store simple bet when prev betType is multi. Convert multi fields to simple fields
function store_multiTosimple(game_id,odd_type){
  sessionStorage.removeItem("amount");

  keys = Object.keys(sessionStorage)
  for(var i=0;i<keys.length;i++){
      if(keys[i]=="betType"){
          //pass
      }else{
        game_data = sessionStorage.getItem(keys[i])
        game_data_obj = JSON.parse(game_data)
        new_store_value = [{"bet_outcome" : game_data_obj[0].bet_outcome, "amount" : 0}]
        sessionStorage.setItem(keys[i],JSON.stringify(new_store_value))
      }
  }

  store_simple(game_id,odd_type)
}

// Session store multi bet
function store_multi(game_id,odd_type){
  new_store_value = [{"bet_outcome" : odd_type}]
  sessionStorage.setItem(game_id,JSON.stringify(new_store_value))
}

// Session store multi bet. Convert simple fields to multi fields
function store_simpleTomulti(game_id,odd_type){
  keys = Object.keys(sessionStorage)
  for(var i=0;i<keys.length;i++){
      if(keys[i]=="betType"){
          //pass
      }else{
        game_data = sessionStorage.getItem(keys[i])
        game_data_obj = JSON.parse(game_data)
        store_multi(keys[i],game_data_obj[0].bet_outcome)
      }
  }
  store_multi(game_id,odd_type)
  sessionStorage.setItem("amount","0")
}

// store_onDelete_simple
function store_onDeleteTo_simple(game_id){
  sessionStorage.removeItem("amount");
  sessionStorage.removeItem(game_id);

  keys = Object.keys(sessionStorage)
  for(var i=0;i<keys.length;i++){
      if(keys[i]=="betType"){
          //pass
      }else{
        game_data= sessionStorage.getItem(keys[i])
        game_data_obj = JSON.parse(game_data)
        new_store_value = [{"bet_outcome" : game_data_obj[0].bet_outcome, "amount" : 0}]
        sessionStorage.setItem(keys[i],JSON.stringify(new_store_value))

      }
  }
}

// store_onDelete_multi
function store_onDeleteTo_multi(game_id,odd_type){
  same_game_data = sessionStorage.getItem(keys[i])
  same_game_data_obj = JSON.parse(game_data)
  for(var i=0;i<same_game_data_obj.lenght;i++){
        if(same_game_data_obj[i]==odd_type){
          //remove from array
          same_game_data_obj.splice(index, i)
        }
  }

  keys = Object.keys(sessionStorage)
  for(var i=0;i<keys.length;i++){
      if(keys[i]=="betType"){
          //pass
      }else{
        game_data = sessionStorage.getItem(keys[i])
        game_data_obj = JSON.parse(game_data)
        store_multi(keys[i],game_data_obj[0].bet_outcome)

      }
  }
  sessionStorage.setItem("amount","0")

}

function slip_handler(elem,isremove){
  slipform = document.getElementById("slipform")
  counter = parseInt(slipform.getAttribute("data-counter"))
  sameGcounter = parseInt(slipform.getAttribute("data-sameGcounter"))
  prev_bettype = slipform.getAttribute("data-bettype")

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

  if(sameGcounter>=1 || counter<=1){

      change_to_simple()
      slipform.setAttribute("data-bettype","simple")
      sessionStorage.setItem("betType","simple")
      // Get all elements with id = betbox
      var betboxs = document.getElementsByClassName('betbox');

      if(!isremove){
      // If last state is simple just add at the end
      if(prev_bettype=="simple"){
        store_simple(elem.name,odd_type)
        // Iterate throw all betbox
        for(var i=0;i<betboxs.length;i++){
            // Get children elements in betbox
            var children = betboxs[i].children;

            if(i==counter-1){ // Only add to the end
            // Iterate throw children elements
            for(var j=0; j<children.length; j++){
                // Only add after
                if(j==1){
                    var child = children[j];
                    child.outerHTML += '<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Montante" onfocus="this.oldvalue = this.value;" oninput="simpleAmount_handler(this);this.oldvalue = this.value;"><span class="betboxMontanteEuro">€</span></div></div>'
                }
            }
          }
        }
      }else{ // if last state is multi add to all bet boxes
          store_multiTosimple(elem.name,odd_type)
          for(var i=0;i<betboxs.length;i++){
              // Get children elements in betbox
              var children = betboxs[i].children;
              // Iterate throw children elements
              for(var j=0; j<children.length; j++){
                  // Only add after
                  if(j==1){
                      var child = children[j];
                      child.outerHTML += '<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Montante" onfocus="this.oldvalue = this.value;" oninput="simpleAmount_handler(this);this.oldvalue = this.value;"><span class="betboxMontanteEuro">€</span></div></div>'
                  }
              }
          }
        }
        var rowCimaNome = document.getElementById('rowCimaNome')
        rowCimaNome.innerHTML = "Montante Total"

        var rowCimaValor = document.getElementById('rowCimaValor')
        rowCimaValor.innerHTML = '0,00€'

      }else{
        // If its a remove operation and prev state is multiple => change footer and ad simple input
          if(prev_bettype=="multiple"){
            store_onDeleteTo_simple(elem.name)

            for(var i=0;i<betboxs.length;i++){
                // Get children elements in betbox
                var children = betboxs[i].children;
                // Iterate throw children elements
                for(var j=0; j<children.length; j++){
                    // Only add after
                    if(j==1){
                        var child = children[j];
                        child.outerHTML += '<div class="betboxFooter"><div class="betboxMontante"><input class="betboxMontanteInput" type="number" placeholder="Montante" onfocus="this.oldvalue = this.value;" oninput="simpleAmount_handler(this);this.oldvalue = this.value;"><span class="betboxMontanteEuro">€</span></div></div>'
                    }
                }
            }

            var rowCimaNome = document.getElementById('rowCimaNome')
            rowCimaNome.innerHTML = "Montante Total"

            var rowCimaValor = document.getElementById('rowCimaValor')
            rowCimaValor.innerHTML = '0,00€'

          }else{
              sessionStorage.removeItem(elem.name);
          }
      }
}else if(counter>1){
      total_odd = 1
      change_to_multi()
      slipform.setAttribute("data-bettype","multiple")
      sessionStorage.setItem("betType","multiple")
      window.totalAmount = 0

      var betboxs = document.getElementsByClassName('betbox');
      if(!isremove){
        if(prev_bettype=="multiple"){ // If last state is multiple just add to the end
          store_multi(elem.name,odd_type)

          for(var i=0;i<betboxs.length;i++){
            total_odd = total_odd * parseFloat(betboxs[i].getAttribute("data-odd"))
            var children = betboxs[i].children;
            if(i==counter){
              for(var j=0; j<children.length; j++){
                  var child = children[j];
                  if(j==1){
                      child.outerHTML = '<label>'+odd+'</label>'
                  }
                }
              }
            }
        }else{ // If last state is simple clear all input
          store_simpleTomulti(elem.name,odd_type)
          for(var i=0;i<betboxs.length;i++){
            total_odd = total_odd * parseFloat(betboxs[i].getAttribute("data-odd"))
            var children = betboxs[i].children;
            if(i==0){
              var child = children[2]
              child.outerHTML=""
            }else if(i==counter){
              for(var j=0; j<children.length; j++){
                  var child = children[j];
                  if(j==1){
                    child.outerHTML = '<label>'+odd+'</label>'
                  }
                }
              }
            }
          }
    }else{

        if(prev_bettype=="simple"){// If its a remove operation and prev state is simple => change footer and remove simple input
          store_onDeleteTo_multi(elem.name)
          for(var i=0;i<betboxs.length;i++){
            total_odd = total_odd * parseFloat(betboxs[i].getAttribute("data-odd"))
            var children = betboxs[i].children;
            for(var j=0; j<children.length; j++){
                  var child = children[j];
                  if(j==2){
                      child.outerHTML = ""
                  }
              }
          }
        }else{
            sessionStorage.removeItem(elem.name,odd_type);

            for(var i=0;i<betboxs.length;i++){
              total_odd = total_odd * parseFloat(betboxs[i].getAttribute("data-odd"))
            }


        }
      }
      var rowCimaNome = document.getElementById('rowCimaNome')
      rowCimaNome.innerHTML = "Cota " + total_odd.toFixed(2)

      var rowCimaValor = document.getElementById('rowCimaValor')
      rowCimaValor.innerHTML = '<div class="montante"><input class="montanteInput" type="number" placeholder="Montante" oninput="update_gains(this,'+total_odd.toFixed(2)+')"><span class="montanteEuro">€</span></div>'
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


    if(bet==home){
      odd_type = "home"
    }else if(bet==away){
      odd_type = "away"
    }else{
      odd_type = "draw"

    }



    //Add game to slip in the html
    slip.innerHTML += '<div class="betbox" id='+elem.name+' data-odd='+odd+' data-oddType='+odd_type+'><div class="betboxHeader"><label>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet + '<br>Cota '+odd+' </div></label><input type="hidden" name='+ elem.name + '> </input></div>';

    // Increase total games counter in the form
    slipform = document.getElementById("slipform")
    counter = parseInt(slipform.getAttribute("data-counter"))
    counter++

    slipform.setAttribute("data-counter",String(counter))
    slip_handler(elem,false)
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
      slip_handler(elem,true)
    }
  }
}
