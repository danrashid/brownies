function getParam(name) {
  var regex = new RegExp("[?&]" + name + "=([^?&]+)");
  var matches = window.location.search.match(regex) || [];
  return decodeURIComponent(matches[1]);
}
