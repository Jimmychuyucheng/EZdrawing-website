const display = document.getElementById("display");

function appendToDisplay(input) {
    // 添加 ^ 符号表示指数的功能
    if (input === '^') {
        display.value += '^';
    } else if (input === '(' || input === ')') {
        display.value += input;
    } else {
        display.value += input;
    }
}

function clearDisplay() {
    display.value = "";
}

function calculate() {
    try {
        let expression = display.value;

        // 處理括號內的表達式
        while (expression.includes('(')) {
            const startIndex = expression.lastIndexOf('(');
            const endIndex = expression.indexOf(')', startIndex);
            const subExpression = expression.slice(startIndex + 1, endIndex);
            const subResult = evaluateExpression(subExpression);
            expression = expression.slice(0, startIndex) + subResult + expression.slice(endIndex + 1);
        }

        // 處理指數運算
        const powerRegex = /(\d+(\.\d+)?)\^(\d+(\.\d+)?)/;
        while (expression.match(powerRegex)) {
            expression = expression.replace(powerRegex, (match, base, _, exponent) => {
                return Math.pow(parseFloat(base), parseFloat(exponent));
            });
        }

        // 處理乘除運算
        expression = expression.replace(/(\d+(\.\d+)?)\*(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) * parseFloat(num2);
        });
        expression = expression.replace(/(\d+(\.\d+)?)\/(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) / parseFloat(num2);
        });

        // 處理加減運算
        expression = expression.replace(/(\d+(\.\d+)?)\+(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) + parseFloat(num2);
        });
        expression = expression.replace(/(\d+(\.\d+)?)\-(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
            return parseFloat(num1) - parseFloat(num2);
        });

        display.value = expression;
    } catch (error) {
        display.value = "Error";
    }
}

function evaluateExpression(expression) {
    // 遞歸地計算括號內的表達式
    let result = expression;
    let newExpression = expression;
    while (newExpression.includes('^')) {
        const match = newExpression.match(/(\d+(\.\d+)?)\^(\d+(\.\d+)?)/);
        if (match) {
            const base = parseFloat(match[1]);
            const exponent = parseFloat(match[3]);
            const subResult = Math.pow(base, exponent);
            newExpression = newExpression.replace(match[0], subResult);
        }
    }
    // 遞歸地計算括號內的表達式
    while (result.includes('(')) {
        const startIndex = result.lastIndexOf('(');
        const endIndex = result.indexOf(')', startIndex);
        const subExpression = result.slice(startIndex + 1, endIndex);
        const subResult = evaluateExpression(subExpression);
        result = result.slice(0, startIndex) + subResult + result.slice(endIndex + 1);
    }
    // 計算乘除運算
    result = result.replace(/(\d+(\.\d+)?)\*(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) * parseFloat(num2);
    });
    result = result.replace(/(\d+(\.\d+)?)\/(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) / parseFloat(num2);
    });
    // 計算加減運算
    result = result.replace(/(\d+(\.\d+)?)\+(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) + parseFloat(num2);
    });
    result = result.replace(/(\d+(\.\d+)?)\-(\d+(\.\d+)?)/g, (match, num1, _, num2) => {
        return parseFloat(num1) - parseFloat(num2);
    });
    return result;
}