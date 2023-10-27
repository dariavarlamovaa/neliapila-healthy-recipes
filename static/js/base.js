const arrow = document.getElementById("arrow");
const profilePopupSettings = document.getElementById("profile-popup-settings");
const alertCloseButtons = document.querySelectorAll("#alert__close");
const searchLogo = document.getElementById("search_logo")
const searchBar = document.getElementById("search-bar")

let isPopupVisible = false;
let isSearchBarVisible = false

if (arrow != null) {
    arrow.addEventListener("click", () => {
        arrow.classList.toggle("rotate");

        if (isPopupVisible) {
            profilePopupSettings.style.display = "none";
        } else {
            profilePopupSettings.style.display = "flex";
        }

        isPopupVisible = !isPopupVisible;
    });
}

if (searchLogo != null) {
    searchLogo.addEventListener("click", () => {
        if (isSearchBarVisible) {
            searchBar.style.display = "none";
        } else {
            searchBar.style.display = "block"
        }
        isSearchBarVisible = !isSearchBarVisible;
    })
}


alertCloseButtons.forEach(alertCloseButton => {
    alertCloseButton.addEventListener("click", () => {
        const alertBlock = alertCloseButton.closest("#alert");
        if (alertBlock) {
            alertBlock.style.display = "none";
        }
    });
});
