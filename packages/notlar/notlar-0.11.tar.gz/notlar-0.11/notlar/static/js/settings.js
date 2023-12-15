$(document).ready(function () {
    var updateProfileForm = $('#update-profile-form');

    updateProfileForm.submit(function (event) {
        event.preventDefault();

        var formData = {
            floating_email: $('#floating_email').val(),
            floating_password: $('#floating_password').val(),
            floating_repeat_password: $('#floating_repeat_password').val(),
            floating_first_name: $('#floating_first_name').val(),
            floating_last_name: $('#floating_last_name').val(),
        };

        $.ajax({
            type: 'POST',
            url: '/update_profile',
            data: formData,
            success: function (response) {
                alert(response.message);  // You can customize how you handle success messages
            },
            error: function (error) {
                displayError(error.responseJSON.error);  // Utilize your error handling function
            }
        });
    });
});
