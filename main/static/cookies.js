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


function sendData(data) {
  console.log('Sending data');

  const XHR = new XMLHttpRequest();

  const urlEncodedDataPairs = [];

  // Turn the data object into an array of URL-encoded key/value pairs.
  for (const [name, value] of Object.entries(data)) {
    urlEncodedDataPairs.push(`${encodeURIComponent(name)}=${encodeURIComponent(value)}`);
  }

  // Combine the pairs into a single string and replace all %-encoded spaces to
  // the '+' character; matches the behavior of browser form submissions.
  const urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

  // Define what happens on successful data submission
  XHR.addEventListener('load', (event) => {
    alert('Yeah! Data sent and response loaded.');
  });

  // Define what happens in case of error
  XHR.addEventListener('error', (event) => {
    alert('Oops! Something went wrong.');
  });

  // Set up our request
  XHR.open('POST', 'http://127.0.0.1:8000/gamble/bet');

  // Add the required HTTP header for form data POST requests
  XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

  // Finally, send our data.
  XHR.send(urlEncodedData);
}



function sendToCookie(){
  sendData({ test: 'ok' });
  type = sessionStorage.getItem("betType")
  amount = sessionStorage.getItem("amount")
  sessionStorage.removeItem("betType");
  sessionStorage.removeItem("amount");
  keys = Object.keys(sessionStorage)

  var cookieValue = "" +type+"|"+amount+"|"
  for(var i=0;i<keys.length;i++){
    if(i==keys.length-1){
      cookieValue += "" + keys[i]+"/"+sessionStorage.getItem(keys[i])
    }else{
      cookieValue +=  "" + keys[i]+"/"+sessionStorage.getItem(keys[i])+"|"
    }

  }
  console.log(cookieValue)
  setCookie("slip",cookieValue,365)

  window.location.href = "/gamble/bet"
}
