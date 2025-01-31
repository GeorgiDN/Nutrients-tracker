let foodData = {};

function fillData(data, key1, key2, nutrients, element) {
    data[key1][key2][nutrients] += parseFloat(element.textContent) || 0;
    return data
}

const tableEls = document.querySelectorAll(".nutrients-table");

tableEls.forEach(table => {
    const h3El = table.previousElementSibling;
    if (!h3El) return;

    const mealType = h3El.textContent.trim();
    foodData[mealType] = {};

    const allRowsEl = table.querySelectorAll("tbody tr");
    allRowsEl.forEach(row => {
        const foodNameEl = row.querySelector(".food-name");
        const foodGramsEl = row.querySelector(".food-quantity");
        const foodCaloriesEl = row.querySelector(".food-calories");
        const foodCarbsEl = row.querySelector(".food-carbs");
        const foodProteinEl = row.querySelector(".food-protein");
        const foodFatsEl = row.querySelector(".food-fats");

        if (foodNameEl && foodGramsEl && foodCaloriesEl && foodCarbsEl && foodProteinEl && foodFatsEl) {
            const foodName = foodNameEl.textContent.trim();

            if (!foodData[mealType][foodName]) {
                foodData[mealType][foodName] = {grams: 0, calories: 0, carbs: 0, protein: 0, fats: 0};
            }

            foodData = fillData(foodData, mealType, foodName, 'grams', foodGramsEl);
            foodData = fillData(foodData, mealType, foodName, 'calories', foodCaloriesEl);
            foodData = fillData(foodData, mealType, foodName, 'carbs', foodCarbsEl);
            foodData = fillData(foodData, mealType, foodName, 'protein', foodProteinEl);
            foodData = fillData(foodData, mealType, foodName, 'fats', foodFatsEl);
        }
    });
});

foodData['TotalNutrients'] = {
    'total': {calories: 0, carbs: 0, protein: 0, fats: 0},
    'goal': {calories: 0, carbs: 0, protein: 0, fats: 0},
}

const tableTotalEls = document.querySelector(".nutrients-table-total");

const caloriesTotal = tableTotalEls.querySelector(".calories-total");
const carbsTotal = tableTotalEls.querySelector(".carbs-total");
const proteinTotal = tableTotalEls.querySelector(".protein-total");
const fatsTotal = tableTotalEls.querySelector(".fats-total");
foodData = fillData(foodData, 'TotalNutrients', 'total', 'calories', caloriesTotal);
foodData = fillData(foodData, 'TotalNutrients', 'total', 'carbs', carbsTotal);
foodData = fillData(foodData, 'TotalNutrients', 'total', 'protein', proteinTotal);
foodData = fillData(foodData, 'TotalNutrients', 'total', 'fats', fatsTotal);

const caloriesGoal = tableTotalEls.querySelector(".calories-goal");
const carbsGoal = tableTotalEls.querySelector(".carbs-goal");
const proteinGoal = tableTotalEls.querySelector(".protein-goal");
const fatsGoal = tableTotalEls.querySelector(".fats-goal");
foodData = fillData(foodData, 'TotalNutrients', 'goal', 'calories', caloriesGoal);
foodData = fillData(foodData, 'TotalNutrients', 'goal', 'carbs', carbsGoal);
foodData = fillData(foodData, 'TotalNutrients', 'goal', 'protein', proteinGoal);
foodData = fillData(foodData, 'TotalNutrients', 'goal', 'fats', fatsGoal);

const userSpanEL = document.querySelector(".username");
const user = userSpanEL.textContent;

const userNutrients = {};
userNutrients[user] = {};
userNutrients[user] = foodData

document.getElementById("save-nutrients").addEventListener("click", function () {
    const jsonData = JSON.stringify(userNutrients);

    fetch(saveUserNutrientsURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: jsonData
    })
        .then(response => response.json())
        .then(data => {
            alert("Nutrient data saved successfully!");
            console.log(data);
        })
        .catch(error => console.error("Error saving JSON:", error));
});

function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
