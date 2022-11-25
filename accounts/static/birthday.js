window.onload = function() {
    var date = new Date();
    var dd = date.getDate();
    var mm = date.getMonth() + 1;
    var yyyy = date.getFullYear();

    //Add a zero if one Digit (eg: 05,09)
    if (dd < 10) {
      dd = "0" + dd;
    }

    //Add a zero if one Digit (eg: 05,09)
    if (mm < 10) {
      mm = "0" + mm;
    }

    minYear = yyyy - 80; //Calculate Minimun Age (<80)
    maxYear = yyyy - 18; //Calculate Maximum Age (>18)

    var min = minYear + "-" + mm + "-" + dd;
    var max = maxYear + "-" + mm + "-" + dd;

    document.getElementById("birthday").setAttribute("min", min);
    document.getElementById("birthday").setAttribute("max", max);
  };