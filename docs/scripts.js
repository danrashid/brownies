function getParam(name) {
  var regex = new RegExp("[?&]" + name + "=([^?&]+)");
  var matches = window.location.search.match(regex) || [];
  return matches[1] && decodeURIComponent(matches[1]);
}
