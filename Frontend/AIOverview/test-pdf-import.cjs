const pdfMod = require('pdf-parse');
console.log('Module keys:', Object.keys(pdfMod).slice(0, 10));
console.log('PDFParse type:', typeof pdfMod.PDFParse);

if (pdfMod.PDFParse) {
  console.log('PDFParse function name:', pdfMod.PDFParse.name);
  console.log('Can assign to pdfParse:', typeof pdfMod.PDFParse);
}
