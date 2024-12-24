document.addEventListener("DOMContentLoaded", function () {
    const phoneDisplay = document.getElementById("phone-display");
    const phoneEdit = document.getElementById("phone-edit");
    const editPhoneBtn = document.getElementById("edit-phone-btn");
    const savePhoneBtn = document.getElementById("save-phone-btn");

    editPhoneBtn.addEventListener("click", function () {
        phoneDisplay.style.display = "none";
        phoneEdit.style.display = "inline";
        editPhoneBtn.style.display = "none";
        savePhoneBtn.style.display = "inline";
    });

    savePhoneBtn.addEventListener("click", function () {
        const updatedPhoneNumber = phoneEdit.value;

        // Make an AJAX request to save the updated phone number
        fetch(updatePhoneNumberUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify({phone_number: updatedPhoneNumber}),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to update phone number.");
                }
                return response.json();
            })
            .then((data) => {
                phoneDisplay.textContent = data.phone_number;
                phoneDisplay.style.display = "inline";
                phoneEdit.style.display = "none";
                editPhoneBtn.style.display = "inline";
                savePhoneBtn.style.display = "none";
            })
            .catch((error) => {
                console.error(error);
                alert("Failed to update phone number. Please try again.");
            });
    });
});

console.log("Edit buttons script loaded!");
