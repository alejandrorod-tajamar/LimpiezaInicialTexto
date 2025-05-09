**Práctica : Normalización de Texto para Análisis Multilingüe en Reseñas de Productos**  
**Contexto:** Eres parte del equipo de NLP de **GlobalReviews**, una empresa que procesa reseñas de usuarios en español, francés e inglés para detectar defectos en productos electrónicos.  

---

### **Instrucciones**  
**Objetivo Final:**  
Crear un pipeline de normalización de texto que maneje acentos, codificaciones rotas y contracciones, garantizando que el modelo GPT-4 fine-tuned interprete correctamente reseñas como:  
`"Ã‰ste es un buen móvil!!! No q'huvo fallos. #Duradero❤️"` → `"éste es un buen móvil no que hubo fallos #duradero"`.  



---

### **Fase 1: Diagnóstico de Problemas**  
**Objetivo:** Identificar errores de codificación, acentos inconsistentes y contracciones.  

#### **Tarea 1 - Análisis Inicial**  
1. **Descargar** el dataset `resenas_multilingue.csv`. Puedes descargar cualquier otro dataset de otra fuente. 
2. **Ejemplo Crítico:**  
   ```  
   "Ã‰ste celular es increÃ­ble!!! Pero tarda 5hs en cargarse... #BaterÃ­aMala 😞"  
   ```  
3. **Identificar:**  
   - Caracteres corruptos (`Ã‰`, `Ã­`).  
   - Emojis/acentos que afectan el análisis.  

#### **Pistas:**  
- Usar `chardet` para detectar la codificación real de textos corruptos.  
- Buscar patrones como `Ã` seguido de otro carácter (ej. `Ã©` → `é` en UTF-8 mal leído como Latin-1).  

---

### **Fase 2: Normalización Unicode y Codificación**  
**Objetivo:** Corregir textos corruptos y unificar formatos Unicode.  

#### **Tarea 2 - Pipeline Básico**  
1. **Corregir Codificación:**  
   - Convertir `"cafÃ©"` → `"café"` reinterpretando bytes (Latin-1 → UTF-8).  
2. **Normalizar Unicode:**  
   - Usar `unicodedata.normalize('NFC', texto)` para componer caracteres (ej: `e´` → `é`).  
3. **Preservar Emojis Relevantes:**  
   - Eliminar símbolos no esenciales (❌, ▲), pero preservar 😊, 😞 para análisis de sentimiento.  

#### **Pistas:**  
- Si `chardet` no detecta la codificación, probar combinaciones comunes: `utf-8`, `latin-1`, `windows-1252`.  
- Usar `errors='replace'` solo como último recurso.  

#### **Verificación:**  
Texto procesado:  
```  
"Éste celular es increíble!!! Pero tarda 5hs en cargarse... #BateríaMala 😞"  
```  

---

### **Fase 3: Manejo de Acentos y Contracciones**  
**Objetivo:** Eliminar acentos opcionales y expandir contracciones coloquiales.  

#### **Tarea 3 - Normalización Lingüística**  
1. **Eliminar Acentos No Fonémicos (Español):**  
   - Usar `unidecode` para convertir `"canción"` → `"cancion"`.  
   - **Excepción:** No aplicar a palabras donde el acento cambie el significado (ej: francés "aîné" vs. "aine").  
2. **Expandir Contracciones:**  
   - Crear un diccionario personalizado para:  
     - `"q'huvo"` → `"que hubo"`  
     - `"pq"` → `"porque"`  
     - `" x "` → `" por "`  
3. **Normalizar Hashtags:**  
   - Convertir `#BateríaMala` → `#bateriamala` (sin acentos, minúsculas).  

#### **Pistas:**  
- Usar `re.sub(r'\b([x])\b', 'por', texto)` para contracciones.  
- Para hashtags, aplicar `unidecode` antes de convertir a minúsculas.  

#### **Verificación:**  
Texto procesado:  
```  
"este celular es increible pero tarda 5hs en cargarse #bateriamala 😞"  
```  

---

### **Fase 4: Evaluación de Impacto**  
**Objetivo:** Medir cómo la normalización afecta la calidad del análisis.  

#### **Tarea 4 - Métricas Cuantitativas**  
1. **Reducción de Vocabulario:**  
   - Comparar el número de tokens únicos antes/después (ej: `"café"` y `"cafe"` → mismo token).  
2. **Entrenar Modelo de Clasificación:**  
   - Usar `CountVectorizer` + `LogisticRegression` para detectar reseñas negativas.  
   - Comparar precisión (accuracy) con/sin normalización.  

#### **Verificación:**  
- Reportar métricas en una tabla:  
  | Métrica               | Sin Normalización | Con Normalización |  
  |-----------------------|-------------------|-------------------|  
  | Tokens Únicos         | 12,540            | 9,320             |  
  | Accuracy              | 78%               | 85%               |  

---

### **Entrega Final**  
1. **Código:**  
   - Script de Python con funciones de normalización (`normalizacion.py`).  
2. **Documentación:**  
   - Reporte PDF con:  
     - Ejemplos antes/después.  
     - Análisis de cómo la normalización afectó las métricas.  
3. **Diccionario de Contracciones:**  
   - Archivo `.txt` con 20 entradas (ej: `dnd → donde`).  

**Datos de Validación:**  
- Archivo `test_normalizacion.json` con 10 casos (input y output esperado). Ejemplo:  
  ```json  
  {  
    "input": "Ã‰ste es un buen móvil!!! No q'huvo fallos. #Duradero❤️",  
    "output": "este es un buen movil no que hubo fallos #duradero"  
  }  
  ```  

**Nota:** Los alumnos recibirán un cheatsheet con:  
- Lista de caracteres Unicode problemáticos (ej: `Ã, Â, ã`).  
- Regex comunes para contracciones en español.


Claro, aquí tienes el **cheatsheet** que puedes entregar a los alumnos:

---

### **Cheatsheet: Limpieza de Texto Multilingüe para NLP**

#### **1. Caracteres Unicode Problemáticos (Comunes en UTF-8 mal decodificado):**

Estos caracteres suelen aparecer cuando un texto en UTF-8 es leído como ISO-8859-1 (Latin-1):

| Carácter | Corrección esperada | Comentario                             |
|----------|----------------------|----------------------------------------|
| Ã¡       | á                    | Vocal acentuada                        |
| Ã©       | é                    | Vocal acentuada                        |
| Ã­       | í                    | Vocal acentuada                        |
| Ã³       | ó                    | Vocal acentuada                        |
| Ãº       | ú                    | Vocal acentuada                        |
| Ã±       | ñ                    | Letra "ñ"                              |
| Ã‰       | É                    | Vocal mayúscula                        |
| Â        | (eliminar)           | Común con tildes o comillas            |
| â€™      | ’                    | Comilla derecha                        |
| â€œ / â€ | “ / ”                | Comillas tipográficas                  |
| â€“      | –                    | Guion largo (en lugar de "-")          |

> **Conjejos para limpiar:** Usa `.encode('latin1').decode('utf8')` en Python cuando leas archivos con estos errores.

---

#### **2. Regex útiles para limpiar y normalizar texto (contracciones en español):**

| Expresión Regular                | Objetivo                              | Ejemplo                           |
|----------------------------------|---------------------------------------|-----------------------------------|
| `\b(al|del)\b`                   | Detectar contracciones comunes        | "al supermercado", "del coche"   |
| `(?i)\b(no|nunca|tampoco|ni|sin)\b` | Detectar negaciones clave              | "no quiero", "sin azúcar"        |
| `[#@]\w+`                        | Detectar hashtags y menciones         | "#MalaEntrega", "@Soporte"       |
| `[^a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s]`      | Eliminar símbolos no deseados         | Emojis, puntuación innecesaria   |
| `\s{2,}`                         | Reemplazar múltiples espacios          | "esto   es   prueba" → "esto es prueba" |

