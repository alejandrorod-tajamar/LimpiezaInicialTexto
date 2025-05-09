**Práctica: Lematización para Mejora de Análisis de Sentimiento en Reseñas Multilingües**  
**Contexto:** Eres parte del equipo de NLP de **GlobalFeedback**, una empresa que analiza reseñas de productos en español, inglés y francés para identificar defectos críticos. El modelo actual confunde "no funcionó" y "funciona mal" como conceptos distintos por falta de normalización léxica.  

---

### **Instrucciones**  
**Objetivo:** Implementar un pipeline de lematización que unifique variantes morfológicas (*"corriendo" → "correr"*), mejorando la precisión del modelo de clasificación.  

---

### **Fase 1: Diagnóstico de Problemas**  
**Objetivo:** Identificar palabras no lematizadas que causan ruido en el análisis.  

#### **Tarea 1 - Análisis Exploratorio**  
1. **Descargar** el dataset `reviews_multilang.csv` 
2. **Ejemplo Crítico (Español):**  
   ```  
   "Los usuarios reportaron fallas constantes: no funciona, se traba y no responde."  
   ```  
3. **Procesar sin Lematización** usando `CountVectorizer`:  
   - Contar frecuencias de tokens: ["funciona", "funcionar", "trabó", "responder"].  
4. **Identificar:**  
   - Variantes morfológicas que inflan el vocabulario.  
   - Errores de POS tagging (ej: "reportaron" etiquetado como sustantivo).  

#### **Pistas:**  
- Usar `spacy.load("es_core_news_sm")` para inspeccionar POS tags.  
- Generar una nube de palabras con `WordCloud` para visualizar repeticiones innecesarias.  

#### **Verificación:**  
Tabla con 5 pares de palabras que deben unificarse (ej: "fallas" → "falla").  

---

### **Fase 2: Implementación del Lematizador**  
**Objetivo:** Crear una función que lematice texto según su idioma y categoría gramatical.  

#### **Tarea 2 - Pipeline de Lematización**  
1. **Para Español:**  
   - Usar spaCy para lematizar y obtener POS tags.  
   - Mapear verbos a infinitivo (*"reportaron" → "reportar"*), sustantivos a singular (*"fallas" → "falla"*).  
2. **Para Inglés:**  
   - Usar `WordNetLemmatizer` de NLTK con POS tags (ej: `pos='v'` para verbos).  
3. **Manejar Ambiguidades:**  
   - En "El banco financiero cerró", "cerró" → "cerrar" (verbo) vs "banco" → "banco" (sustantivo).  

#### **Requisitos:**  
- **Input:** "Los dispositivos fallaron constantemente, no funcionan bien."  
- **Output Esperado:** ["el", "dispositivo", "fallar", "constantemente", "no", "funcionar", "bien"].  

#### **Pista:**  
- Filtrar stopwords después de lematizar.  
- Usar `token.lemma_` en spaCy y `lemmatizer.lemmatize(token, pos)` en NLTK.  

---

### **Fase 3: Optimización y Validación**  
**Objetivo:** Ajustar el lematizador para manejar jerga técnica y evaluar su impacto.  

#### **Tarea 3 - Personalización y Pruebas (Opcional)**  
1. **Métricas de Rendimiento:**  
   - Entrenar un modelo de `RandomForest` con y sin lematización. Para predecir el sentimiento.  
   - Comparar F1-score y tamaño del vocabulario.  

#### **Pista:**  
- Usar `PhraseMatcher` de spaCy para detectar términos técnicos no lematizados.  
- Para "crasheó", aplicar una regla regex si el lematizador no lo resuelve.  

---

### **Fase 4: Evaluación Comparativa**  
**Objetivo:** Medir la mejora en la precisión del modelo y reducir falsos negativos.  

#### **Tarea 4 - Análisis Cuantitativo**  
1. **Dataset de Validación:**  
   - 200 reseñas etiquetadas manualmente (50% negativas, 50% positivas).  
2. **Resultados Esperados:**  
   - Reducción de vocabulario ≥30%.  
   - Aumento de F1-score ≥10% en reseñas con negaciones (*"no funciona" vs "funcionando"*).  

#### **Pista:**  
- Usar `TfidfVectorizer` para ponderar términos clave post-lematización.  
- Si el F1-score baja, revisar lemas de palabras negativas (*"nunca" → "nunca"*).  

---

### **Entrega Final**  
1. **Código:**  
   - Función `lematizar(texto, idioma)` que maneje español e inglés.  
2. **Documentación:**  
   - Reporte PDF con:  
     - Comparativo de métricas pre/post lematización.  
     - Ejemplos de errores corregidos (ej: "trabó" → "trabar").  
