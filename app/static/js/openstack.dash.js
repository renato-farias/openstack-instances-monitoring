$(function () {

    function fmtBytes(bytes) {
        if (bytes==0) { return "0 bytes"; }
        var s = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'];
        var e = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, e)).toFixed(2) + " " + s[e];
    }

    print_server_container = function(instance) {
        st = 'warn';
        if (instance.status == 'active') {
            st = 'ok';
        } else if (instance.status == 'shutoff') {
            st = 'err';
        }
        return '<div class="panel panel-instance" data-instance="' + instance.id + '">'
               + '<div class="panel-heading cd-collapsable cd-collapsed">'
                 + '<h3 class="panel-title">'
                 + '<i class="glyphicon glyphicon-off icon-' + st + '"></i> '
                   + instance.name
                 + '</h3>'
               + '</div>'
               + '<div class="panel-body hide">'
                 // + '<div class="row">'
                 //   + '<div class="col-md-3">'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Environment:</span> FRA</div></div>'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Hypervisor Host:</span> onix</div></div>'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Owner:</span> Nome (email@email)</div></div>'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Tenant:</span> B2W</div></div>'
                 //   + '</div>'
                 //   + '<div class="col-md-3">'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">IP:</span> 10.0.0.0 (Fixo)</div></div>'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">IP:</span> 10.0.0.0 (Flutuante)</div></div>'
                 //   + '</div>'
                 //   + '<div class="col-md-3">'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Flavor Name:</span> l1.medium</div></div>'
                 //     + '<div class="row text-center"><div class="col-md-4"><span class="strong block">vCPUs:</span> 4 </div>'
                 //     + '<div class="col-md-4"><span class="strong block">RAM:</span> 512 </div>'
                 //     + '<div class="col-md-4"><span class="strong block">Disk:</span> 10 GB </div></div>'
                 //   + '</div>'
                 //   + '<div class="col-md-3">'
                 //     + '<div class="row"><div class="col-md-12"><span class="strong">Image Name:</span> 10.0.0.0 Lorem ipsum do net la porem (Flutuante)</div></div>'
                 //   + '</div>'
                 // + '</div>'
               + '</div>'
             + '</div>'
    }


    print_server_details = function(server) {
        ips = ''
        for (i=0; i < server.networks.length; i++) {
            ips += '<div class="row"><div class="col-md-12"><span class="strong">IP:</span> ' + server.networks[i].addr + ' (' + server.networks[i].type + ')</div></div>'
        }
        return '<div class="row">'
                + '<div class="col-md-3">'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Environment:</span> FRA</div></div>'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Hypervisor Host:</span> ' + server.hypervisor + '</div></div>'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Owner:</span> ' + server.user.name + ' (' + server.user.email + ')</div></div>'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Tenant:</span> ' + server.tenant.name + '</div></div>'
                + '</div>'
                + '<div class="col-md-3">'
                 + ips
                + '</div>'
                + '<div class="col-md-3">'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Flavor Name:</span> ' + server.flavor.name + '</div></div>'
                 + '<div class="row text-center"><div class="col-md-4"><span class="strong block">vCPUs:</span> ' + server.flavor.vcpus + '</div>'
                 + '<div class="col-md-4"><span class="strong block">RAM:</span> ' + fmtBytes(server.flavor.ram*1024*1024) + '</div>'
                 + '<div class="col-md-4"><span class="strong block">Disk:</span> ' + fmtBytes(server.flavor.disk*1024*1024*1024) + '</div></div>'
                + '</div>'
                + '<div class="col-md-3">'
                 + '<div class="row"><div class="col-md-12"><span class="strong">Image Name:</span> ' + server.image.name + '</div></div>'
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
                            print_server_container(data.instances[i])
                        );
                        if (i == data.instances.length-1) {
                            turn_collapsable();
                        }
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
                            print_server_container(data.instances[i])
                        );
                        if (i == data.instances.length-1) {
                            turn_collapsable();
                        }
                    }
                }
            }
        });
    };

    get_server = function(id) {
        $.ajax({
            url: '/server/' + id,
            cache: false,
            statusCode: {
                200: function(data) {
                    $('.panel-instance[data-instance="' + id + '"] .panel-body').html(
                        print_server_details(data)
                    );
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

    turn_collapsable = function() {
        $('.cd-collapsable').on("click", function (e) {
            if ($(this).hasClass('cd-collapsed')) {
                // expand the panel
                $(this).parent('.panel').find('.panel-body.hide');
                $(this).parent('.panel').find('.panel-body').slideDown().removeClass('hide');
                $(this).removeClass('cd-collapsed');
                get_server($(this).parent('.panel').data('instance'));
            }
            else {
                // collapse the panel
                $(this).parent('.panel').find('.panel-body').slideUp();
                $(this).addClass('cd-collapsed');
            }
        });
    }

    

    load_servers();

});
