# MIR 2026 - Resultados de Evaluación

Fecha: 26/1/2026

## Ranking Final

| Posición | Modelo | Precisión | Aciertos/Total |
|----------|--------|-----------|----------------|
| 1 | **GPT-5.2** | 97.14% | 204/210 |
| 2 | **o3** | 95.71% | 201/210 |
| 3 | **GPT-5-mini** | 94.76% | 199/210 |
| 4 | **DeepSeek-R1** | 93.33% | 196/210 |
| 5 | **Gemini 3 Pro** | 92.38% | 194/210 |
| 6 | **Claude Opus 4.5** | 91.43% | 192/210 |
| 7 | **Claude Sonnet 4.5** | 90.95% | 191/210 |
| 8 | **DeepSeek V3.2** | 70.00% | 147/210 |

## Resultados Detallados

| Modelo | Aciertos | Total | % Acierto | Errores |
|--------|----------|-------|-----------|---------|
| gpt52 | 204 | 210 | 97.14% | 0 |
| o3 | 201 | 210 | 95.71% | 0 |
| gpt5mini | 199 | 210 | 94.76% | 0 |
| deepseekr1 | 196 | 210 | 93.33% | 0 |
| gemini3pro | 194 | 210 | 92.38% | 0 |
| claude45opus | 192 | 210 | 91.43% | 0 |
| claude45sonnet | 191 | 210 | 90.95% | 0 |
| deepseek | 147 | 210 | 70.00% | 0 |

## Desglose por Tipo de Pregunta

### Preguntas CON Imagen (25 preguntas)

| Modelo | Aciertos | Precisión |
|--------|----------|-----------|
| **gpt52** | 24/25 | 96.0% |
| o3 | 23/25 | 92.0% |
| gpt5mini | 23/25 | 92.0% |
| deepseekr1 | 22/25 | 88.0% |
| gemini3pro | 16/25 | 64.0% |
| claude45sonnet | 15/25 | 60.0% |
| claude45opus | 13/25 | 52.0% |
| deepseek | 7/25 | 28.0% |

### Preguntas SIN Imagen (185 preguntas)

| Modelo | Aciertos | Precisión |
|--------|----------|-----------|
| **gpt52** | 180/185 | 97.3% |
| claude45opus | 179/185 | 96.8% |
| o3 | 178/185 | 96.2% |
| gemini3pro | 178/185 | 96.2% |
| gpt5mini | 176/185 | 95.1% |
| claude45sonnet | 176/185 | 95.1% |
| deepseekr1 | 174/185 | 94.1% |
| deepseek | 140/185 | 75.7% |

## Observaciones Clave

### Rendimiento General
- **GPT-5.2 lidera** con 97.14%, siendo el mejor tanto en preguntas con imagen (96%) como sin imagen (97.3%)
- Los modelos de OpenAI (GPT-5.2, o3, GPT-5-mini) ocupan los 3 primeros puestos
- **DeepSeek-R1** (con razonamiento) muestra un excelente rendimiento, superando a modelos más establecidos

### Análisis de Preguntas con Imagen
- Gran disparidad entre modelos en interpretación de imágenes médicas
- **GPT-5.2** destaca con 96% de acierto en imágenes
- **Claude Opus 4.5** tiene mejor precisión en texto (96.8%) pero peor en imágenes (52%)
- **DeepSeek V3.2** tiene un rendimiento muy pobre en imágenes (28%), indicando limitaciones multimodales

### Preguntas Problemáticas
- **3 preguntas falladas por TODOS los modelos**: 3, 122 y 139
- Estas preguntas podrían ser impugnables o presentar ambigüedad

### Consistencia por Especialidad
- Mejor rendimiento global: Traumatología (100% en varios modelos)
- Mayor variabilidad: Genética, Anatomía Patológica, Hematología

## Preguntas Falladas por Modelo

| Modelo | Nº Fallos | Preguntas |
|--------|-----------|-----------|
| gpt52 | 6 | 3, 77, 122, 138, 139, 208 |
| o3 | 9 | 3, 14, 122, 132, 138, 139, 142, 198, 208 |
| gpt5mini | 11 | 1, 3, 77, 122, 128, 132, 138, 139, 142, 198, 208 |
| deepseekr1 | 14 | 1, 3, 11, 66, 77, 82, 122, 128, 138, 139, 140, 142, 172, 198 |
| gemini3pro | 16 | 3, 5, 6, 9, 11, 16, 18, 20, 25, 111, 122, 139, 140, 142, 172, 208 |
| claude45opus | 18 | 3, 4, 6, 9, 10, 11, 12, 13, 14, 18, 22, 24, 111, 122, 127, 139, 140, 142 |
| claude45sonnet | 19 | 3, 6, 7, 9, 10, 11, 13, 14, 20, 22, 77, 122, 138, 139, 140, 142, 172, 198, 208 |
| deepseek | 63 | 1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 24, 27, 31, 33, 36, 38, 50, 56, 58, 64, 66, 71, 73, 77, 81, 82, 91, 109, 110, 116, 118, 119, 120, 122, 123, 124, 134, 138, 139, 140, 142, 143, 155, 156, 163, 169, 172, 176, 179, 188, 190, 192, 198, 202, 207, 208 |

## Gráficas Generadas

Las gráficas están disponibles en `results/charts/`:

### Comparativas Generales
- `models_comparison.png` - Ranking de todos los modelos
- `image_vs_text_comparison.png` - Rendimiento con/sin imagen por modelo
- `model_concordance_heatmap.png` - Concordancia entre modelos
- `specialty_distribution.png` - Distribución de preguntas por especialidad

### Por Modelo (Precisión por Especialidad)
- `gpt52_by_specialty.png` - GPT-5.2
- `o3_by_specialty.png` - o3
- `gpt5mini_by_specialty.png` - GPT-5-mini
- `deepseekr1_by_specialty.png` - DeepSeek-R1
- `gemini3pro_by_specialty.png` - Gemini 3 Pro
- `claude45opus_by_specialty.png` - Claude Opus 4.5
- `claude45sonnet_by_specialty.png` - Claude Sonnet 4.5
- `deepseek_by_specialty.png` - DeepSeek V3.2

## Vista Previa de Gráficas

### Comparativa de Modelos
![Comparativa de modelos](charts/models_comparison.png)

### Rendimiento Con/Sin Imagen
![Con vs Sin Imagen](charts/image_vs_text_comparison.png)

### Concordancia entre Modelos
![Heatmap concordancia](charts/model_concordance_heatmap.png)

### Distribución por Especialidad
![Distribución especialidades](charts/specialty_distribution.png)
