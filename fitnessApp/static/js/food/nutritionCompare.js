
function calculatePercentageDiff(total, goal) {
    return goal !== 0 ? (((total - goal) / goal) * 100).toFixed(2) : "n/a";

}

function calculateGramsDiff(total, goal) {
    return (total - goal).toFixed(2);
}

function markExceededNutrientGoals(cellTotalEl, cellGramsTdEl, cellDiffPercentTdEl) {
    cellTotalEl.style.backgroundColor = "yellow";
    cellTotalEl.style.color = "red";
    cellGramsTdEl.textContent = `+${cellGramsTdEl.textContent}`;
    cellDiffPercentTdEl.textContent = `+${cellDiffPercentTdEl.textContent}`;
}

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

    const calDiffGramsTdEl = document.querySelector(".calories-diff-grams");
    const carbsDiffGramsTdEl = document.querySelector(".carbs-diff-grams");
    const proteinDiffGramsTdEl = document.querySelector(".protein-diff-grams");
    const fatsDiffGramsTdEl = document.querySelector(".fats-diff-grams");

    const calDiffPercentTdEl = document.querySelector(".calories-diff-percent");
    const carbsDiffPercentTdEl = document.querySelector(".carbs-diff-percent");
    const proteinDiffPercentTdEl = document.querySelector(".protein-diff-percent");
    const fatsDiffPercentTdEl = document.querySelector(".fats-diff-percent");

    calDiffGramsTdEl.textContent = calculateGramsDiff(totalCalories, caloriesGoal);
    carbsDiffGramsTdEl.textContent = calculateGramsDiff(totalCarbs, carbsGoal);
    proteinDiffGramsTdEl.textContent = calculateGramsDiff(totalProtein, proteinGoal);
    fatsDiffGramsTdEl.textContent = calculateGramsDiff(totalFats, fatsGoal);

    calDiffPercentTdEl.textContent = `${calculatePercentageDiff(totalCalories, caloriesGoal)}%`;
    carbsDiffPercentTdEl.textContent = `${calculatePercentageDiff(totalCarbs, carbsGoal)}%`;
    proteinDiffPercentTdEl.textContent = `${calculatePercentageDiff(totalProtein, proteinGoal)}%`;
    fatsDiffPercentTdEl.textContent = `${calculatePercentageDiff(totalFats, fatsGoal)}%`;

    if (totalCalories > caloriesGoal) {
        markExceededNutrientGoals(totalCaloriesTdEl, calDiffGramsTdEl, calDiffPercentTdEl);
    }
    if (totalCarbs > carbsGoal) {
        markExceededNutrientGoals(totalCarbsTdEl, carbsDiffGramsTdEl, carbsDiffPercentTdEl);
    }
    if (totalProtein > proteinGoal) {
        markExceededNutrientGoals(totalProteinTdEl, proteinDiffGramsTdEl, proteinDiffPercentTdEl);
    }
    if (totalFats > fatsGoal) {
        markExceededNutrientGoals(totalFatsTdEl, fatsDiffGramsTdEl, fatsDiffPercentTdEl);
    }
});
