/*
  Dom js file
  Functions to make dom document usage easier
*/

function $(element) // basic JQuery selector copy
{
  switch (element[0]) {
    case '.': // Class
      return document.getElementsByClassName(element.substring(1))
    break;
    case '#': // Id
      return document.getElementById(element.substring(1))
    default: // Else
    var elements = document.getElementsByTagName(element)
    if (elements.length == 1) { // An array of one element is an element
      return elements[0]
    } else {
      return elements
    }
  }
}

function New(type,display = '',infos = {}) { // Creates an element
  var element = document.createElement(type)
  element.innerHTML = display
  for(var propriety in infos) { // Going through each attribute of the future element
    if(infos.hasOwnProperty(propriety)) {
      element.setAttribute(propriety,infos[propriety]) // Setting the propriety and its value
    }
  }
  return element
}

function  pushElementsNext(elements) { // Adds all elements as successive children of the first one, if one element is an array ~> applying pushElements on said array
  var parent = elements[0]
  elements.shift()
  elements.reverse()
  elements.unshift(parent)
  for(var i = (elements.length - 1);i > 0;i--) {
    if(Array.isArray(elements[i])) {
      elements[i-1].appendChild(pushElements(elements[i]))
    } else {
      elements[0].appendChild(elements[i])
    }
  }
  return elements[0]
}

function pushElements(elements) { // Adds all elements as children of the previous one, if one element is array ~> applying pushElementsNext on said array
  var parent = elements[0]
  for(var i = 1;i < elements.length;i++) {
    if(Array.isArray(elements[i])) {
      var newNode = pushElementsNext(elements[i])
      parent.appendChild(newNode)
      parent = newNode[0]
    } else {
      parent.appendChild(elements[i])
      parent = elements[i]
    }
  }
  return elements[0]
}

function clearElement(element) { // Erases all children of an element
  element.innerHTML = ''
  return element
}
