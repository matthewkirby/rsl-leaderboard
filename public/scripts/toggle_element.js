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

function toggle_block_visibility(element, className) {
    let parent = element.parentElement;
    let block = null;
    for(let i=0; i<parent.childNodes.length; i++) {
        child = parent.childNodes[i];
        if(child.nodeType === 1 && child.classList.contains(className)) {
            block = child;
            break;
        }
    }
    block.style.display = block.style.display === "none" ? "block" : "none";
}