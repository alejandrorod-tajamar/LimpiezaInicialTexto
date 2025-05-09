**Práctica: Eliminación Contextual de Stopwords para Análisis de Reseñas de Productos**  

**Contexto:** Eres un NLP Engineer en **ReviewBoost**, una startup que analiza reseñas de Amazon para identificar problemas críticos en productos.  

---

### **Fase 1: Análisis Inicial**  
**Objetivo:** Entender cómo las stopwords por defecto afectan el significado en reseñas.  

#### **Tarea 1:**  
- **Descargar** el dataset `comensarios_clintes.csv`. Puedes utilizar otro dataset de internet.  
- **Ejemplo de Entrada:**  
```No recomiendo este producto. Aunque es barato, se rompió en dos días.
``` 
- **Procesar** el texto usando spaCy con stopwords por defecto.  
- **Registrar:**  
  - ¿Qué palabras clave se eliminaron (ej. "no", "aunque")?  
  - ¿Cómo afecta esto al significado?  

**Procesamiento Actual (spaCy):**  
```  
["mal", "producto", "entrega", "pésima", "marketminddecepciona"]  
```  
**Problema:** La palabra "no" se eliminó, invirtiendo el significado.  

#### **Pistas:**  
- Usar `spacy.load("es_core_news_sm")` y `token.is_stop`.  
- Para debuggear: Imprimir lista de stopwords con `print(nlp.Defaults.stop_words)`.  

#### **Verificación:**  
El estudiante debe generar una tabla con 5 ejemplos donde la eliminación de stopwords alteró el significado.  
 

---

### **Fase 2: Personalización de la Lista**  
**Objetivo:** Crear una lista de stopwords adaptada a reseñas de productos.  

#### **Tarea 2:**  
1. **Preservar Términos Clave:**  
   - Negaciones: "no", "nunca", "tampoco".  
   - Conectores de contraste: "pero", "aunque", "sin embargo".  
2. **Eliminar Términos Genéricos:**  
   - Palabras redundantes: "producto", "cliente", "día".  
   - Verbos comunes sin contexto: "hacer", "tener", "decir".  
3. **Añadir Stopwords Específicas:**  
   - Términos no informativos: "hola", "gracias", "pd".  

#### **Pasos:**  
- **Analizar Frecuencia:** Usar `Counter` de Python para identificar palabras repetidas en el 90% de las reseñas.  
- **Modificar Lista:**  
  - Cargar stopwords de spaCy.  
  - Quitar términos críticos (ej. `stopwords_es.discard("no")`).  
  - Añadir términos redundantes (ej. `stopwords_es.add("producto")`).  

#### **Pistas:**  
- Para "hola" y "gracias", usar regex: `r'\b(hola|gracias)\b'`.  
- Usar `nltk.corpus.stopwords.words('spanish')` como lista alternativa si hay inconsistencias.  

---

### **Fase 3: Implementación y Pruebas**  
**Objetivo:** Validar que la lista personalizada preserva el contexto crítico.  

#### **Tarea 3:**  
1. **Función de Procesamiento:**  
   - Input: Texto crudo.  
   - Output: Lista de tokens sin stopwords personalizadas.  
2. **Casos de Prueba:**  
   ```  
   Texto 1: "No funciona bien, pero el diseño es bonito."  
   Output Esperado: ["no", "funciona", "bien", "pero", "diseño", "bonito"]  

   Texto 2: "Nunca compré algo tan malo. Aunque el precio es bajo, no lo vale."  
   Output Esperado: ["nunca", "compré", "malo", "aunque", "precio", "bajo", "no", "vale"]  
   ```  
3. **Métricas:**  
   - Precisión: 100% de los términos clave preservados en 20 casos de prueba predefinidos.  

#### **Pistas:**  
- Usar `token.text.lower()` para normalizar.  
- Si "aunque" se elimina, revisar `stopwords_es.remove("aunque")`.  

---

### **Fase 4: Evaluación de Impacto**  
**Objetivo:** Medir cómo afecta la personalización al análisis de sentimiento.  

#### **Tarea 4:**  
1. **Entrenar Modelo Básico:**  
   - Usar `sklearn` (CountVectorizer + LogisticRegression).  
   - Comparar resultados con/sin stopwords personalizadas.  
2. **Métricas:**  
   - Exactitud (accuracy) en un subset de 200 reseñas etiquetadas manualmente.  
3. **Análisis:**  
   - ¿En qué reseñas mejoró/deterioró la clasificación?  

#### **Pistas:**  
- Usar `max_features=1000` en CountVectorizer para reducir dimensionalidad.  
- Ejemplo de mejora: Reseñas con negaciones clasificadas correctamente.  

---

### **Entrega Final**  
1. **Código:**  
   - Script `stopwords_custom.py` (funciones de carga, procesamiento, y evaluación).  
2. **Documentación:**  
   - Lista final de stopwords (`.txt`).  

