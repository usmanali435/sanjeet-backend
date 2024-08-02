document.addEventListener('DOMContentLoaded', () => {
    const dragDropArea = document.getElementById('dragDropArea');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const loadingBar = document.getElementById('loadingBar');
    const welcomeMessage = document.getElementById('wel-on');
    const grow = document.getElementById('grow');
    const uploadContainer = document.querySelector('.upload-container');
    const mainContainer = document.querySelector('.pre-i');
    const resetButton = document.getElementById('resetButton');
    const processButton = document.getElementById('processButton');
    
    let selectedFile = null;

    mainContainer.addEventListener('dragover', (event) => {
        event.preventDefault();
        dragDropArea.classList.add('drag-over');
        hideWelcomeMessage();
        showUploadContainer();
    });

    mainContainer.addEventListener('dragleave', (event) => {
        dragDropArea.classList.remove('drag-over');
    });

    dragDropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        handleFiles(event.target.files);
    });

    dragDropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dragDropArea.classList.add('drag-over');
    });

    dragDropArea.addEventListener('dragleave', () => {
        dragDropArea.classList.remove('drag-over');
    });

    dragDropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dragDropArea.classList.remove('drag-over');
        const files = event.dataTransfer.files;
        handleFiles(files);
    });

    resetButton.addEventListener('click', () => {
        resetUpload();
    });

    processButton.addEventListener('click', () => {
        if (selectedFile) {
            engine(selectedFile);
            processButton.disabled = true;
        } else {
            alert('No file selected for processing.');
        }
    });

    function handleFiles(files) {
        for (const file of files) {
            if (file.type.startsWith('image/')) {
                selectedFile = file;
                hideWelcomeMessage();
                hideDragDropArea();
                showLoadingBar();
                uploadFile(file);
            } else {
                alert('Please upload an image file.');
            }
        }
    }

    function showLoadingBar() {
        loadingBar.style.display = 'block';
    }

    function hideLoadingBar() {
        loadingBar.style.display = 'none';
    }

    function hideWelcomeMessage() {
        welcomeMessage.style.display = 'none';
    }

    function showUploadContainer() {
        uploadContainer.style.display = 'block';
    }

    function hideDragDropArea() {
        dragDropArea.style.display = 'none';
    }

    function showDragDropArea() {
        dragDropArea.style.display = 'block';
    }

    function hideUploadContainer() {
        uploadContainer.style.display = 'none';
    }

    function resetUpload() {
        fileInput.value = ''; // Clear the file input
        previewContainer.innerHTML = ''; // Clear the preview
        hideLoadingBar(); // Hide the loading bar
        showWelcomeMessage(); // Show the welcome message
        hideUploadContainer(); // Hide the upload container
        showDragDropArea(); // Show the drag-drop area
        resetButton.style.display = 'none'; // Hide the reset button
        selectedFile = null; // Clear the selected file
        processButton.disabled = true;
    }

    function showWelcomeMessage() {
        welcomeMessage.style.display = 'block';
    }

    function uploadFile(file) {
        const reader = new FileReader();
        reader.onloadstart = () => {
            // Optional: Do something at the start of the load
        };
        reader.onprogress = (event) => {
            if (event.lengthComputable) {
                const percentLoaded = Math.round((event.loaded / event.total) * 100);
                loadingBar.querySelector('.progress-bar').style.width = `${percentLoaded}%`;
            }
        };
        reader.onloadend = (event) => {
            hideLoadingBar();
            displayImage(event.target.result);
            resetButton.style.display = 'block'; // Show the reset button
            processButton.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function displayImage(src) {
        const img = document.createElement('img');
        img.src = src;
        img.style.maxWidth = '100%';
        img.style.height = '100%';
        img.style.position = 'relative'; // Ensure z-index works
        img.style.top = '-10px'; // Adjust as needed
        img.style.zIndex = '50'; // Ensure it’s below the reset button
        previewContainer.innerHTML = '';
        previewContainer.appendChild(img);
    }

    async function engine(file) {
        let user_data = sessionStorage.getItem("user");

        if (user_data) {
            let user = JSON.parse(user_data);
            grow.style.display = "inline-block";
            try {
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('/annovate/engine/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Authorization': `Bearer ${user.token.access}`
                    }
                });

                if (response.ok) {
                    const result = await response.json();
                    grow.style.display = "none";
                    displayImage(result.url);
                    processButton.disabled = false;
                } else {
                    const errorData = await response.json();
                    console.log(errorData);
                    if (errorData.errors && Array.isArray(errorData.errors)) {
                        errorData.errors.forEach(error => {
                            console.log(error);
                        });
                    } else {
                        console.log('An unknown error occurred. Please try again.');
                    }
                    processButton.disabled = false;
                    grow.style.display = "none";
                }
            } catch (error) {
                console.error('Error:', error);
                console.log('An error occurred while submitting the form.');
                processButton.disabled = false;
                grow.style.display = "none";
            }
        } else {
            console.error("No user data found in session storage.");
            processButton.disabled = false;
            grow.style.display = "none";
        }
    }
});


document.addEventListener('DOMContentLoaded', () => {
    let nameElement = document.getElementById("name");
    let classElement = document.getElementById("class");
    let profilePicElement = document.getElementById("profile-pic");
    let profileUpload = document.getElementById("profile-pic-upload");
    let imageInput = document.getElementById("image");
    let bio = document.getElementById("bio");


    // Profile update elements
    let firstname = document.getElementById("firstname");
    let lastname = document.getElementById("lastname");
    let upemail = document.getElementById("upemail");
    let upbio = document.getElementById("upbio");

    // Get session data
    let user_data = sessionStorage.getItem("user");

    // Check if user_data is not null
    if (user_data) {
        
        let user = JSON.parse(user_data);

        // Check for the correct property names
        if (user.first_name && user.last_name) {
            nameElement.innerText = `${user.first_name} ${user.last_name}`;
            if (firstname) firstname.placeholder = user.first_name;
            if (lastname) lastname.placeholder = user.last_name;
        } else if (user.full_name) {
            nameElement.innerText = user.full_name;
        } else {
            nameElement.innerText = "Name not available";
        }

        classElement.innerText = user.class || "Class not available";

        // Set profile picture if profile_url is available
        if (user.profile_url) {
            profilePicElement.src = user.profile_url;
        }

        // Set placeholders for profile update fields
        if (upemail) upemail.placeholder = user.email || "Email not available";
        if (upbio) upbio.placeholder = user.bio || "Bio not added";
        if (bio) bio.innerText = user.bio || "Bio not Updated";
    } else {
        console.error("No user data found in session storage.");
    }

    // Image preview on file upload
    imageInput.addEventListener('change', function (event) {
        let file = event.target.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function (e) {
                profileUpload.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });
});
