$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        // console.log("update_form_data: res try")
        // console.log(res)
        addr = res.address;
        $("#user_id").val(res.user_id);
        $("#first_name").val(res.first_name);
        $("#last_name").val(res.last_name);
        $("#street").val(addr.street);
        $("#apartment").val(addr.apartment);
        $("#city").val(addr.city);
        $("#state").val(addr.state);
        $("#zip_code").val(addr.zip_code);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#user_id").val("");
        $("#first_name").val("");
        $("#last_name").val("");
        $("#password").val("");

        $("#street").val("");
        $("#apartment").val("");
        $("#city").val("");
        $("#state").val("");
        $("#zip_code").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        // get user info from the ui
        var user_id = $("#user_id").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var password = $("#password").val();

        // get address from the ui
        var street = $("#street").val();
        var apartment = $("#apartment").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip_code = $("#zip_code").val();

        // create address obj
        var address = {
            "street": street,
            "apartment": apartment,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }

        // create data obj
        var data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address": address
        };

        // send it to the backend
        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


// ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        var user_id = $("#user_id").val();
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var password = $("#password").val();

        // get address from the ui
        var street = $("#street").val();
        var apartment = $("#apartment").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip_code = $("#zip_code").val();

        // create address obj
        var address = {
            "street": street,
            "apartment": apartment,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }

        // create data obj
        var data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address": address
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + user_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Deactivate a Customer
    // ****************************************

    $("#deactivate-btn").click(function () {

        var user_id = $("#user_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + user_id + "/deactivate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            // console.log(res)
            update_form_data(res)
            flash_message("Customer deactivated.")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Activate a Customer
    // ****************************************

    $("#activate-btn").click(function () {

        var user_id = $("#user_id").val();

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + user_id + "/activate",
                contentType: "application/json"
            })

        ajax.done(function(res){
            // console.log(res)
            update_form_data(res)
            flash_message("Customer activated.")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#search-btn").click(function () {
        console.log("retrieve-btn.click")
        var user_id = $("#user_id").val();
        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + user_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            console.log("retrieve-btn.click: res")
            console.log(res)
            update_form_data(res[0])
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        var user_id = $("#user_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/customers/" + user_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {
        var fname = $("#first_name").val();
        var lname = $("#last_name").val();
        var city = $("#city").val();
        var state = $("#state").val();
        var zip = $("#zip_code").val();

        var queryString = ""

        
        if (fname) {
            queryString += 'fname=' + fname
        }
        if (lname) {
            if (queryString.length > 0) {
                queryString += '&lname=' + lname
            } else {
                queryString += 'lname=' + lname
            }
        }
        if (city) {
            if (queryString.length > 0) {
                queryString += '&city=' + city
            } else {
                queryString += 'city=' + city
            }
        }
        if (state) {
            if (queryString.length > 0) {
                queryString += '&state=' + state
            } else {
                queryString += 'state=' + state
            }
        }
        if (zip) {
            if (queryString.length > 0) {
                queryString += '&zip=' + zip
            } else {
                queryString += 'zip=' + zip
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:5%">ID</th>'
            header += '<th style="width:10%">User Name</th>'
            header += '<th style="width:15%">First Name</th>'
            header += '<th style="width:15%">Last Name</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:15%">Active</th></tr>'
            $("#search_results").append(header);
            var firstCust = "";
            for(var i = 0; i < res.length; i++) {
                var customer = res[i];
                var addr = customer.address
                var row = "<tr><td>"+customer.customer_id+"</td><td>"+customer.user_id+"</td><td>"+customer.first_name+"</td><td>"+customer.last_name+"</td><td>"+
                addr.street+", "+addr.apartment+", "+addr.city+", "+addr.state+" - "+addr.zip_code+"</td><td>"+customer.active+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstCust = customer;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstCust != "") {
                update_form_data(firstCust)
            }
            else {
                clear_form_data()
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });
})
