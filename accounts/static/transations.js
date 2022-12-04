
function check_deposit_value(elem){
    if(elem.value=="" || (elem.value>=5 && elem.value<=500)){
      // Enable btts to continue for payment
      $('.depositBtt').prop('disabled', false);
      $('.minAmount').html("")
    }else if(elem.value<5){
      // disables btts
      $('.depositBtt').prop('disabled', true);
      $('.minAmount').html("<br>Limite mínimo: 5 €")
    }else if(elem.value>500) {
      // disables btts
      $('.depositBtt').prop('disabled', true);
      $('.minAmount').html("Limite máximo atingido: 500€")
    }
}
