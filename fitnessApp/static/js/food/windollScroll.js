document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function () {
            localStorage.setItem('my-scroll-pos', window.scrollY);
        });
    });

    const pos = localStorage.getItem('my-scroll-pos');
    if (pos) {
        window.scrollTo(0, pos);
        localStorage.removeItem('my-scroll-pos');
    }
});
