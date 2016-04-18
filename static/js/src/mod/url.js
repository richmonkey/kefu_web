define(function(require, exports, module) {
  var exports = {}

  exports.getURLParameter = function(name, search) {
    search = search || location.search
    var param = search.match(
      RegExp(name + '=' + '(.+?)(&|$)'))
    return param ? decodeURIComponent(param[1]) : null
  }

  var rNonQuerystring = /\+/g

  exports.deparam = function(string) {
    var params = {}
      , paramsArray = string.replace(rNonQuerystring, ' ').split('&')

    for (var i = 0, l = paramsArray.length; i < l; i++) {
      var paramString = paramsArray[i]
        , pair = paramString.split('=')
        , paramName = decodeURIComponent([pair[0]])
        , paramValue = decodeURIComponent([pair[1]])

      params[paramName] = paramValue
    }

    return params
  }

  // copy from
  // https://github.com/jfromaniello/url-join/blob/master/lib/url-join.js
  // version: b02169596877a1e6cd518f1b0d711f38c721fb02
  function normalize(str) {
    return str
      .replace(/[\/]+/g, '/')
      .replace(/\/\?/g, '?')
      .replace(/\/\#/g, '#')
      .replace(/\:\//g, '://')
  }

  var join = exports.join = function() {
    var joined = [].slice.call(arguments, 0).join('/')
    return normalize(joined)
  }

  exports.addParam = function(url, params) {
    var paramString = ''

    for (var key in params) {
      if (!params.hasOwnProperty(key)) { continue }

      var value = params[key]
      if (value === '' || typeof value === 'undefined') { continue }

      if (paramString) { paramString += '&' }
      paramString += encodeURIComponent(key)
        + '=' + encodeURIComponent(value)
    }

    if (!paramString) { return url }

    var hash = ''
      , search = ''
      , rest = url
      , hashIndex = rest.indexOf('#')
      , markIndex = rest.indexOf('?')

    if (hashIndex !== -1) {
      hash = rest.substr(hashIndex)
      rest = rest.slice(0, hashIndex)
    }

    if (markIndex !== -1) {
      search = rest.substr(markIndex)
      rest = rest.slice(0, markIndex)
    }

    return (rest
      + (search ? (search + '&' + paramString) : ('?' + paramString))
      + (hash ? hash : ''))
  }

  var hasSameOrigin = exports.hasSameOrigin = function(url, originUrl) {
    if (url[0] === '/') { return true }
    var rOrigin = new RegExp('^' + originUrl)
    return rOrigin.test(url)
  }

  exports.getRelativeUrl = function(url, originUrl) {
    if (url[0] === '/' || !hasSameOrigin(url, originUrl)) { return url }
    return join('/', url.substr(originUrl.length))
  }

  module.exports = exports
});