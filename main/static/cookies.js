function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
let name = cname + "=";
let decodedCookie = decodeURIComponent(document.cookie);
let ca = decodedCookie.split(';');
for(let i = 0; i <ca.length; i++) {
  let c = ca[i];
  while (c.charAt(0) == ' ') {
    c = c.substring(1);
  }
  if (c.indexOf(name) == 0) {
    return c.substring(name.length, c.length);
  }
}
return "";
}

function close_no_balance_popup(){
  const popup = document.getElementById("no-balance-popup")
  popup.style.display = "none"

}
function post_slip(){
  type = sessionStorage.getItem("betType")
  sessionStorage.removeItem("betType");
  sessionStorage.removeItem("order");
  slip_data = {}
  if(type=="simple"){
    slip_data['bet_type'] = type
    slip_data['games'] = []
    keys = Object.keys(sessionStorage)
    for(var i=0;i<keys.length;i++){
      game_data_obj = JSON.parse(sessionStorage.getItem(keys[i]))
      for(var j=0;j<game_data_obj.length;j++){
          game_bet = {"game_id" : keys[i],"bet_outcome" : game_data_obj[j].bet_outcome,"amount" : game_data_obj[j].amount }
          slip_data['games'].push(game_bet)
      }
      sessionStorage.removeItem(keys[i]);
    }
    console.log(slip_data['games'])
  }else if(type=="multiple"){
    amount = sessionStorage.getItem("amount")
    sessionStorage.removeItem("amount");
    slip_data['bet_type'] = type
    slip_data['amount'] = amount
    slip_data['games'] = []
    keys = Object.keys(sessionStorage)
    for(var i=0;i<keys.length;i++){
      game_data_obj = JSON.parse(sessionStorage.getItem(keys[i]))
      game_bet = {"game_id" : keys[i],"bet_outcome" : game_data_obj[0].bet_outcome}
      sessionStorage.removeItem(keys[i]);
      slip_data['games'].push(game_bet)
    }
  }
  $.ajax({
      type: 'POST',
      url: '/gamble/bet/',
      dataType: "json",
      headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
     },
     data: JSON.stringify({slip : slip_data}),
     success: function( data, status, xhttp) {
              if(data.status==0){
                  // Bet placed
                  const popup = document.getElementById("sucess-popup")
                  // Display sucess popup
                  popup.style.display = "block"
             }else if(data.status==1){
                  // Not logged in or session expired
                  window.location.assign('/accounts/login/')
            }else if(data.status==2){
                // Not enough balance
                const popup = document.getElementById("no-balance-popup")
                // Display no balance popup
                popup.style.display = "block"
                // Not enough balance
            }
    },
})


}

function update_fav(elem){
  favorited = elem.checked
  type = elem.name.split(':')[0]
  favorite = elem.name.split(':')[1]
  console.log(favorited)
  console.log(type)
  console.log(favorite)
  $.ajax({
    type: 'POST',
    url: '/accounts/update_favorite/',
    dataType: "json",
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
   },
   data: JSON.stringify({'favorited' : favorited,'type':type,'favorite':favorite}),
   success: function( data, status, xhttp) {
            if(data.status==0){
                window.location.reload();
           }else{
                window.location.assign('/')
          }
  },
})
};


function change_language(elem){
  new_language = elem.value


  $.ajax({
    type: 'POST',
    url: '/change_language',
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
    },
    data: JSON.stringify({'language' : new_language}),
    success: window.location.reload()
  })
}

function update_follow(elem){
  followed = elem.checked
  game = elem.name
  console.log(followed)
  console.log(game)
  
  $.ajax({
    type: 'POST',
    url: '/accounts/update_follow/',
    dataType: "json",
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
   },
   data: JSON.stringify({'followed' : followed, 'game':game}),
   success: function( data, status, xhttp) {
            if(data.status==0){
                window.location.reload();
           }else{
                window.location.assign('/')
          }
  },
  
})

};