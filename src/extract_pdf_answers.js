/**
 * Script para extraer las respuestas oficiales del PDF de soluciones
 * y compararlas con las respuestas del Excel MIR 2026
 */

const fs = require('fs');
const { PDFParse } = require('pdf-parse');
const xlsx = require('xlsx');
const path = require('path');

async function main() {
  console.log('Leyendo PDF...');
  const pdfPath = path.join(__dirname, '..', 'data', 'solucion.pdf');
  const parser = new PDFParse(pdfPath);
  const pages = await parser.parse();
  
  // Unir texto de todas las páginas
  let text = '';
  for (const page of pages) {
    text += page.text + '\n';
  }
  
  console.log('PDF cargado, extrayendo respuestas...');
  console.log('Longitud del texto:', text.length);
  
  // Guardar texto completo para debug
  fs.writeFileSync(path.join(__dirname, '..', 'data', 'pdf_text_full.txt'), text);
  console.log('Texto del PDF guardado en data/pdf_text_full.txt');
  
  // Extraer respuestas usando múltiples patrones
  const respuestasPDF = {};
  
  // Patrón 1: buscar "N.º de pregunta en el examen: X" seguido de "Respuesta correcta: Y"
  const regex1 = /N\.º de pregunta en el examen:\s*(\d+)[\s\S]*?Respuesta correcta:\s*(\d+)/g;
  let match;
  while ((match = regex1.exec(text)) !== null) {
    respuestasPDF[match[1]] = match[2];
  }
  
  // Si no funciona el primer patrón, probar otro
  if (Object.keys(respuestasPDF).length === 0) {
    // Patrón alternativo: líneas separadas
    const lineas = text.split('\n');
    let preguntaActual = null;
    
    for (let i = 0; i < lineas.length; i++) {
      const linea = lineas[i].trim();
      
      // Buscar número de pregunta
      const matchPregunta = linea.match(/N\.º de pregunta en el examen:\s*(\d+)/);
      if (matchPregunta) {
        preguntaActual = matchPregunta[1];
      }
      
      // Buscar respuesta correcta
      const matchRespuesta = linea.match(/Respuesta correcta:\s*(\d+)/);
      if (matchRespuesta && preguntaActual) {
        respuestasPDF[preguntaActual] = matchRespuesta[1];
        preguntaActual = null;
      }
    }
  }
  
  console.log(`\nRespuestas extraídas del PDF: ${Object.keys(respuestasPDF).length}`);
  
  // Leer respuestas del Excel
  console.log('\nLeyendo Excel MIR 2026...');
  const wb = xlsx.readFile(path.join(__dirname, '..', 'data', 'Excel MIR 2026.xlsx'));
  const sheet = wb.Sheets['Hoja 1'];
  
  const respuestasExcel = {};
  for (let i = 2; i <= 220; i++) {
    const pregCell = sheet['A' + i];
    const respCell = sheet['B' + i];
    if (pregCell && respCell) {
      respuestasExcel[String(pregCell.v)] = String(respCell.v);
    }
  }
  
  console.log(`Respuestas en Excel: ${Object.keys(respuestasExcel).length}`);
  
  // Comparar
  console.log('\n' + '='.repeat(60));
  console.log('COMPARACIÓN PDF OFICIAL vs EXCEL');
  console.log('='.repeat(60));
  
  const diferencias = [];
  const todasLasPreguntas = new Set([...Object.keys(respuestasPDF), ...Object.keys(respuestasExcel)]);
  const preguntasOrdenadas = [...todasLasPreguntas].sort((a, b) => parseInt(a) - parseInt(b));
  
  for (const pregunta of preguntasOrdenadas) {
    const respPDF = respuestasPDF[pregunta];
    const respExcel = respuestasExcel[pregunta];
    
    if (!respPDF) {
      console.log(`Pregunta ${pregunta}: NO ENCONTRADA EN PDF (Excel: ${respExcel})`);
    } else if (!respExcel) {
      console.log(`Pregunta ${pregunta}: NO ENCONTRADA EN EXCEL (PDF: ${respPDF})`);
    } else if (respPDF !== respExcel) {
      diferencias.push({
        pregunta,
        pdf: respPDF,
        excel: respExcel
      });
    }
  }
  
  if (diferencias.length > 0) {
    console.log('\n❌ DIFERENCIAS ENCONTRADAS:');
    console.log('-'.repeat(40));
    diferencias.forEach(d => {
      console.log(`Pregunta ${d.pregunta}: PDF=${d.pdf}, Excel=${d.excel}`);
    });
    console.log(`\nTotal diferencias: ${diferencias.length}`);
  } else {
    console.log('\n✅ No hay diferencias entre PDF y Excel');
  }
  
  // Guardar resultado
  const resultado = {
    respuestasPDF,
    respuestasExcel,
    diferencias,
    totalPDF: Object.keys(respuestasPDF).length,
    totalExcel: Object.keys(respuestasExcel).length
  };
  
  fs.writeFileSync(
    path.join(__dirname, '..', 'data', 'comparacion_pdf_excel.json'),
    JSON.stringify(resultado, null, 2)
  );
  console.log('\nResultado guardado en data/comparacion_pdf_excel.json');
}

main().catch(console.error);
