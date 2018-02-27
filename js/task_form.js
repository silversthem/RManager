var insert_buttons = document.querySelectorAll('[data-action="insert-step"]')
var delete_buttons = document.querySelectorAll('[data-action="delete-step"]')

var steps_counter = parseInt($('#steps-n').value)

function modifyCounter(value) {
  steps_counter += value
  $('#steps-n').value = steps_counter
}

function modifyStepsNumber(start,value) {
  steps = document.querySelectorAll('.step')
  for(var i = start;i < steps.length;i++) {
    let val = i + value
    if(steps[i].id == undefined) continue;
    steps[i].id = 'step'+val
    nodes = steps[i].childNodes
    nodes[0].innerHTML = '#' + val
    nodes[1].onclick = 'deleteStep(' + val + ')'
    nodes[1].onclick = function() { deleteStep(val) }
    nodes[2].name = 'step' + val + '_text'
    nodes[2].id   = 'step' + val + '_text'
    nodes[3].name = 'step' + val + '_tags'
    nodes[3].id   = 'step' + val + '_tags'
    nodes[4].onclick = 'insertStep(' + val+1 + ')'
    nodes[4].onclick = function() { insertStep(val+1) }
  }
}

function insertStep(after) {
  modifyCounter(1)
  // Inserting step
  step = pushElementsNext([
    New('li','',{id:'step'+after,class:'step'}),
    New('span','#'+after),
    New('span','',{class:'glyphicon glyphicon-remove',onclick:'deleteStep('+ after +')'}),
    New('textarea','',{class:"small-textarea",name:"step"+after+'_text',id:"step"+after+'_text',placeholder:"Step description"}),
    New('textarea','',{class:"small-textarea",name:"step"+after+'_tags',id:"step"+after+'_tags',placeholder:"Step tags"}),
    New('button','Add Step',{class:"btn btn-default",onclick:'insertStep(' + after + ')',type:"button"})
  ])
  $('#steps_list').insertBefore(step,document.getElementById('step'+(after-1)).nextSibling)
  modifyStepsNumber(0,1)
}

function deleteStep(step) {
  $('#step'+step).remove()
  modifyStepsNumber(0,1)
  modifyCounter(-1)
}

for(var i = 0;i < insert_buttons.length;i++) {
  insert_buttons[i].onclick = function() {
    insertStep(i+1)
  }
  delete_buttons[i].onclick = function() {
    deleteStep(i+1)
  }
}
