const arrow = document.getElementById("arrow");
const profilePopupSettings = document.getElementById("profile-popup-settings");
const alertCloseButton = document.getElementById("alert__close");
const alertBlock = document.getElementById("alert");

let isPopupVisible = false;

if (arrow != null) {
    arrow.addEventListener("click", () => {
        arrow.classList.toggle("rotate");

        if (isPopupVisible) {
            profilePopupSettings.style.display = "none";
        } else {
            profilePopupSettings.style.display = "flex";
        }

        isPopupVisible = !isPopupVisible
    });
}

if (alertCloseButton != null) {
    alertCloseButton.addEventListener("click", () => {
        alertBlock.style.display = "none";
    });
}