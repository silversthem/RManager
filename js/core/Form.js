/*
  Form js file
  Functions to browse form more easily
*/

function Button(display,infos,clickaction) { // Creates a button quickly, with an onclick action
  var b = New('button',display,infos)
  b.onclick = clickaction
  return b
}
