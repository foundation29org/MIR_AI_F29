/**
 * Script unificado para probar múltiples modelos de IA en el examen MIR 2026.
 * Soporta: Azure OpenAI, OpenAI, Google Gemini, Anthropic Claude
 * 
 * Uso: node src/MIR_qna_multimodel.js [modelo]
 * Modelos disponibles: gpt5mini, o3, claude45sonnet, gemini3pro, gemini3flash
 */

const xlsx = require('xlsx');
const fs = require('fs');
const path = require('path');
const { ChatOpenAI } = require("@langchain/openai");
const { HumanMessage } = require("@langchain/core/messages");
const { GoogleGenAI } = require("@google/genai");
const Anthropic = require("@anthropic-ai/sdk");
const { config, validateConfig } = require('./config');

// Inicializar clientes
const googleAI = new GoogleGenAI({ apiKey: config.GOOGLE_API_KEY });

// Cliente de Anthropic Claude (API directa)
const anthropicClient = new Anthropic({ apiKey: config.ANTHROPIC_API_KEY });

// Prompt templates
const PROMPT_TEMPLATE = `Behave like a hypotethical doctor who has to answer the following question. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is:
{description}`;

const PROMPT_TEMPLATE_WITH_IMAGE = `Behave like a hypotethical doctor who has to answer the following question. Analyze the provided image carefully as it contains crucial information for answering. You have to indicate only a number 1-4 with the correct answer. Don't output anything different than 1-4 please. The question is:
{description}`;

// Definición de modelos disponibles
const MODEL_CONFIGS = {
  // Azure OpenAI (foundation29-ai endpoint)
  gpt5mini: {
    type: 'azure',
    model: "gpt-5-mini",
    deployment: "gpt-5-mini",
  },
  o3: {
    type: 'azure',
    model: "o3",
    deployment: "o3",
  },
  
  // Azure OpenAI GPT-5.2 (nav29sweden endpoint)
  gpt52: {
    type: 'azure-sweden',
    model: "gpt-5.2",
    deployment: "gpt-5.2",
  },
  
  // Anthropic Claude (API directa)
  claude4sonnet: {
    type: 'anthropic',
    model: "claude-sonnet-4-20250514",
  },
  claude45sonnet: {
    type: 'anthropic',
    model: "claude-sonnet-4-5-20250929",
  },
  claude45opus: {
    type: 'anthropic',
    model: "claude-opus-4-5-20251101",
  },
  claude35sonnet: {
    type: 'anthropic',
    model: "claude-3-5-sonnet-20241022",
  },
  
  // Google Gemini
  gemini3pro: {
    type: 'google',
    model: "gemini-3-pro-preview",
  },
  gemini3flash: {
    type: 'google',
    model: "gemini-3-flash-preview",
  },
  gemini25pro: {
    type: 'google',
    model: "gemini-2.5-pro",
  },
  gemini25flash: {
    type: 'google',
    model: "gemini-2.5-flash",
  },
};

// Crear modelo Azure OpenAI (LangChain) - foundation29-ai endpoint
function createAzureModel(deployment) {
  return new ChatOpenAI({
    modelName: deployment,
    azure: true,
    azureOpenAIApiKey: config.O_A_K_GPT5MINI,
    azureOpenAIApiVersion: config.OPENAI_API_VERSION,
    azureOpenAIEndpoint: config.AZURE_OPENAI_ENDPOINT,
    azureOpenAIApiDeploymentName: deployment,
    timeout: 140000,
  });
}

// Crear modelo Azure OpenAI Sweden (LangChain) - nav29sweden endpoint
// GPT-5.2 con reasoning_effort: high
function createAzureSwedenModel(deployment) {
  return new ChatOpenAI({
    modelName: deployment,
    azure: true,
    azureOpenAIApiKey: config.AZURE_GPT52_KEY,
    azureOpenAIApiVersion: config.OPENAI_API_VERSION,
    azureOpenAIEndpoint: config.AZURE_GPT52_ENDPOINT,
    azureOpenAIApiDeploymentName: deployment,
    timeout: 300000, // 5 minutos para reasoning
    modelKwargs: {
      reasoning_effort: "high",
    },
  });
}

// Función para codificar imagen en base64
function encodeImage(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  return imageBuffer.toString('base64');
}

// Función para obtener el tipo MIME de la imagen
function getImageMimeType(imagePath) {
  const ext = path.extname(imagePath).toLowerCase();
  const mimeTypes = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
  };
  return mimeTypes[ext] || 'image/png';
}

// Extraer número 1-4 de respuesta (o convertir letra A-D a número)
function extractAnswer(text) {
  const trimmed = text.trim();
  
  // Primero intentar encontrar número 1-4
  const numMatch = trimmed.match(/[1-4]/);
  if (numMatch) return numMatch[0];
  
  // Si no hay número, buscar letra A-D y convertir
  const letterMatch = trimmed.toUpperCase().match(/[A-D]/);
  if (letterMatch) {
    const letterToNum = { 'A': '1', 'B': '2', 'C': '3', 'D': '4' };
    return letterToNum[letterMatch[0]];
  }
  
  return trimmed;
}

// Azure OpenAI (LangChain)
async function askAzureModel(model, description, imagePath = null) {
  let prompt;
  let message;
  
  if (imagePath && fs.existsSync(imagePath)) {
    prompt = PROMPT_TEMPLATE_WITH_IMAGE.replace('{description}', description);
    const base64Image = encodeImage(imagePath);
    const mimeType = getImageMimeType(imagePath);
    
    message = new HumanMessage({
      content: [
        { type: "text", text: prompt },
        {
          type: "image_url",
          image_url: {
            url: `data:${mimeType};base64,${base64Image}`,
          },
        },
      ],
    });
  } else {
    prompt = PROMPT_TEMPLATE.replace('{description}', description);
    message = new HumanMessage({ content: prompt });
  }
  
  const response = await model.invoke([message]);
  return extractAnswer(response.content);
}

// Anthropic Claude (API directa)
async function askAnthropicModel(modelName, description, imagePath = null) {
  let prompt;
  let content;
  
  if (imagePath && fs.existsSync(imagePath)) {
    prompt = PROMPT_TEMPLATE_WITH_IMAGE.replace('{description}', description);
    const base64Image = encodeImage(imagePath);
    const mimeType = getImageMimeType(imagePath);
    
    content = [
      {
        type: "image",
        source: {
          type: "base64",
          media_type: mimeType,
          data: base64Image,
        },
      },
      { type: "text", text: prompt },
    ];
  } else {
    prompt = PROMPT_TEMPLATE.replace('{description}', description);
    content = [{ type: "text", text: prompt }];
  }
  
  const response = await anthropicClient.messages.create({
    model: modelName,
    max_tokens: 100,
    messages: [{ role: "user", content: content }],
  });
  
  return extractAnswer(response.content[0].text);
}

// Google Gemini (SDK oficial)
async function askGoogleModel(modelName, description, imagePath = null, verbose = false) {
  let prompt;
  let contents;
  
  if (imagePath && fs.existsSync(imagePath)) {
    prompt = PROMPT_TEMPLATE_WITH_IMAGE.replace('{description}', description);
    const base64Image = encodeImage(imagePath);
    const mimeType = getImageMimeType(imagePath);
    const imageSize = fs.statSync(imagePath).size;
    
    if (verbose) {
      console.log(`   📷 Gemini imagen: ${path.basename(imagePath)}, ${mimeType}, ${(imageSize/1024).toFixed(1)}KB, base64: ${base64Image.length} chars`);
    }
    
    contents = [
      {
        role: "user",
        parts: [
          { text: prompt },
          {
            inlineData: {
              mimeType: mimeType,
              data: base64Image,
            },
          },
        ],
      },
    ];
  } else {
    prompt = PROMPT_TEMPLATE.replace('{description}', description);
    contents = prompt;
  }
  
  const response = await googleAI.models.generateContent({
    model: modelName,
    contents: contents,
    config: {
      thinkingConfig: {
        thinkingLevel: "low",
      },
    },
  });
  
  const rawText = response.text;
  if (verbose) {
    console.log(`   📝 Gemini raw response: "${rawText.substring(0, 100)}..."`);
  }
  
  return extractAnswer(rawText);
}

// Función para parsear las referencias de imagen del Excel
function parseImageRefs(imageRefsStr) {
  if (!imageRefsStr || imageRefsStr === '' || imageRefsStr === 'null' || imageRefsStr === 'undefined') {
    return [];
  }
  const refs = imageRefsStr.toString()
    .split(/[,;]/)
    .map(ref => ref.trim())
    .filter(ref => ref !== '')
    .map(ref => ref.replace(/[A-Za-z]/g, ''));
  
  return [...new Set(refs)];
}

// Función principal
async function main() {
  const modelName = process.argv[2] || 'gpt5mini';
  const verbose = process.argv.includes('--verbose') || process.argv.includes('-v');
  
  if (!MODEL_CONFIGS[modelName]) {
    console.error(`Modelo "${modelName}" no disponible.`);
    console.error(`Modelos disponibles: ${Object.keys(MODEL_CONFIGS).join(', ')}`);
    process.exit(1);
  }
  
  const modelConfig = MODEL_CONFIGS[modelName];
  
  // Validar credenciales según el tipo de modelo
  const requiredKeys = {
    azure: ['O_A_K_GPT5MINI'],
    'azure-sweden': ['AZURE_GPT52_KEY'],
    google: ['GOOGLE_API_KEY'],
    anthropic: ['ANTHROPIC_API_KEY'],
  };
  validateConfig(requiredKeys[modelConfig.type]);
  
  console.log(`\n🏥 MIR 2026 - Evaluación con modelo: ${modelName} (${modelConfig.model})`);
  console.log('='.repeat(60));
  
  // Crear modelo si es Azure
  let azureModel = null;
  if (modelConfig.type === 'azure') {
    azureModel = createAzureModel(modelConfig.deployment);
  } else if (modelConfig.type === 'azure-sweden') {
    azureModel = createAzureSwedenModel(modelConfig.deployment);
  }
  
  // Leer el Excel
  const excelPath = path.join(__dirname, '..', 'data', 'MIR26.xlsx');
  const workbook = xlsx.readFile(excelPath);
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  const data = xlsx.utils.sheet_to_json(worksheet);
  
  console.log(`📊 Cargadas ${data.length} preguntas del examen\n`);
  
  const resultColumn = `answer_${modelName}`;
  const imagesDir = path.join(__dirname, '..', 'images', '26');
  
  let processed = 0;
  let errors = 0;
  let withImages = 0;
  
  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const qnum = row.qnum || (i + 1);
    const description = row.Description;
    const imageRefs = parseImageRefs(row.image_refs);
    
    if (row[resultColumn] && row[resultColumn] !== 'ERROR') {
      console.log(`⏭️  Pregunta ${qnum}: Ya respondida`);
      continue;
    }
    
    console.log(`\n📝 Pregunta ${qnum}/${data.length}`);
    if (description && description.length > 100) {
      console.log(`   ${description.substring(0, 100)}...`);
    } else {
      console.log(`   ${description}`);
    }
    
    // Determinar si hay imagen
    let imagePath = null;
    if (imageRefs.length > 0) {
      const imgNum = imageRefs[0];
      imagePath = path.join(imagesDir, `image_${imgNum}.png`);
      if (!fs.existsSync(imagePath)) {
        for (const ext of ['.jpg', '.jpeg', '.gif', '.webp']) {
          const altPath = path.join(imagesDir, `image_${imgNum}${ext}`);
          if (fs.existsSync(altPath)) {
            imagePath = altPath;
            break;
          }
        }
        if (!fs.existsSync(imagePath)) {
          console.log(`   ⚠️  Imagen no encontrada: image_${imgNum}.png`);
          imagePath = null;
        }
      }
      if (imagePath) {
        console.log(`   🖼️  Con imagen: ${path.basename(imagePath)}`);
        withImages++;
      }
    }
    
    // Intentar obtener respuesta
    let attempts = 0;
    let result = 'ERROR';
    
    while (attempts < 3) {
      try {
        switch (modelConfig.type) {
          case 'azure':
          case 'azure-sweden':
            result = await askAzureModel(azureModel, description, imagePath);
            break;
          case 'anthropic':
            result = await askAnthropicModel(modelConfig.model, description, imagePath);
            break;
          case 'google':
            result = await askGoogleModel(modelConfig.model, description, imagePath, verbose);
            break;
        }
        console.log(`   ✅ Respuesta: ${result}`);
        break;
      } catch (error) {
        attempts++;
        console.log(`   ❌ Error (intento ${attempts}/3): ${error.message}`);
        if (attempts === 3) {
          errors++;
          console.log(`   ⚠️  Máximo de intentos alcanzado`);
        } else {
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      }
    }
    
    data[i][resultColumn] = result;
    processed++;
    
    if (processed % 10 === 0) {
      saveExcel(workbook, sheetName, data, excelPath);
      console.log(`   💾 Guardado progreso (${processed} preguntas)`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  saveExcel(workbook, sheetName, data, excelPath);
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 RESUMEN');
  console.log('='.repeat(60));
  console.log(`   Total preguntas: ${data.length}`);
  console.log(`   Procesadas: ${processed}`);
  console.log(`   Con imagen: ${withImages}`);
  console.log(`   Errores: ${errors}`);
  console.log(`   Resultados guardados en columna: ${resultColumn}`);
  console.log('='.repeat(60) + '\n');
}

function saveExcel(workbook, sheetName, data, filePath) {
  const newWorksheet = xlsx.utils.json_to_sheet(data);
  workbook.Sheets[sheetName] = newWorksheet;
  xlsx.writeFile(workbook, filePath);
}

main().catch(console.error);
