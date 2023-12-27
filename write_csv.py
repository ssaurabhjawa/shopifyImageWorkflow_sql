function calculate() {
    var customerWidth = parseFloat(document.getElementById("width").value);
    var customerHeight = parseFloat(document.getElementById("height").value);

    if (!isNaN(customerWidth) && !isNaN(customerHeight)) {
        var requiredArea = customerWidth * customerHeight;

        var rollSizes = [
            { width: 60.00, height: 120.00 },
            { width: 60.00, height: 250.00 },
            { width: 60.00, height: 305.00 },
            { width: 120.00, height: 250.00 },
            { width: 120.00, height: 305.00 }
        ];

        var rollQuantities = [10, 5, 10, 10, 5]; // Example quantities for each roll size

        var suggestedRolls = [];
        var wastageList = [];

        for (var i = 0; i < rollSizes.length; i++) {
            var roll = rollSizes[i];
            var rollArea = roll.width * roll.height;

            var wasteWidth = customerWidth % roll.width;
            var wasteHeight = customerHeight % roll.height;
            var totalWaste = wasteWidth * wasteHeight;

            wastageList.push({ size: roll, wastage: totalWaste });
        }

        wastageList.sort(function(a, b) {
            return a.wastage - b.wastage;
        });

        var n = 3; // Number of roll sizes to suggest
        for (var i = 0; i < n; i++) {
            var suggestion = wastageList[i];
            suggestedRolls.push({ size: suggestion.size, quantity: Math.ceil(requiredArea / (suggestion.size.width * suggestion.size.height))) });
        }

        document.getElementById("bestSize").textContent = "Best Size(s):";
        document.getElementById("quantity").textContent = "Quantity Required:";
        document.getElementById("waste").textContent = "Waste:";

        for (var i = 0; i < suggestedRolls.length; i++) {
            var suggestion = suggestedRolls[i];
            document.getElementById("bestSize").textContent += " " + suggestion.size.width + "x" + suggestion.size.height + " cm";
            document.getElementById("quantity").textContent += " " + suggestion.quantity + " rolls";
            document.getElementById("waste").textContent += " " + wastageList[i].wastage + " cm²";
        }
    }
}