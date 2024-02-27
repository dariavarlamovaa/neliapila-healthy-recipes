const arrow = document.getElementById("arrow");
const profilePopupSettings = document.getElementById("profile-popup-settings");
const alertCloseButtons = document.querySelectorAll("#alert__close");
const searchLogo = document.getElementById("search_logo")
const searchBar = document.getElementById("search-bar")
const searchClose = document.getElementById('close-search-bar')
const searchBlockClose = document.getElementById('close-search-bar-block')
const arrowMenuNav = document.getElementById('arrow-menu-nav')
const profileLinksNav = document.getElementById('profile-links')


let isPopupVisible = false;
let isSearchBarVisible = false
let isPopupMenuVisible = false

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
            if (isPopupVisible) {
                profilePopupSettings.style.display = "none";
                arrow.classList.toggle("rotate");
                isPopupVisible = !isPopupVisible;
            }
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

searchClose.addEventListener("click", () => {
    if (isSearchBarVisible) {
        searchBar.style.display = "none";
    }
    isSearchBarVisible = !isSearchBarVisible;
})

searchBlockClose.addEventListener("click", () => {
    if (isSearchBarVisible) {
        searchBar.style.display = "none";
    }
    isSearchBarVisible = !isSearchBarVisible;
})


document.addEventListener('DOMContentLoaded', function () {
    const profilePopup = document.getElementById('profile-popup-settings');

    document.addEventListener('click', function (event) {
        if (isPopupVisible) {
            let isClickInsidePopup = profilePopup.contains(event.target) || arrow.contains(event.target);
            if (!isClickInsidePopup) {
                profilePopup.style.display = 'none';
                arrow.classList.toggle("rotate");
                isPopupVisible = !isPopupVisible;
            }
        }
    });
});

if (arrowMenuNav != null) {
    arrowMenuNav.addEventListener("click", () => {
        arrowMenuNav.classList.toggle("rotate");

        if (isPopupMenuVisible) {
            profileLinksNav.style.display = "none";
        } else {
            profileLinksNav.style.display = "flex";
        }

        isPopupMenuVisible = !isPopupMenuVisible;
    });
}

