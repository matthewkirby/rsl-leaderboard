function revealTimes(button) {
    // Find the block element encompassing the finish times
    var race = button.parentElement.parentElement;
    var finishers = null;
    for(var i=0; i<race.childNodes.length; i++) {
        if (race.childNodes[i].classList.contains("placement-block")) {
            finishers = race.childNodes[i];
            break;
        }
    }

    // Toggle visibility
    if(finishers.style.display === "none") {
        finishers.style.display = "block";
    } else {
        finishers.style.display = "none";
    }
  }