$(document).ready(function() {

    var url_prefix = '/dashboard';

    crossroads.addRoute('/', function() {
        _load_all_instances();
    });
    crossroads.addRoute(url_prefix, function() {
        _load_all_instances();
    });
    crossroads.addRoute(url_prefix + '/instances', function() {
        _load_all_instances();
    });
    crossroads.addRoute(url_prefix + '/report', function() {
        _load_report();
    });
    crossroads.parse(document.location.pathname);
});
