document.addEventListener("DOMContentLoaded", () => {
    const totalCaloriesTdEl = document.querySelector(".calories-total");
    const totalCalories = parseFloat(totalCaloriesTdEl.textContent);
    const totalCarbsTdEl = document.querySelector(".carbs-total");
    const totalCarbs = parseFloat(totalCarbsTdEl.textContent);
    const totalProteinTdEl = document.querySelector(".protein-total");
    const totalProtein = parseFloat(totalProteinTdEl.textContent);
    const totalFatsTdEl = document.querySelector(".fats-total");
    const totalFats = parseFloat(totalFatsTdEl.textContent);

    const caloriesGoalTdEl = document.querySelector(".calories-goal");
    const caloriesGoal = parseFloat(caloriesGoalTdEl.textContent);
    const carbsGoalTdEl = document.querySelector(".carbs-goal");
    const carbsGoal = parseFloat(carbsGoalTdEl.textContent);
    const proteinGoalTdEl = document.querySelector(".protein-goal");
    const proteinGoal = parseFloat(proteinGoalTdEl.textContent);
    const fatsGoalTdEl = document.querySelector(".fats-goal");
    const fatsGoal = parseFloat(fatsGoalTdEl.textContent);

    if (totalCalories > caloriesGoal) {
        totalCaloriesTdEl.style.backgroundColor = "yellow";
        totalCaloriesTdEl.style.color = "red";
    }
    if (totalCarbs > carbsGoal) {
        totalCarbsTdEl.style.backgroundColor = "yellow";
        totalCarbsTdEl.style.color = "red";
    }
    if (totalProtein > proteinGoal) {
        totalProteinTdEl.style.backgroundColor = "yellow";
        totalProteinTdEl.style.color = "red";
    }
    if (totalFats > fatsGoal) {
        totalFatsTdEl.style.backgroundColor = "yellow";
        totalFatsTdEl.style.color = "red";
    }
});
