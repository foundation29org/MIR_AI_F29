/**
 * Script para comparar resultados de los modelos con las respuestas oficiales
 * Los resultados se guardan en results/26/mir26.md (NO modifica el Excel)
 */

const xlsx = require('xlsx');
const fs = require('fs');
const path = require('path');

function main() {
  // Leer correcciones oficiales
  const wbCorr = xlsx.readFile(path.join(__dirname, '..', 'data', '26', 'Excel MIR 2026.xlsx'));
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

  // Contar aciertos por modelo (total y separado por con/sin imagen)
  const stats = {};
  answerColumns.forEach(col => {
    stats[col] = { 
      total: 0, correct: 0, errors: 0,
      withImage: { total: 0, correct: 0 },
      withoutImage: { total: 0, correct: 0 }
    };
  });

  // Comparar respuestas
  for (let i = 0; i < data.length; i++) {
    const qnum = String(data[i].qnum || (i + 1));
    const correctAnswer = correctas[qnum];
    const hasImage = data[i].image_refs && data[i].image_refs !== '';

    // Comparar cada modelo
    answerColumns.forEach(col => {
      const modelAnswer = String(data[i][col] || '');
      if (modelAnswer && modelAnswer !== 'ERROR' && modelAnswer !== '') {
        stats[col].total++;
        const imageCategory = hasImage ? 'withImage' : 'withoutImage';
        stats[col][imageCategory].total++;
        
        if (modelAnswer === correctAnswer) {
          stats[col].correct++;
          stats[col][imageCategory].correct++;
        }
      } else if (modelAnswer === 'ERROR') {
        stats[col].errors++;
      }
    });
  }

  // Construir output para consola y archivo
  let output = '';
  
  output += `# MIR 2026 - Resultados de Evaluación\n\n`;
  output += `Fecha: ${new Date().toLocaleString('es-ES')}\n\n`;

  output += '## Resultados por Modelo\n\n';
  output += '| Modelo | Aciertos | Total | % Acierto | Errores |\n';
  output += '|--------|----------|-------|-----------|--------|\n';

  const results = [];
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const s = stats[col];
    const percentage = s.total > 0 ? ((s.correct / s.total) * 100).toFixed(2) : '0.00';
    output += `| ${modelName} | ${s.correct} | ${s.total} | ${percentage}% | ${s.errors} |\n`;
    results.push({ model: modelName, correct: s.correct, total: s.total, percentage: parseFloat(percentage), errors: s.errors });
  });

  output += '\n';

  // Ordenar por porcentaje de aciertos
  results.sort((a, b) => b.percentage - a.percentage);
  output += '## Ranking\n\n';
  results.forEach((r, i) => {
    output += `${i + 1}. **${r.model}**: ${r.percentage}% (${r.correct}/${r.total})\n`;
  });
  output += '\n';

  // Desglose por tipo (con/sin imagen)
  output += '## Desglose por Tipo de Pregunta\n\n';
  output += '| Modelo | Con Imagen | Sin Imagen |\n';
  output += '|--------|------------|------------|\n';
  
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const s = stats[col];
    const withImg = s.withImage;
    const withoutImg = s.withoutImage;
    const withImgPct = withImg.total > 0 ? ((withImg.correct / withImg.total) * 100).toFixed(1) : '0.0';
    const withoutImgPct = withoutImg.total > 0 ? ((withoutImg.correct / withoutImg.total) * 100).toFixed(1) : '0.0';
    
    output += `| ${modelName} | ${withImg.correct}/${withImg.total} (${withImgPct}%) | ${withoutImg.correct}/${withoutImg.total} (${withoutImgPct}%) |\n`;
  });
  output += '\n';

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

  // Preguntas falladas
  output += '## Preguntas Falladas por Modelo\n\n';
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const failed = failedQuestions[col];
    output += `- **${modelName}** (${failed.length}): ${failed.join(', ')}\n`;
  });
  output += '\n';

  // Preguntas falladas por todos los modelos
  const allFailed = answerColumns.reduce((acc, col) => {
    if (acc === null) return new Set(failedQuestions[col]);
    return new Set([...acc].filter(q => failedQuestions[col].includes(q)));
  }, null);
  
  if (allFailed && allFailed.size > 0) {
    output += `## Preguntas Falladas por TODOS los Modelos\n\n`;
    output += `${[...allFailed].sort((a, b) => parseInt(a) - parseInt(b)).join(', ')}\n\n`;
  }

  // Guardar en archivo markdown
  const resultsPath = path.join(__dirname, '..', 'results/26/mir26.md');
  fs.writeFileSync(resultsPath, output);

  // Mostrar en consola (formato simplificado)
  console.log('='.repeat(70));
  console.log('📊 RESULTADOS POR MODELO');
  console.log('='.repeat(70));
  console.log('');
  console.log('Modelo'.padEnd(25) + 'Aciertos'.padEnd(12) + 'Total'.padEnd(10) + '% Acierto'.padEnd(12) + 'Errores');
  console.log('-'.repeat(70));

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
  });

  console.log('-'.repeat(70));
  console.log('');

  console.log('🏆 RANKING:');
  results.forEach((r, i) => {
    console.log(`   ${i + 1}. ${r.model}: ${r.percentage}% (${r.correct}/${r.total})`);
  });
  console.log('');

  console.log('📊 DESGLOSE POR TIPO DE PREGUNTA:');
  console.log('-'.repeat(70));
  console.log('Modelo'.padEnd(20) + 'Con Imagen'.padEnd(18) + 'Sin Imagen'.padEnd(18));
  console.log('-'.repeat(70));
  
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const s = stats[col];
    const withImg = s.withImage;
    const withoutImg = s.withoutImage;
    const withImgPct = withImg.total > 0 ? ((withImg.correct / withImg.total) * 100).toFixed(1) : '0.0';
    const withoutImgPct = withoutImg.total > 0 ? ((withoutImg.correct / withoutImg.total) * 100).toFixed(1) : '0.0';
    
    console.log(
      modelName.padEnd(20) + 
      `${withImg.correct}/${withImg.total} (${withImgPct}%)`.padEnd(18) +
      `${withoutImg.correct}/${withoutImg.total} (${withoutImgPct}%)`.padEnd(18)
    );
  });
  console.log('-'.repeat(70));
  console.log('');

  console.log('❌ PREGUNTAS FALLADAS POR MODELO:');
  answerColumns.forEach(col => {
    const modelName = col.replace('answer_', '');
    const failed = failedQuestions[col];
    console.log(`   ${modelName} (${failed.length}): ${failed.join(', ')}`);
  });
  console.log('');

  console.log(`✅ Resultados guardados en: results/26/mir26.md`);
  console.log(`ℹ️  El Excel NO ha sido modificado\n`);
}

main();
