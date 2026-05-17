# §10.5 Auto-detection de Marca

> Contrato LOCKED — D6 (`brands.yaml` extensível). Roda **antes** da entrevista universal.

## Arquivo de configuração

```
~/.config/deck-builder/brands.yaml
```

Template em `templates/brands.yaml.example` (3 marcas pré-povoadas).

## Schema

```yaml
schema_version: 1
brands:
  - name: "<Nome legível>"
    regex: '<regex JS/Python compatível>'
    design_system_skill: "<skill slug ou null>"
    compliance_tags: ["<tag>", ...]
```

## 3 marcas pré-povoadas (instaladas via copy do template)

```yaml
brands:
  - name: "Beauty Smile"
    regex: '\bBeauty Smile\b|beautysmile'
    design_system_skill: "beauty-smile-design-system"
    compliance_tags: ["odontologia-br", "cfo-cfm"]

  - name: "Fotona"
    regex: '\bFotona\b|LightWalker|Er:YAG|Nd:YAG'
    design_system_skill: null
    compliance_tags: ["anvisa-laser-classe-iii", "cfo-laser"]

  - name: "Carnaval 360"
    regex: '\bCarnaval 360\b|carnaval360'
    design_system_skill: null
    compliance_tags: []
```

## Ordem de detecção (primeiro match vence)

1. **Input do usuário** — regex YAML aplicada na mensagem original
2. **CLAUDE.md ativo** — varre o `CLAUDE.md` do cwd buscando match
3. **Agente `culture-lab` carregado** → Beauty Smile fallback
4. **Skill `laser-physics` carregada** → Fotona fallback
5. **Nenhum match** → marca = "genérico", pergunta U6 normalmente

## Ações ao detectar uma marca

1. **Carrega tokens de design system** (se `design_system_skill` declarado e instalado):
   - Beauty Smile → carrega skill `beauty-smile-design-system` (paleta + tipografia + glass morphism)
   - Outras marcas com design system custom → mesmo padrão

2. **Injeta compliance tags** nas skills relevantes:
   - `odontologia-br` + `cfo-cfm` → `deck-clinical` aplica 3 tiers CFO 196/2019 + CFM 1974/2011
   - `anvisa-laser-classe-iii` → `deck-equipment` + `deck-clinical` aplicam compliance laser
   - `cfo-laser` → `deck-teaching` (curso laser) injeta disclaimer

3. **Pula U6** se detection foi alta confiança (regex direta no input).

## Adicionando uma marca própria

Editar `~/.config/deck-builder/brands.yaml`:

```yaml
brands:
  # ... 3 padrão acima ...

  - name: "Cliente XYZ"
    regex: '\bXYZ\b|xyz-corp|clientexyz\.com'
    design_system_skill: null   # ou nome de skill custom
    compliance_tags: ["b2b-saas", "lgpd"]
```

Tags livres — cada skill decide se reconhece a tag. Tags desconhecidas são ignoradas.

## Falhas graciosas

- `brands.yaml` ausente → assume marca "genérico", pergunta U6
- `brands.yaml` malformado → log warning + assume "genérico" (não trava o fluxo)
- Regex inválido em uma entrada → pula essa entrada, processa as outras

## Cross-references

- `entrevista-universal-u1-u6.md` — U6 é a fallback quando detection falha
- `routing-matrix.md` — auto-detection roda ANTES do routing
- `../templates/brands.yaml.example` — template instalado em `~/.config/deck-builder/`
