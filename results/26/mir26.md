# MIR 2026 - Resultados de Evaluación

Fecha: 27/1/2026, 17:16:26

## Resultados por Modelo

| Modelo | Aciertos | Total | % Acierto | Errores |
|--------|----------|-------|-----------|--------|
| o3 | 204 | 210 | 97.14% | 0 |
| gpt52 | 204 | 210 | 97.14% | 0 |
| gpt5mini | 203 | 210 | 96.67% | 0 |
| deepseekr1 | 198 | 210 | 94.29% | 0 |
| gemini3pro | 193 | 210 | 91.90% | 0 |
| claude45sonnet | 193 | 210 | 91.90% | 0 |
| claude45opus | 191 | 210 | 90.95% | 0 |
| deepseek | 147 | 210 | 70.00% | 0 |

## Ranking

1. **o3**: 97.14% (204/210)
2. **gpt52**: 97.14% (204/210)
3. **gpt5mini**: 96.67% (203/210)
4. **deepseekr1**: 94.29% (198/210)
5. **gemini3pro**: 91.9% (193/210)
6. **claude45sonnet**: 91.9% (193/210)
7. **claude45opus**: 90.95% (191/210)
8. **deepseek**: 70% (147/210)

## Desglose por Tipo de Pregunta

| Modelo | Con Imagen | Sin Imagen |
|--------|------------|------------|
| gpt5mini | 23/25 (92.0%) | 180/185 (97.3%) |
| o3 | 23/25 (92.0%) | 181/185 (97.8%) |
| gemini3pro | 16/25 (64.0%) | 177/185 (95.7%) |
| claude45sonnet | 15/25 (60.0%) | 178/185 (96.2%) |
| claude45opus | 13/25 (52.0%) | 178/185 (96.2%) |
| gpt52 | 24/25 (96.0%) | 180/185 (97.3%) |
| deepseek | 7/25 (28.0%) | 140/185 (75.7%) |
| deepseekr1 | 22/25 (88.0%) | 176/185 (95.1%) |

## Preguntas Falladas por Modelo

- **gpt5mini** (7): 1, 3, 77, 128, 197, 198, 208
- **o3** (6): 3, 14, 77, 197, 198, 208
- **gemini3pro** (17): 3, 5, 6, 9, 11, 16, 18, 20, 25, 77, 111, 132, 138, 140, 172, 197, 208
- **claude45sonnet** (17): 3, 6, 7, 9, 10, 11, 13, 14, 20, 22, 77, 132, 140, 172, 197, 198, 208
- **claude45opus** (19): 3, 4, 6, 9, 10, 11, 12, 13, 14, 18, 22, 24, 77, 111, 127, 132, 138, 140, 197
- **gpt52** (6): 3, 77, 132, 142, 197, 208
- **deepseek** (63): 1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 21, 23, 24, 27, 31, 33, 36, 38, 50, 56, 58, 64, 66, 71, 73, 77, 81, 82, 91, 109, 110, 116, 118, 119, 120, 123, 124, 132, 134, 138, 140, 142, 143, 155, 156, 163, 169, 172, 176, 179, 188, 190, 192, 197, 198, 202, 207, 208
- **deepseekr1** (12): 1, 3, 11, 66, 77, 82, 128, 132, 140, 172, 197, 198

## Preguntas Falladas por TODOS los Modelos

3, 77, 197

---

## Gráficas

### Comparativa de Modelos

![Comparativa de modelos](charts/models_comparison.png)

### Rendimiento: Con Imagen vs Sin Imagen

![Comparativa con/sin imagen](charts/image_vs_text_comparison.png)

### Concordancia entre Modelos

![Heatmap de concordancia](charts/model_concordance_heatmap.png)

### Distribución de Preguntas por Especialidad

![Distribución por especialidad](charts/specialty_distribution.png)

---

### Precisión por Especialidad - Por Modelo

#### o3

![o3 por especialidad](charts/o3_by_specialty.png)

#### GPT-5.2

![GPT-5.2 por especialidad](charts/gpt52_by_specialty.png)

#### GPT-5-mini

![GPT-5-mini por especialidad](charts/gpt5mini_by_specialty.png)

#### DeepSeek-R1

![DeepSeek-R1 por especialidad](charts/deepseekr1_by_specialty.png)

#### Gemini 3 Pro

![Gemini 3 Pro por especialidad](charts/gemini3pro_by_specialty.png)

#### Claude 4.5 Sonnet

![Claude 4.5 Sonnet por especialidad](charts/claude45sonnet_by_specialty.png)

#### Claude 4.5 Opus

![Claude 4.5 Opus por especialidad](charts/claude45opus_by_specialty.png)

#### DeepSeek V3.2

![DeepSeek por especialidad](charts/deepseek_by_specialty.png)

