document.addEventListener('DOMContentLoaded', function () {
    const currentSortOption = getParameterByName('sort_by');

    if (currentSortOption) {
        const links = document.querySelectorAll('.categories-ul li a');

        links.forEach(link => {
            const href = link.getAttribute('href');

            if (href.includes(currentSortOption)) {
                link.parentElement.classList.add('selected');
            }
        });
    }
});

function getParameterByName(name) {
    const regex = new RegExp("[?&]" + name + "=([^&#]*)");
    const results = regex.exec(window.location.href);

    return results ? decodeURIComponent(results[1].replace(/\+/g, " ")) : null;
}