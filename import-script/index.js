const excelToJson = require('./convert-excel-to-json');
const sourceFile = "./Aparat Listesi.xlsx";


const commentsData = excelToJson({
    sourceFile,
    range: 'A1:BU1',
    onlyComments: true,
    header: {rows: 0},
})

const excelData = excelToJson({
    sourceFile,
})

const sheetName = Object.keys(excelData)[0];
const comments = commentsData[sheetName]


const cellToProductGroup = {};
const productsInsetSQLs = [];
Object.entries(excelData[sheetName][0]).forEach(([cell, group]) => {
    if (cell === "A") {
        return;
    }
    const cellCode = `${cell}1`;
    const products = comments[cellCode] ? comments[cellCode].split('\n').filter(c => !!c) : [];
    cellToProductGroup[cell] = group;
    products.forEach((productName) => {
        productsInsetSQLs.push(`INSERT INTO products (bracket_group, product_name, image) VALUES ("${group}", "${productName}", "");`)
    })
});


const vehiclesInsetSQLs = [];
const relationInsetSQLs = [];
let brandName = "";
Object.entries(excelData[sheetName]).forEach((line) => {
    const [index, cells] = line;
    if (index === "0") {
        return;
    }
    const title = cells['A'];
    const code = title.split("-")[0].replace(/[^0-9]+/gm, '');
    const codeInt = parseFloat(code);
    let name = title.substr(code.length + 3, title.length);
    let years = name.match(/\[(.*)\]/gm);
    if(!years) {
        years = name.match(/\((.*)\)/gm);
    }


    let startYear = null;
    let endYear = null;
    if(years) {
        name = name.replace((years[0]),'').replace(/^\s+|\s+$/gm,'');
        years = years[0].replace((/\[?\]?\(?\)?/gm),'');
        const yearsSplit = years
            .replace("+","/")
            .replace("-","/")
            .split("/");
        if(yearsSplit[0]) {
            startYear = parseFloat(yearsSplit[0])>50? `19${yearsSplit[0]}`:`20${yearsSplit[0]}`;
        }
        if(yearsSplit[1]) {
            endYear = parseFloat(yearsSplit[1])>50? `19${yearsSplit[1]}`:`20${yearsSplit[1]}`;
        }
    }

    const isBrand = codeInt % 100 === 0;
    brandName = isBrand ? name : brandName;

    if(isBrand) {
        return;
    }


    vehiclesInsetSQLs.push(`INSERT INTO vehicles (code, name, start_year, end_year, brand) VALUES (${code}, "${name}", ${startYear}, ${endYear}, "${brandName}");`)

    //console.log(index, codeInt, brandName, name, startYear, endYear);

    Object.entries(cells).forEach(([cell, value])=>{
        if(cell === "A") {
            return;
        }
        const vehicleId = vehiclesInsetSQLs.length;
        const group = cellToProductGroup[cell]
        relationInsetSQLs.push(`INSERT INTO vehicle_product (vehicle_id, bracket_group) VALUES (${vehicleId}, ${group});`)
        //console.log(name, cell, value, group)
    });


})


//console.log(productsInsetSQLs.join("\n"))
//console.log(vehiclesInsetSQLs.join("\n"))
console.log(relationInsetSQLs.join("\n"))


