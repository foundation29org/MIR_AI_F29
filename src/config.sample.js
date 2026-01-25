/**
 * Configuración de credenciales para los modelos de IA.
 * Copia este archivo a config.js y rellena con tus credenciales.
 */

const config = {
  // Azure OpenAI GPT-5 Mini
  O_A_K_GPT5MINI: '<TU_AZURE_OPENAI_API_KEY>',
  OPENAI_API_VERSION: '2024-12-01-preview',
  AZURE_OPENAI_ENDPOINT: 'https://tu-endpoint.cognitiveservices.azure.com/',
  
  // Google API Key
  GOOGLE_API_KEY: '<TU_GOOGLE_API_KEY>',
  
  // Anthropic Claude (API directa)
  ANTHROPIC_API_KEY: '<TU_ANTHROPIC_API_KEY>',
};

// Validar que las credenciales necesarias estén configuradas
function validateConfig(requiredKeys) {
  const missing = requiredKeys.filter(key => !config[key] || config[key].startsWith('<'));
  if (missing.length > 0) {
    console.error(`❌ Faltan las siguientes credenciales en config.js: ${missing.join(', ')}`);
    console.error('   Por favor, copia config.sample.js a config.js y rellena con tus credenciales.');
    process.exit(1);
  }
}

module.exports = { config, validateConfig };
