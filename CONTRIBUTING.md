# Contribuir a Jelou

¡Gracias por tu interés en contribuir a Jelou! 🎉

## 🐛 Reportar bugs

Si encuentras un bug:

1. Verifica que no exista ya en [Issues](https://github.com/N7C0LAS/jelou/issues)
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs. actual
   - Versión de Python y sistema operativo

## ✨ Sugerir mejoras

Para sugerir nuevas características:

1. Abre un issue con la etiqueta "enhancement"
2. Describe el caso de uso
3. Explica por qué sería útil

## 🔧 Contribuir código

### 1. Fork y clone
```bash
git clone https://github.com/TU-USUARIO/jelou.git
cd jelou
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest
```

### 3. Crear una rama
```bash
git checkout -b feature/mi-nueva-caracteristica
```

### 4. Hacer cambios

- Escribe código claro y bien documentado
- Sigue el estilo existente del proyecto
- Agrega tests para código nuevo

### 5. Ejecutar tests
```bash
pytest -v
```

**Todos los tests deben pasar** ✅

### 6. Commit

Usa mensajes descriptivos:
```bash
git commit -m "feat: agregar soporte para frases completas"
git commit -m "fix: corregir conversión de diptongo /eɪ/"
git commit -m "docs: actualizar README con nuevos ejemplos"
```

### 7. Push y Pull Request
```bash
git push origin feature/mi-nueva-caracteristica
```

Luego abre un Pull Request en GitHub.

## 📋 Checklist antes de PR

- [ ] Todos los tests pasan (`pytest -v`)
- [ ] Agregué tests para código nuevo
- [ ] Actualicé la documentación si es necesario
- [ ] El código sigue el estilo del proyecto
- [ ] Commit messages son claros

## 🎯 Áreas donde ayudar

- Agregar más tests
- Mejorar documentación
- Agregar soporte para británico inglés
- Optimizar performance
- Traducir README a otros idiomas

## 💬 ¿Preguntas?

Abre un issue con la etiqueta "question" o contacta al mantenedor.

## 📜 Código de Conducta

Se respetuoso y profesional. Este es un proyecto de código abierto para ayudar a la comunidad.

---

**¡Gracias por contribuir!** ❤️
