/**
 * Script para comparar resultados de los modelos con las respuestas oficiales
 */

const xlsx = require('xlsx');
const path = require('path');

function main() {
  // Leer correcciones oficiales
  const wbCorr = xlsx.readFile(path.join(__dirname, '..', 'data', 'Excel MIR 2026.xlsx'));
  const sheetCorr = wbCorr.Sheets['Hoja 1'];

  // Extraer respuestas correctas (PREGUNTA -> RESPUESTA)
  const correctas = {};
  for (let i = 2; i <= 220; i++) {
    const pregCell = sheetCorr['A' + i];
    const respCell = sheetCorr['B' + i];
    if (pregCell && respCell && pregCell.v) {
      correctas[String(pregCell.v)] = String(respCell.v);
    }
  }

  console.log(`\n📋 Respuestas correctas cargadas: ${Object.keys(correctas).length}`);

  // Leer Excel con resultados de modelos
  const excelPath = path.join(__dirname, '..', 'data', 'MIR26.xlsx');
  const workbook = xlsx.readFile(excelPath);
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  const data = xlsx.utils.sheet_to_json(worksheet);

  console.log(`📊 Preguntas en MIR26.xlsx: ${data.length}\n`);

  // Identificar columnas de respuestas de modelos
  const answerColumns = Object.keys(data[0] || {}).filter(col => col.startsWith('answer_'));
  console.log(`🤖 Modelos encontrados: ${answerColumns.map(c => c.replace('answer_', '')).join(', ')}\n`);

  // Contar aciertos por modelo
  const stats = {};
  answerColumns.forEach(col => {
    stats[col] = { total: 0, correct: 0, errors: 0 };
  });

  // Añadir columna de respuesta correcta y comparar
  for (let i = 0; i < data.length; i++) {
    const qnum = String(data[i].qnum || (i + 1));
    const correctAnswer = correctas[qnum];
    
    // Añadir respuesta correcta
    data[i]['correct_answer'] = correctAnswer || 'N/A';

    // Comparar cada modelo
    answerColumns.forEach(col => {
      const modelAnswer = String(data[i][col] || '');
      if (modelAnswer && modelAnswer !== 'ERROR' && modelAnswer !== '') {
        stats[col].total++;
        if (modelAnswer === correctAnswer) {
          stats[col].correct++;
        }
      } else if (modelAnswer === 'ERROR') {
        stats[col].errors++;
      }
    });
  }

  // Mostrar resultados
  console.log('='.repeat(70));
  console.log('📊 RESULTADOS POR MODELO');
  console.log('='.repeat(70));
  console.log('');
  console.log('Modelo'.padEnd(25) + 'Aciertos'.padEnd(12) + 'Total'.padEnd(10) + '% Acierto'.padEnd(12) + 'Errores');
  console.log('-'.repeat(70));

  const results = [];
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const s = stats[col];
    const percentage = s.total > 0 ? ((s.correct / s.total) * 100).toFixed(2) : '0.00';
    console.log(
      modelName.padEnd(25) + 
      String(s.correct).padEnd(12) + 
      String(s.total).padEnd(10) + 
      (percentage + '%').padEnd(12) +
      String(s.errors)
    );
    results.push({ model: modelName, correct: s.correct, total: s.total, percentage: parseFloat(percentage), errors: s.errors });
  });

  console.log('-'.repeat(70));
  console.log('');

  // Ordenar por porcentaje de aciertos
  results.sort((a, b) => b.percentage - a.percentage);
  console.log('🏆 RANKING:');
  results.forEach((r, i) => {
    console.log(`   ${i + 1}. ${r.model}: ${r.percentage}% (${r.correct}/${r.total})`);
  });
  console.log('');

  // Recopilar preguntas falladas por modelo
  const failedQuestions = {};
  answerColumns.forEach(col => {
    failedQuestions[col] = [];
  });

  for (let i = 0; i < data.length; i++) {
    const qnum = String(data[i].qnum || (i + 1));
    const correctAnswer = correctas[qnum];
    
    answerColumns.forEach(col => {
      const modelAnswer = String(data[i][col] || '');
      if (modelAnswer && modelAnswer !== 'ERROR' && modelAnswer !== '' && modelAnswer !== correctAnswer) {
        failedQuestions[col].push(qnum);
      }
    });
  }

  // Mostrar preguntas falladas
  console.log('❌ PREGUNTAS FALLADAS POR MODELO:');
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const failed = failedQuestions[col];
    console.log(`   ${modelName} (${failed.length}): ${failed.join(', ')}`);
  });
  console.log('');

  // Añadir filas al final con resumen de preguntas falladas
  const emptyRow = {};
  Object.keys(data[0]).forEach(key => emptyRow[key] = '');
  
  // Fila vacía separadora
  data.push({...emptyRow});
  
  // Fila de encabezado
  const headerRow = {...emptyRow};
  headerRow.qnum = 'RESUMEN';
  headerRow.Description = 'Preguntas falladas por modelo';
  data.push(headerRow);

  // Filas con preguntas falladas por cada modelo
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const failed = failedQuestions[col];
    const row = {...emptyRow};
    row.qnum = modelName;
    row.Description = `Falladas (${failed.length}): ${failed.join(', ')}`;
    row[col] = `${failed.length} errores`;
    data.push(row);
  });

  // Guardar Excel actualizado
  const newWorksheet = xlsx.utils.json_to_sheet(data);
  workbook.Sheets[sheetName] = newWorksheet;
  xlsx.writeFile(workbook, excelPath);

  console.log(`✅ Excel actualizado con columna 'correct_answer' y resumen de fallos\n`);
}

main();
