# Logos Reference

Sistema de logos do Beauty Smile Design System.

## Variacoes

### Horizontal
Uso: Headers, materiais digitais, banners
```
/logos/svg/horizontal/BS_Horizontal_Azul.svg
/logos/svg/horizontal/BS_Horizontal_Branco.svg
/logos/svg/horizontal/BS_Horizontal_Cinza.svg
/logos/svg/horizontal/BS_Horizontal_Dourado.svg
/logos/svg/horizontal/BS_Horizontal_Preto.svg
/logos/svg/horizontal/BS_Horizontal_Turquesa.svg
/logos/svg/horizontal/BS_Horizontal_Ouro3D.svg
/logos/svg/horizontal/BS_Horizontal_Prata3D.svg
```

### Vertical
Uso: Espacos quadrados, materiais impressos
```
/logos/svg/vertical/BeautySmile_Vertical_Azul.svg
/logos/svg/vertical/BeautySmile_Vertical_Branco.svg
/logos/svg/vertical/BeautySmile_Vertical_Preto.svg
/logos/svg/vertical/BS_Vertical_Cinza.svg
/logos/svg/vertical/BS_Vertical_Dourado.svg
/logos/svg/vertical/BS_Vertical_Turquesa.svg
/logos/svg/vertical/BS_Vertical_Azul3D.svg
/logos/svg/vertical/BS_Vertical_Cinza3D.svg
/logos/svg/vertical/BS_Vertical_Dourado3D.svg
/logos/svg/vertical/BS_Vertical_Ouro3D.svg
/logos/svg/vertical/BS_Vertical_Prata3D.svg
/logos/svg/vertical/BS_Vertical_Turquesa3D.svg
```

### Isotipo
Uso: Favicon, icones de app, espacos pequenos
```
/logos/svg/isotipo/BS_Isotipo_Azul.svg
/logos/svg/isotipo/BS_Isotipo_Branco.svg
/logos/svg/isotipo/BS_Isotipo_Cinza.svg
/logos/svg/isotipo/BS_Isotipo_Dourado.svg
/logos/svg/isotipo/BS_Isotipo_Preto.svg
/logos/svg/isotipo/BS_Isotipo_Turquesa.svg
/logos/svg/isotipo/BS_Isotipo_Azul3D.svg
/logos/svg/isotipo/BS_Isotipo_Branco3D.svg
/logos/svg/isotipo/BS_Isotipo_Cinza3D.svg
/logos/svg/isotipo/BS_Isotipo_Ouro3D.svg
/logos/svg/isotipo/BS_Isotipo_Prata3D.svg
/logos/svg/isotipo/BS_Isotipo_Turquesa3D.svg
```

### Tipografico
Uso: Apenas nome da marca
```
/logos/svg/tipografico/BS_Tipografico_Azul.svg
/logos/svg/tipografico/BS_Tipografico_Branco.svg
/logos/svg/tipografico/BS_Tipografico_Cinza.svg
/logos/svg/tipografico/BS_Tipografico_Dourado.svg
/logos/svg/tipografico/BS_Tipografico_Preto.svg
/logos/svg/tipografico/BS_Tipografico_Turquesa.svg
/logos/svg/tipografico/BS_Tipografico_Ouro3D.svg
/logos/svg/tipografico/BS_Tipografico_Prata3D.svg
```

## Cores Disponiveis

| Cor | Hex | Uso |
|-----|-----|-----|
| Azul | #00109E | Fundo claro, uso principal |
| Branco | #FFFFFF | Fundo escuro/colorido |
| Cinza | #6B6D70 | Aplicacoes neutras |
| Dourado | #BB965B | Premium, destaques |
| Preto | #2D2E30 | Alto contraste |
| Turquesa | #35BFAD | Public theme |

## Logos 3D Metalicos

Para aplicacoes premium:
```
# PNG (alta resolucao)
/logos/3d/png/BS_Horizontal_Ouro3D.png
/logos/3d/png/BS_Vertical_Ouro3D.png
/logos/3d/png/BS_Isotipo_Ouro3D.png

# WebP (otimizado web)
/logos/3d/webp/BS_Horizontal_Ouro3D.webp
/logos/3d/webp/BS_Horizontal_Prata3D.webp
/logos/3d/webp/BS_Vertical_Azul3D.webp
/logos/3d/webp/BS_Vertical_Ouro3D.webp
/logos/3d/webp/BS_Isotipo_Ouro3D.webp
```

## Tamanhos Minimos

| Formato | Digital (px) | Impresso (mm) |
|---------|--------------|---------------|
| Horizontal | 120px | 30mm |
| Vertical | 80px | 20mm |
| Isotipo | 32px | 8mm |
| Tipografico | 100px | 25mm |

## Area de Protecao

Espaco minimo ao redor = altura do isotipo

```
+------------------+
|                  |
|   [  LOGO  ]     |
|                  |
+------------------+
```

## Uso no React

```tsx
// Importar como componente
import HorizontalLogo from '@/assets/logos/svg/horizontal/BS_Horizontal_Azul.svg'

// Uso
<img src="/logos/svg/horizontal/BS_Horizontal_Azul.svg" alt="Beauty Smile" />

// Com fallback
<picture>
  <source srcSet="/logos/3d/webp/BS_Horizontal_Ouro3D.webp" type="image/webp" />
  <img src="/logos/3d/png/BS_Horizontal_Ouro3D.png" alt="Beauty Smile" />
</picture>
```

## Selecao por Contexto

| Contexto | Variacao | Cor |
|----------|----------|-----|
| Header site | Horizontal | Azul |
| Header dark | Horizontal | Branco |
| Favicon | Isotipo | Azul |
| App icon | Isotipo | Turquesa |
| Footer | Horizontal | Cinza |
| Material premium | Horizontal 3D | Ouro |
| Admin dashboard | Horizontal | Branco |
| Landing page | Vertical | Turquesa |
| Email signature | Horizontal | Azul |
| Apresentacao | Vertical 3D | Ouro |

## Uso Correto

### Fazer
- Usar cores oficiais
- Manter proporcoes originais
- Respeitar area de protecao
- Usar fundos com contraste
- Preferir SVG

### Nao Fazer
- Alterar cores
- Distorcer/esticar
- Adicionar sombras/efeitos
- Usar em fundos sem contraste
- Reduzir abaixo do minimo

## Estrutura de Arquivos

```
src/assets/logos/
├── svg/
│   ├── horizontal/    # 8 arquivos
│   ├── vertical/      # 13 arquivos
│   ├── isotipo/       # 12 arquivos
│   └── tipografico/   # 8 arquivos
├── 3d/
│   ├── png/           # 15 arquivos
│   └── webp/          # 17 arquivos
└── index.ts           # Exports tipados
```
