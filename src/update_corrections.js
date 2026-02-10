/**
 * Script para actualizar Correcion_academia.xlsx con respuestas oficiales del Ministerio
 */

const xlsx = require('xlsx');
const path = require('path');

// Respuestas oficiales del PDF del Ministerio
// Preguntas anuladas (sin respuesta): 13, 50, 64, 139, 142, 161, 208
const oficiales = {
  1: '1', 2: '2', 3: '4', 4: '4', 5: '2', 6: '3', 7: '2', 8: '4', 9: '4', 10: '1',
  11: '2', 12: '1', 13: '', 14: '3', 15: '1', 16: '3', 17: '3', 18: '4', 19: '2', 20: '2',
  21: '2', 22: '3', 23: '2', 24: '1', 25: '3', 26: '1', 27: '2', 28: '4', 29: '1', 30: '4',
  31: '3', 32: '3', 33: '2', 34: '2', 35: '3', 36: '4', 37: '4', 38: '1', 39: '3', 40: '1',
  41: '4', 42: '1', 43: '2', 44: '2', 45: '2', 46: '2', 47: '4', 48: '3', 49: '3', 50: '',
  51: '1', 52: '3', 53: '3', 54: '3', 55: '1', 56: '1', 57: '1', 58: '1', 59: '2', 60: '2',
  61: '3', 62: '2', 63: '2', 64: '', 65: '3', 66: '3', 67: '3', 68: '1', 69: '2', 70: '2',
  71: '2', 72: '2', 73: '2', 74: '1', 75: '3', 76: '3', 77: '1', 78: '4', 79: '1', 80: '4',
  81: '3', 82: '4', 83: '2', 84: '1', 85: '4', 86: '1', 87: '2', 88: '2', 89: '2', 90: '3',
  91: '1', 92: '3', 93: '4', 94: '3', 95: '3', 96: '2', 97: '2', 98: '1', 99: '2', 100: '3',
  101: '3', 102: '1', 103: '3', 104: '3', 105: '3', 106: '2', 107: '3', 108: '1', 109: '3', 110: '3',
  111: '2', 112: '3', 113: '3', 114: '4', 115: '2', 116: '4', 117: '3', 118: '2', 119: '1', 120: '1',
  121: '3', 122: '2', 123: '2', 124: '2', 125: '3', 126: '2', 127: '3', 128: '2', 129: '3', 130: '3',
  131: '2', 132: '2', 133: '3', 134: '2', 135: '3', 136: '2', 137: '4', 138: '2', 139: '', 140: '4',
  141: '1', 142: '', 143: '1', 144: '4', 145: '3', 146: '3', 147: '2', 148: '3', 149: '2', 150: '2',
  151: '2', 152: '3', 153: '3', 154: '4', 155: '2', 156: '1', 157: '4', 158: '2', 159: '3', 160: '1',
  161: '', 162: '1', 163: '3', 164: '3', 165: '1', 166: '1', 167: '4', 168: '3', 169: '2', 170: '2',
  171: '1', 172: '2', 173: '4', 174: '3', 175: '2', 176: '1', 177: '4', 178: '4', 179: '2', 180: '3',
  181: '2', 182: '3', 183: '4', 184: '4', 185: '2', 186: '4', 187: '4', 188: '3', 189: '3', 190: '2',
  191: '4', 192: '4', 193: '3', 194: '3', 195: '4', 196: '1', 197: '3', 198: '1', 199: '2', 200: '4',
  201: '3', 202: '1', 203: '1', 204: '3', 205: '2', 206: '3', 207: '1', 208: '', 209: '2', 210: '3'
};

const excelPath = path.join(__dirname, '..', 'data/26/Correcion_academia.xlsx');

// Leer el Excel existente
const workbook = xlsx.readFile(excelPath);
const sheetName = 'Hoja 1';
const worksheet = workbook.Sheets[sheetName];

console.log('Actualizando respuestas con valores oficiales del Ministerio...\n');

let cambios = 0;
const anuladas = [];

// Actualizar cada respuesta
for (let i = 2; i <= 211; i++) {
  const pregCell = worksheet['A' + i];
  if (pregCell && pregCell.v) {
    const pregNum = String(pregCell.v);
    const respOficial = oficiales[parseInt(pregNum)];
    const respActual = worksheet['B' + i] ? String(worksheet['B' + i].v) : '';
    
    if (respOficial === '') {
      // Pregunta anulada
      anuladas.push(pregNum);
      if (respActual !== '') {
        worksheet['B' + i] = { t: 's', v: '' };
        console.log(`Pregunta ${pregNum}: "${respActual}" -> "" (ANULADA)`);
        cambios++;
      }
    } else if (respActual !== respOficial) {
      worksheet['B' + i] = { t: 's', v: respOficial };
      console.log(`Pregunta ${pregNum}: "${respActual}" -> "${respOficial}"`);
      cambios++;
    }
  }
}

// Guardar el archivo
xlsx.writeFile(workbook, excelPath);

console.log('\n' + '='.repeat(50));
console.log(`Total cambios realizados: ${cambios}`);
console.log(`Preguntas anuladas: ${anuladas.join(', ')}`);
console.log(`Archivo actualizado: ${excelPath}`);
