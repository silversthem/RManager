/*
  Table js file
  Functions to manipulate tables
*/

function addLineToTable(table,elements) { // Adds elements to a table, elements is an array with each element being a td
  var tr = New('tr')
  for(var i in elements) {
    tr.appendChild(elements[i])
  }
  table.appendChild(tr)
  return tr
}

function Cell(display,infos = {}) { // Returns a td containing display
  return New('td',display,infos)
}
