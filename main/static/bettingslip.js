
function slip(elem){
  console.log(elem.name);

  let slip = document.querySelector('.slip');

  let html = slip.outerHTML;

  // Get data atributes from tag
  var home = elem.getAttribute("data-home")
  var away = elem.getAttribute("data-away")
  var bet = elem.getAttribute("data-bet")

  //Add game to slip in the html
  slip.outerHTML = '<input type="hidden" id='+ elem.name + 'name='+ elem.name + '>' + home + '-' + away + '<br>Resultado(Tempo Regulamentar): ' + bet +'</input> <br><br>' + slip.outerHTML;


}
