$(function () {

    print_server_container = function(name) {
        return '<div class="panel panel-instance">'
               + '<div class="panel-heading cd-collapsable cd-collapsed">'
                 + '<h3 class="panel-title">'
                   + name
                 + '</h3>'
               + '</div>'
               + '<div class="panel-body hide">'
               + '</div>'
             + '</div>'
    }

    load_servers = function() {
        $('.panel-instance-list').empty();
        $.ajax({
            url: '/servers',
            cache: false,
            statusCode: {
                200: function(data) {
                    for (i = 0; i < data.instances.length; i++) {
                        $('.panel-instance-list').append(
                            print_server_container(data.instances[i].name)
                        );
                    }
                }
            }
        });
    };

    search_servers = function(s) {
        $('.panel-instance-list').empty();
        $.ajax({
            url: '/search/' + s,
            cache: false,
            statusCode: {
                200: function(data) {
                    for (i = 0; i < data.instances.length; i++) {
                        $('.panel-instance-list').append(
                            print_server_container(data.instances[i].name)
                        );
                    }
                }
            }
        });
    };


    $('input[name="instance_name"]').on('keydown', function(e) {
        if (e.which == 13) {
            e.preventDefault();
            if ($(this).val().length >= 3) {
                search_servers($(this).val());
            }
        }
    });

    $('button[name="clear"]').on('click', function() {
        $('input[name="instance_name"]').val('');
        load_servers();
    });

    load_servers();

});
