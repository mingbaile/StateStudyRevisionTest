const parser = require('@solidity-parser/parser');
const fs = require('fs');
const path = require('path');

const filePath = process.argv[2];

const inputDir = process.argv[3];

const outputFolder = process.argv[4];

const solCode = fs.readFileSync(filePath, 'utf-8');

try {
    const ast = parser.parse(solCode, { loc: true });

    const relativeFilePath = path.relative(inputDir, filePath);

    const dirPath = path.dirname(relativeFilePath);

    const finalOutputDir = path.join(outputFolder, dirPath);

    if (!fs.existsSync(finalOutputDir)) {
        fs.mkdirSync(finalOutputDir, { recursive: true });
    }

    const fileName = path.basename(filePath, '.sol');
    const outputFilePath = path.join(finalOutputDir, `${fileName}_ast.json`);

    fs.writeFileSync(outputFilePath, JSON.stringify(ast, null, 2), 'utf-8');

    console.log(`AST for ${filePath} has been saved to: ${outputFilePath}`);
} catch (error) {
    if (error instanceof parser.ParserError) {
        console.error("Parsing error:", error.errors);
    } else {
        console.error('Unexpected error:', error);
    }
    process.exit(1);
}
