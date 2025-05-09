**Práctica Integrada: Pipeline de Preprocesamiento para Análisis de Feedback en E-Commerce**  
**Contexto Empresarial Real:**  
Eres parte del equipo de NLP de **MarketMind**, una empresa de e-commerce que analiza millones de comentarios de clientes (inglés/español) y tweets para detectar tendencias de productos. **Problema actual:** El modelo GPT-4 fine-tuned genera resúmenes erróneos porque el texto crudo contiene URLs, precios, y emoticones mal normalizados.  

---

### **Fase 1: Limpieza Contextual de Texto**  
**Objetivo:** Crear una función que procese texto crudo preservando información crítica para análisis comercial.  

#### **Datos de Entrada:**  

Archivo -> validation_samples.json

#### **Requisitos:**  
1. **Eliminar:**  
   - URLs, handles de usuario (@MariaP), y signos de puntuación *excepto* `!`, `?`, `%`, `$`, `/`.  
   - Paréntesis `()` y corchetes `[]`.  
2. **Preservar:**  
   - Emoticones (😃, 🔥), hashtags (#ModaDeportiva2023), y formatos comerciales (`2x`, `$99.99`).  
   - Fechas (`30/11/2023`), horas (`18:30`), y porcentajes (`15%`).  
3. **Normalizar:**  
   - Unificar espacios múltiples y saltos de línea.  

#### **Pistas de Implementación:**  
- Usar regex con grupos capturadores para fechas (`\b\d{2}/\d{2}/\d{4}\b`).  
- Para emoticones, usar la librería `emoji` (no eliminar 🚫→ ✅).  
- Preservar `$`, `%`, y `/` solo si están adyacentes a números: `\$?\d+(\.\d+)?%?`.  

#### **Verificación:**  
El texto procesado debe quedar:  
```  
🔥 OFERTA Compre 2x zapatos Nike a $99.99 antes $150 👟  
Válido hasta el 30/11/2023 Atención ¿Envío gratis 😃 #ModaDeportiva2023  
```  

---

### **Fase 2: Normalización de Números y Unidades**  
**Objetivo:** Reemplazar números genéricos pero preservar formatos clave para el modelo de precios.  

#### **Requisitos:**  
1. **Reemplazar:**  
   - Números sueltos (ej. `150` → `<NUM>`) excepto si están en fechas, precios, o unidades (`2x`).  
2. **Convertir:**  
   - Fechas a formato estándar ISO: `30/11/2023` → `2023-11-30`.  
   - Unidades de venta al por menor: `2x` → `2_unidades`, `3kg` → `3_kg`.  
3. **Procesar Monedas:**  
   - `$99.99` → `<USD>99.99`, `150€` → `<EUR>150`.  

#### **Pistas de Implementación:**  
- Usar `dateparser` para normalizar fechas en múltiples formatos (ej. `marzo 15, 2023` → `2023-03-15`).  
- Para unidades: `r'\b(\d+)(x|kg|ml)\b'` → `\1_\2`.  
- Diferenciar `$100` (precio) de `100$` (común en español) usando lookbehinds en regex.  

#### **Verificación:**  
Salida esperada:  
```  
🔥 OFERTA Compre 2_unidades zapatos Nike a <USD>99.99 antes <NUM> 👟  
Válido hasta el 2023-11-30 Atención ¿Envío gratis 😃 #ModaDeportiva2023  
```  

---

### **Fase 3: Normalización de Mayúsculas con Reconocimiento de Entidades**  
**Objetivo:** Convertir a minúsculas sin perder marcas comerciales o nombres de productos.  

#### **Requisitos:**  
1. **Preservar en mayúsculas:**  
   - Nombres de marcas (`Nike`, `iPhone`).  
   - Hashtags (`#ModaDeportiva2023`).  
   - Entidades geopolíticas (`Madrid`, `México`).  
2. **Convertir a minúsculas:**  
   - Verbo "compre" → "compre", "Zapatos" → "zapatos".  

#### **Pistas de Implementación:**  
- Usar `spaCy` con modelo `es_core_news_lg` para detectar entidades (ORG, LOC, PRODUCT).  
- Para marcas no reconocidas por spaCy (ej. `Zara`), cargar un diccionario personalizado desde un CSV.  

#### **Verificación Final:**  
```  
🔥 oferta compre 2_unidades zapatos nike a <usd>99.99 antes <num> 👟  
válido hasta el 2023-11-30 atención ¿envío gratis 😃 #modadeportiva2023  
```  
**Error Común:** Si "Nike" se convierte a "nike", el modelo de productos no identificará la marca.  

---
