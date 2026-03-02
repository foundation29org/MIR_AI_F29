# MIR 2026 - Comparativa con Resultados Oficiales

Fecha: 2/3/2026

## Contexto del Examen Oficial

- **Base del examen**: 200 preguntas (preguntas 1-200)
- **Preguntas de reserva**: 201-210 (sustituyen a las impugnadas por orden)
- **Preguntas anuladas**: 7 (13, 50, 64, 139, 142, 161, 208)
- **Mejor estudiante oficial**: **188 aciertos** de 200 preguntas (94%)

## Metodología de Comparación

Los modelos fueron evaluados sobre **203 preguntas válidas** (210 totales menos 7 anuladas). Para comparar con el examen oficial de 200 preguntas:

1. **Equivalencia de puntuación**: Se escala la puntuación de cada modelo a base 200: `equivalentes_200 = aciertos × (200/203)`
2. **Umbral para superar al mejor estudiante**: Un modelo necesita ≥191 aciertos en 203 para superar 188/200 (ya que 188 × 203/200 ≈ 190,8)

---

## Comparativa: Modelos vs. Mejor Estudiante (188/200)

| Modelo | Aciertos (203) | % sobre 203 | Equiv. 200 preg. | vs. Mejor Estudiante |
|--------|----------------|-------------|------------------|----------------------|
| **gpt52** | 200 | 98,52% | 197 | **+9** (supera) |
| **o3** | 199 | 98,03% | 196 | **+8** (supera) |
| **OE** | 199 | 98,03% | 196 | **+8** (supera) |
| **gpt5mini** | 198 | 97,54% | 195 | **+7** (supera) |
| **deepseekr1** | 192 | 94,58% | 189 | **+1** (supera) |
| **claude45sonnet** | 189 | 93,10% | 186 | **-2** (no supera) |
| **gemini3pro** | 188 | 92,61% | 185 | **-3** (no supera) |
| **claude45opus** | 186 | 91,63% | 183 | **-5** (no supera) |
| **deepseek** | 146 | 71,92% | 144 | **-44** (no supera) |

---

## Conclusiones

### Cinco modelos superan al mejor estudiante; cuatro quedan por debajo

1. **GPT-5.2** obtendría el nº 1 con **197 equivalentes** sobre 200, 9 puntos por encima del mejor humano.
2. **o3** y **Open Evidence** empatarían en segundo lugar con **196 equivalentes**, 8 puntos por encima.
3. **GPT-5-mini** con **195 equivalentes**, 7 puntos por encima.
4. **DeepSeek-R1** con **189 equivalentes**, 1 punto por encima (el que más se acerca al umbral).
5. **Claude 4.5 Sonnet**, **Gemini 3 Pro**, **Claude 4.5 Opus** y **DeepSeek V3.2** quedan por debajo del mejor estudiante.

### Resumen visual

```
Mejor estudiante: 188/200 █████████████████████░░░ 94,0%
DeepSeek:        144 eq. ███████████████░░░░░░░░░ 72,0%
Claude 4.5 Opus: 183 eq. ████████████████████░░░░ 91,5%
Gemini 3 Pro:    185 eq. ████████████████████▓░░░ 92,5%
Claude 4.5 Sonnet:186 eq. ████████████████████▓▓░░ 93,0%
DeepSeek-R1:     189 eq. █████████████████████░░░ 94,5% (supera +1)
GPT-5-mini:      195 eq. ███████████████████████░ 97,5%
o3 / OE:         196 eq. ███████████████████████▓ 98,0%
GPT-5.2:         197 eq. ████████████████████████ 98,5%
```

---

## Notas metodológicas

- Las **preguntas impugnadas** en el examen oficial se sustituyen por las de reserva (201-210) por orden. Los modelos fueron evaluados sobre el conjunto de 203 preguntas válidas tras las anulaciones.
- La equivalencia a 200 preguntas es una **proyección proporcional** para facilitar la comparación con el baremo oficial.
- El mejor estudiante con 188 aciertos representa el **techo humano** conocido en esta convocatoria.
