# ⚡ Buscador Rayo McQueen 🏎️

**Buscador Rayo McQueen** es una herramienta ligera, potente y extremadamente rápida escrita en Python para encontrar archivos perdidos en las profundidades de tus carpetas.

---

## 🌟 Especialidad

Este buscador utiliza `os.scandir` para iterar por tus archivos a máxima velocidad, ofreciendo filtros avanzados que realmente funcionan.

### 🚀 Características principales:

- **🔍 Búsqueda Multipalabra:** Filtra por múltiples palabras clave. No importa el orden, si están en el nombre, el buscador las encuentra.
- **📏 Filtros de Tamaño Inteligentes:** Si estás buscando un vídeo que pesa más de 1GB, o un script de menos de 10KB, el buscador soporta filtros por tamaño como `KB`, `MB` y `GB` de forma nativa.
- **📂 Apertura Instantánea:** Una vez encuentras lo que buscas, puedes abrir su ubicación directamente desde el programa.
- **🛡️ Anti-Crash:** Limitación inteligente de resultados en pantalla para que tu terminal no explote si buscas en todo el disco `C:\`.
- **💻 Multiplataforma:** Funciona en Windows, macOS y Linux.

---

## 🛠️ Instalación y Uso

### Requisitos

Solo necesitas tener **Python 3.x** instalado. No requiere ninguna librería externa.

### Ejecución

1. Clona este repositorio o descarga el archivo `Buscador-de-archivos.py`.
2. Haz doble clic en el archivo `Buscador-de-archivos.py`.

---

## 📖 Guía de Navegación

El programa es intuitivo, pero aquí hay matices que harán que lo uses con más eficacia:

### 1. Palabras Clave

Si buscas `proyecto final`, el programa encontrará `mi_proyecto_final.zip` y también `final_proyecto_v2.pdf`. El orden no importa, solo la existencia.

### 2. Filtros de Tamaño

Puedes ingresar valores como:

- `500MB`
- `2GB`
- `100KB`
- Si solo pones un número (ej: `100`), se asumirá que son **Megabytes**.

### 3. Rutas

Por defecto buscará en tu unidad principal, pero puedes cambiarla en el menú de filtros a cualquier unidad o carpeta específica para ir aún más rápido.

---

## 🎨 Cómo se ve la interfaz:

```text
==========================================
       CONFIGURAR BUSQUEDA AVANZADA
==========================================
1. Palabras clave : proyecto + 2024
2. Extension      : .pdf
3. Tamano minimo  : 10 MB
4. Tamano maximo  : Sin limite
5. Ruta a buscar  : C:\Users\PC\Documents
------------------------------------------
6. [>] INICIAR BUSQUEDA AHORA
7. [x] Volver al menu principal
```

---

## 🛡️ Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Úsalo, modifícalo y hazlo volar.

---

Desarrollado por [aitorino2009](https://github.com/aitorino2009).
