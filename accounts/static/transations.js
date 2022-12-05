
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

function check_phone_number(elem){
  if(elem.value.length==9){
    $('#mbpaybtt').attr("disabled",false)
  }else{
    $('#mbpaybtt').attr("disabled",true)
  }

}

window.cardNumber = false
window.expdate = false
window.cvv = false
window.owner = false

function card_number_mask(elem){
  new_str = elem.value.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/,"$1 $2 $3 $4");
  elem.value = new_str

  if(elem.value.length==19){
    window.cardNumber = true
    if(window.cardNumber && window.expdate && window.cvv && window.owner ){
        $('#paybtt').attr("disabled",false)
    }
  }else{
    window.cardNumber = false
    $('#paybtt').attr("disabled",true)
  }

}

function expdate_mask(elem){
  new_str = elem.value.replace(/(\d{2})(\d{2})/,"$1/$2");
  elem.value = new_str

  if(elem.value.length==5){
    window.expdate = true
    if(window.cardNumber && window.expdate && window.cvv && window.owner ){
        $('#paybtt').attr("disabled",false)
    }
  }else{
    window.expdate = false
    $('#paybtt').attr("disabled",true)
  }

}

function check_cvv(elem){
  if(elem.value.length==3){
    window.cvv = true
    if(window.cardNumber && window.expdate && window.cvv && window.owner ){
        $('#paybtt').attr("disabled",false)
    }
  }else{
    window.cvv = false
    $('#paybtt').attr("disabled",true)
  }

}

function check_name(elem){
  var letters = /^[A-Za-zç]+$/;
  if(elem.value.match(letters)){

    $('#invalid_owner').html("")
    window.owner = true
    if(window.cardNumber && window.expdate && window.cvv && window.owner ){
        $('#paybtt').attr("disabled",false)
    }else{
      window.owner = false
      $('#paybtt').attr("disabled",true)
    }
  }else{
    window.owner = false
    $('#paybtt').attr("disabled",true)
    if(elem.value==""){
        //pass
    }else{
        $('#invalid_owner').html("<span>Not valid</span>")
    }


  }



}
