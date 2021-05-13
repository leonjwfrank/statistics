/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/people',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(lname, fname, price) {
            let ajax_options = {
                type: 'POST',
                url: 'api/people',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'lname': lname,
                    'fname': fname,
                    'price': price

                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(lname, fname, price) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/people/' + lname,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'lname': lname,
                    'fname': fname,
                    'price': price
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(lname) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/people/' + lname,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $lname = $('#lname'),
        $fname = $('#fname'),
        $price = $('#price');

    // return the API
    return {
        reset: function() {
            $lname.val('');
            $fname.val('');
            $price.val('').focus();
        },
        update_editor: function(lname, fname, price) {
            $lname.val(lname);
            $fname.val(fname);
            $price.val(price).focus();
        },
        build_table: function(people) {
            let rows = ''

            // clear the table
            $('.people table > tbody').empty();

            // did we get a people array?
            if (people) {
                for (let i=0, l=people.length; i < l; i++) {
                    rows += `<tr><td class="lname">${people[i].lname}</td><td class="fname">${people[i].fname}</td><td class="price">${people[i].price}</td><td>${people[i].timestamp}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $lname = $('#lname'),
        $fname = $('#fname'),
        $price = $('#price');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(lname, fname, price) {
        return lname !== "" && fname !== "" && price !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let lname = $lname.val(),
            fname = $fname.val(),
            price = $price.val();
        e.preventDefault();

        if (validate(lname, fname, price)) {
            model.create(lname, fname, price)
        } else {
            alert('Problem with name or food name input');
        }
    });

    $('#update').click(function(e) {
        let lname = $lname.val(),
            fname = $fname.val(),
            price = $price.val();

        e.preventDefault();

        if (validate(lname, fname, price)) {
            model.update(lname, fname, price)
        } else {
            alert('Problem with name or food name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let lname = $lname.val();

        e.preventDefault();

        if (validate('placeholder', lname)) {
            model.delete(lname)
        } else {
            alert('Problem with name or food name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            lname,
            fname,
            price;

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        fname = $target
            .parent()
            .find('td.fname')
            .text();


        price = $target
            .parent()
            .find('td.price')
            .text();

        view.update_editor(lname, fname, price);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));