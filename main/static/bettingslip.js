
function slip(elem){
    elem.checked = true
    console.log(elem.name);
    rm = document.getElementById(elem.name)
    if(rm != null && typeof(rm) != 'undefined'){
      rm.remove()
    }

    let slip = document.querySelector('.slip');

    // Get data atributes from tag
    var home = elem.getAttribute("data-home")
    var away = elem.getAttribute("data-away")
    var bet = elem.getAttribute("data-bet")

    //Add game to slip in the html
    slip.outerHTML = '<div id='+elem.name+'><input type="hidden" name='+ elem.name + '>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet +'</input> <br><br></div>' + slip.outerHTML;

}

function uncheck(elem){
  if(elem.checked){
    console.log("unchecked")
    elem.checked = false
    rm = document.getElementById(elem.name)
    if(rm != null && typeof(rm) != 'undefined'){
      rm.remove()
    }
  }else{
    console.log("checked")
    elem.checked = true
  }
}
