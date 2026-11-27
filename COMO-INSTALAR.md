# Como colocar no seu perfil

Faça isso pelo computador (o GitHub pelo celular não deixa subir pastas).

1. **Crie o repositório especial**: github.com/new → nome `pedropacheico` (igual ao seu usuário) → **Public** → Create.
2. **Suba os arquivos**: no repo, *Add file → Upload files* e arraste **o conteúdo** desta pasta (README.md, assets, scripts, .github). Commit.
   - A pasta `.github` começa com ponto e pode ficar oculta no Windows. Se não aparecer, ative "Itens ocultos" no Explorador de Arquivos.
3. **Libere as Actions para salvar arquivos**: no repo, *Settings → Actions → General → Workflow permissions* → **Read and write permissions** → Save.
4. **Rode as duas Actions uma vez**: aba *Actions* → "Stylish Rank" → *Run workflow*. Depois "Arena (cobra de contribuições)" → *Run workflow*.
5. Abra github.com/pedropacheico. Pronto.

## Mudar textos
- Textos do README: edite o `README.md` direto no GitHub.
- Textos dos banners (nome, subtítulo, frases): edite o topo de `scripts/build_assets.py` e rode `python scripts/build_assets.py` na pasta do repo.
- Faixas do Stylish Rank: lista `RANKS` em `scripts/stylish_rank.py`.
