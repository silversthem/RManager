/*
  Application JS
*/

/* Functions */

function ConfirmBox(insert,display,yesfunc,nofunc = 0,yesdisplay = "Yes",nodisplay = "No") { // Creates a box that that calls yesfunc or nofunc depending on box answer
  if(ConfirmBox.hasOwnProperty('enabled') && ConfirmBox.enabled) { // If a popup is already open
    console.log("Can't open two popup at once") // Can't open a new one
  }
  else {
    ConfirmBox.enabled = true // We've opened a popup
    if(nofunc == 0) { // If the "no" function is null
      nofunc = function(){} // Doing nothing
    }
    insert.appendChild(pushElements([
      New('div','',{class:"panel panel-default small-popup",id:"popup"}),
      [New('div',display,{class:"panel-body"}), // Putting the two buttons in the div
        New('span','<hr/>'),
        Button(yesdisplay,{class:"btn btn-success",style:"float:left;"},function(){
          yesfunc()
          insert.removeChild($("#popup")) // Closing the popup
          ConfirmBox.enabled = false
        }),
        Button(nodisplay,{class:"btn btn-danger",style:"float:right;"},function(){
          nofunc()
          insert.removeChild($("#popup")) // Closing the popup
          ConfirmBox.enabled = false
        })
     ]]))
  }
}

/* Scripting */

$("#addDay-after").onclick = function(){
  ConfirmBox($('#popupcenter'),"Add a new task ?",function(){ // Add a day at the end, then refresh
    addLineToTable($("#tasks_table"),[Cell('#'),Cell('#'),Cell('#'),Cell('#'),Cell('#'),Cell('#')])
  })
}
