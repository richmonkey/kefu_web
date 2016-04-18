define(function(require, exports, module) {
    var loc = this.location;
    var search = loc.search;

    var local = 'localhost:8000/';
    var remote = 'developer.gobelieve.io/';

    seajs.on('fetch', function(data) {
        if (data.uri) {
            if (search.indexOf('online') > -1 && !seajs.development) {
                data.requestUri = data.uri.replace(remote, local);
            } else {
                if (data.uri.indexOf('helper.js') === -1) {
                    data.requestUri = data.uri.replace(remote, local);
                }
            }
        }
    });
});