document.addEventListener('DOMContentLoaded', function () {
    // Handle the signup form
    const signupForm = document.getElementById('signupForm');
    const message = document.getElementById('message');
    if (signupForm) {
        signupForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const email = document.getElementById('stremail').value;

            if (email) {
                try {
                    const response = await fetch('/account/user/email-check/', {
                        method: 'POST',
                        body: JSON.stringify({ email: email }),
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                        }
                    });

                    const result = await response.json();
                    console.log(result);

                    if (response.ok) {
                        // Email check was successful, proceed with form submission or next steps
                        sessionStorage.setItem('tempEmail', email); // Store the email in session storage
                        window.location.href = '/bud-apps/signup-pass'; // Redirect to the next page
                    } else {
                        // Handle errors returned from the server
                        message.style.color = "red";
                        message.innerText = result.message;

                    }
                } catch (e) {
                    console.error('An error occurred:', e);
                    alert('An error occurred while checking the email.');
                }
            } else {
                alert('Please enter an email.');
            }
        });
    }

    const signupContinueForm = document.getElementById('signup-continue');
    if (signupContinueForm) {
        signupContinueForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission
            const email = sessionStorage.getItem('tempEmail');
            const form = event.target;
            const formData = new FormData(form);
            formData.append('email', email);

            // Password confirmation validation
            if (formData.get('Password1') !== formData.get('Password2')) {
                butterup.toast({
                    title: 'Registration Error',
                    message: 'Passwords do not match!',
                    type: 'error',
                });
                return;
            }

            try {
                const response = await fetch('/account/user/register/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                        // No need for 'Content-Type': 'multipart/form-data' when using FormData
                    }
                });

                if (response.ok) {
                    const result = await response.json();
                    // Handle success (e.g., redirect, show a message)
                    sessionStorage.setItem('user', JSON.stringify(result.user))
                    window.location.href = '/';
                } else {
                    // Handle errors
                    const errorData = await response.json();
                    console.log(errorData);
                    if (errorData.errors && Array.isArray(errorData.errors)) {
                        errorData.errors.forEach(error => {
                            butterup.toast({
                                title: 'Registration Error',
                                message: error,
                                type: 'error',
                            });
                        });
                    } else {
                        butterup.toast({
                            title: 'Registration Error',
                            message: 'An unknown error occurred. Please try again.',
                            type: 'error',
                        });
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                butterup.toast({
                    title: 'Registration Error',
                    message: 'An error occurred while submitting the form.',
                    type: 'error',
                });
            }
        });
    }
    const updateUserProfile = document.getElementById('updateuser-profile');
    if (updateUserProfile) {
        updateUserProfile.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission
            const form = event.target;
            const formData = new FormData(form);
            // Get session data
            let user_data = sessionStorage.getItem("user");
            // Check if user_data is not null
            if (user_data) {
                let user = JSON.parse(user_data);
                console.log(user.token.access);
                try {
                    const response = await fetch(`/account/user/update-profile/${user.class}/`, {
                        method: 'PUT',
                        body: formData,
                        headers: {
                            'Accept': 'application/json',
                            "Authorization": `Bearer ${user.token.access}`
                        }
                    });

                    if (response.ok) {
                        const result = await response.json();
                        // Handle success (e.g., redirect, show a message)
                        butterup.toast({
                            title: 'Profile Update Success',
                            message: 'Your profile has been successfully updated!',
                            type: 'success',
                        });

                        // Update sessionStorage data
                        let updatedUser = {
                            ...user,
                            ...result.user,
                            class: user.class,  // Keep the original class
                            token: user.token   // Keep the original token
                        };
                        sessionStorage.setItem("user", JSON.stringify(updatedUser));

                    } else {
                        // Handle errors
                        const errorData = await response.json();
                        console.log(errorData);
                        if (errorData.Error && Array.isArray(errorData.Error)) {
                            errorData.Error.forEach(error => {
                                butterup.toast({
                                    title: 'Profile Update Error',
                                    message: error,
                                    type: 'error',
                                });
                            });
                        } else {
                            butterup.toast({
                                title: 'Profile Update Error',
                                message: 'An unknown error occurred. Please try again.',
                                type: 'error',
                            });
                        }
                    }
                } catch (error) {
                    console.error('Error:', error);
                    butterup.toast({
                        title: 'Profile Update Error',
                        message: 'An error occurred while submitting the form.',
                        type: 'error',
                    });
                }
            } else {
                console.error("No user data found in session storage.");
            }
        });
    }
    const chngPass = document.getElementById('chng-pass');
    if (chngPass) {
        chngPass.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const form = event.target;
            const formData = new FormData(form);

            // Get session data
            let user_data = sessionStorage.getItem("user");

            // Check if user_data is not null
            if (user_data) {
                let user = JSON.parse(user_data);

                try {
                    const response = await fetch('/account/user/update-profile/change-password/', {
                        method: 'PUT',
                        body: formData,
                        headers: {
                            'Authorization': `Bearer ${user.token.access}`
                        }
                    });

                    if (response.ok) {
                        const result = await response.json();
                        butterup.toast({
                            title: 'Password Change Success',
                            message: 'Your password has been successfully updated!',
                            type: 'success',
                        });

                        // No need to update user data in sessionStorage for password change
                        // Just show a success message

                    } else {
                        // Handle errors
                        const errorData = await response.json();
                        console.log(errorData);
                        if (errorData.Error && Array.isArray(errorData.Error)) {
                            errorData.Error.forEach(error => {
                                butterup.toast({
                                    title: 'Password Change Error',
                                    message: error,
                                    type: 'error',
                                });
                            });
                        } else {
                            butterup.toast({
                                title: 'Password Change Error',
                                message: 'An unknown error occurred. Please try again.',
                                type: 'error',
                            });
                        }
                    }
                } catch (error) {
                    console.error('Error:', error);
                    butterup.toast({
                        title: 'Password Change Error',
                        message: 'An error occurred while submitting the form.',
                        type: 'error',
                    });
                }
            } else {
                console.error("No user data found in session storage.");
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission

            const form = event.target;
            const formData = new FormData(form);


            try {
                const response = await fetch('/account/user/login/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',

                    }
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log(result.user);
                    // Handle success (e.g., redirect, show a message)
                    sessionStorage.setItem('user', JSON.stringify(result.user));
                    window.location.href = '/';
                } else {
                    // Handle errors
                    const errorData = await response.json();
                    console.log(errorData);
                    if (errorData.errors && Array.isArray(errorData.errors)) {
                        errorData.errors.forEach(error => {
                            butterup.toast({
                                title: 'Login Error',
                                message: error,
                                type: 'error',
                            });
                        });
                    } else {
                        butterup.toast({
                            title: 'Login Error',
                            message: 'An unknown error occurred. Please try again.',
                            type: 'error',
                        });
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                butterup.toast({
                    title: 'Login Error',
                    message: 'An error occurred while submitting the form.',
                    type: 'error',
                });
            }
        });
    }


});