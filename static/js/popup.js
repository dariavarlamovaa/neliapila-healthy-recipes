const arrow = document.getElementById("arrow");
const profilePopupSettings = document.getElementById("profile-popup-settings");

let isPopupVisible = false;

arrow.addEventListener("click", () => {
    arrow.classList.toggle("rotate");

    if (isPopupVisible) {
        profilePopupSettings.style.display = "none";
    } else {
        profilePopupSettings.style.display = "block";
    }

    isPopupVisible = !isPopupVisible

});