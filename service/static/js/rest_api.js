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
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        var pet_id = $("#pet_id").val();
        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var data = {
            "name": name,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/pets/" + pet_id,
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
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {
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
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        var pet_id = $("#pet_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/pets/" + pet_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
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
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#pet_name").val();
        var category = $("#pet_category").val();
        var available = $("#pet_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/pets?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            var firstPet = "";
            for(var i = 0; i < res.length; i++) {
                var pet = res[i];
                var row = "<tr><td>"+pet._id+"</td><td>"+pet.name+"</td><td>"+pet.category+"</td><td>"+pet.available+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstPet = pet;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
