
function check_deposit_value(elem){
    if(elem.value=="" || (elem.value>=5 && elem.value<=500)){
      // Enable btts to continue for payment
      $('.depositBtt').prop('disabled', false);
      $('.minAmount').html("")
    }else if(elem.value<5){
      // disables btts
      $('.depositBtt').prop('disabled', true);
      $('.minAmount').html("<span>Minimum limit: 5 €</span>")
    }else if(elem.value>500) {
      // disables btts
      $('.depositBtt').prop('disabled', true);
      $('.minAmount').html("<span>Maximum limit reached: 500€</span>")
    }
}
