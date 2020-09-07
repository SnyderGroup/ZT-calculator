//const input = document.querySelector("#CSVFile");

/*input.addEventListener("change", function (e) {
    Papa.parse(input.files[0], {
        complete: function (results) {
            console.log(results.data);
            try {
                var numResults = [];
                for (let i = 0; i < results.data.length; i++) {
                    const tableRow = results.data[i];
                    var numRow = [];
                    for (let j = 0; j < tableRow.length; j++) {
                        const tableCell = tableRow[j];
                        //console.log(typeof (tableCell));
                        if (typeof tableCell === 'number') { numRow[j] = tableCell; }
                    }
                    if (numRow.length === 4) { numResults.push(numRow); }
                }
                console.log(numResults);
                setToFile(numResults);
            } catch (error) {
                document.getElementById("output").innerHTML = "Error: Make sure the csv is formatted correctly.";
            }
        },
        dynamicTyping: true,
        worker: true,
        skipEmptyLines: true,
    });
});*/

function OpenInput() {
    var file = document.getElementById("CSVFile").files[0];
    console.log(file instanceof Blob)
    //var file = filesInput.files.item(0);
    //var file = filesInput.item(0);
    var reader = new FileReader();
    reader.onload = function (event) {
        var csvArray = csvReader(event.target.result);

        CalculateData(csvArray);

        var textArray = [];
        for (let i = 0; i < csvArray.length; i++) {
            const element = csvArray[i];
            textArray[i] = element.join("\t");
        }
        text = textArray.join("\n");
        document.getElementById("output").innerHTML = text;
        console.log(text);
    }
    reader.readAsText(file);
}

function csvReader(CSVText) {
    var csvArray = CSVText.split("\n");
    var csvArrayFloat = []
    var i = 0;
    for (i = 0; i < csvArray.length; i++) {
        csvArray[i] = csvArray[i].split(",");
        var goodRow = true;
        var row = [];
        for (let j = 0; j < csvArray[i].length; j++) {
            const IntValue = csvArray[i][j];
            var value = parseFloat(IntValue)
            if (isNaN(value)) {
                goodRow = false;
                break;
            }
            else { row.push(value); }
        }
        if (goodRow) {
            csvArrayFloat.push(row);
        }
    }
    return csvArrayFloat;
}


function setToFile(parsedCSV) {
    document.getElementById("output").innerHTML = JSON.stringify(
        parsedCSV.data.slice(0, 3),
        null,
        4
    );
    console.log(parsedCSV.data);
    console.log(CalculateData(parsedCSV.data));
}

function setToText() {
    Papa.parse(document.getElementById("CSVText").value, {
        complete: function (results) {
            document.getElementById("output").innerHTML = JSON.stringify(
                results.data.slice(0, 3),
                null,
                4
            );
            console.log(results.data);
        },
        dynamicTyping: true,
        worker: true,
        skipEmptyLines: false,
    });
}


// zt-calculator

function optimizeUForDefEff(data) { //garbage optimization:
    var Us = [.1, 4]
    var test_U = [];
    while (true) {
        ux = Math.max(Us);
        um = Math.min(Us);
        if ((um - ux) < .0001 || (um - ux) > -.0001) {
            break
        }
        test_U = []
        var du = (ux - um) / 5;
        for (let x = 0; x < 6; x++) {
            test_U.push(F_efficiency_as_a_function_of_u(data, (um + x * du))[0])
            // if F_efficiency_as_a_function_of_u(data, (um+(x+2)*du)) < if F_efficiency_as_a_function_of_u(data, (um+x*du))
            // break
        }
        place = test_U.findIndex(Math.max(...test_U)) //place is the highest point
        Us = []
        Us.push(um + du * place)
        test_U[place] = -100
        Us.push(um + du * test_U.findIndex(Math.max(...test_U))) // this is finding the second highest
    }
    return (um)
}

function F_zT(T, R, S, K) {
    return ((T * (S ** 2) / (K * R)) / 10 ** 7)
}
function F_max_Red_eff(zT) {
    return ((Math.sqrt(1 + zT) - 1) / (Math.sqrt(1 + zT) + 1))
}

function F_efficiency_as_a_function_of_u(file, initial_u) {
    var notFile = [];
    notFile[0] = initial_u; // not file is so that the file is not changed it should be called something else some sort of efficiency
    for (let index = 0; index < file.length-1; index++) {
        notFile[index + 1] = (1 / (((1 / notFile[index]) * Math.sqrt(Math.abs(1 - 2 * notFile[index] * notFile[index] * (file[index + 1][1] * file[index + 1][3] + file[index][1] * file[index][3]) * (10 ** -5) / 2 * (file[index + 1][0] - file[index][0])))) - (file[index + 1][0] + file[index][0]) / 2 * (file[index + 1][2] - file[index][2]) * (10 ** -6)))
    }
    var NL = file[file.length-1][2] * file[file.length-1][0] / 1000000 + 1 / notFile[notFile.length-1]
    var N1 = file[0][2] * file[0][0] / 1000000 + 1 / notFile[0]
    return ([(NL - N1) / NL, notFile])
}

function CalculateData(StaticData) {
    var data = StaticData // Is this needed in java script?
    for (let rIndex = 0; rIndex < data.length; rIndex++) {
        const row = data[rIndex];
        data[rIndex][4] = F_zT(row[0], row[1], row[2], row[3]); //zt
        data[rIndex][5] = F_max_Red_eff(row[4]); // max reduced efficiency
        data[rIndex][6] = (Math.sqrt(1 + row[4]) - 1) / (row[2] * row[0] / 1000000); // Seebeck
        data[rIndex][7] = null; // something will be added
    }
    optimized_U = optimizeUForDefEff(data)[0]
    var EfficiencyU = F_efficiency_as_a_function_of_u(data, optimized_U)[1]
    for (let i = 0; i < data.length; i++) {
        data[i][7] = EfficiencyU[i];
    }
    for (let rIndex = 0; rIndex < data.length; rIndex++) {
        const datum = data[rIndex];
        redEfficiency = ((datum[7] * (datum[2] - datum[7] * datum[1] * datum[3] * 10) / 10 ** 6) / (datum[7] * datum[2] / 10 ** 6 + 1 / datum[0]));
        data[rIndex][8] = redEfficiency;
        Phi = (datum[2] * datum[0] / 1000000 + 1 / datum[7]);
        data[rIndex][9] = Phi;
    }
    for (let rIndex = 0; rIndex < data.length - 1; rIndex++) {
        efficiency = ((data[rIndex + 1][9] - data[0][9]) / data[rIndex + 1][9]);
        data[rIndex + 1][10] = efficiency;
    }
    for (let rIndex = 0; rIndex < data.length - 1; rIndex++) {
        ZT = (((data[rIndex + 1][0] - data[0][0] * (1 - data[rIndex + 1][10])) / (data[rIndex + 1][0] * (1 - data[rIndex + 1][10]) - data[0][0])) ** 2 - 1)
        data[rIndex + 1][11] = ZT;
    }
    return data
}
