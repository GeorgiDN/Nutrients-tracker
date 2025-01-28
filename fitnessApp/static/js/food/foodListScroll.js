document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function (event) {
            const row = event.target.closest('tr');
            if (row && row.id) {
                localStorage.setItem('target-food-id', row.id);
            }
        });
    });

    const targetFoodId = localStorage.getItem('target-food-id');
    if (targetFoodId) {
        const targetRow = document.getElementById(targetFoodId);
        if (targetRow) {
            targetRow.scrollIntoView({behavior: 'smooth', block: 'center'});
        }
        localStorage.removeItem('target-food-id');
    }
});
