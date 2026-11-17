# Disciplinas e projetos

Abra `index.html` no navegador para visualizar o site. Não é necessário instalar dependências.

## Adicionar conteúdo

Edite `index.html` e substitua a indicação de seção vazia pelo conteúdo desejado. Por exemplo, dentro da seção de disciplinas:

```html
<article>
  <h3>Nome da disciplina</h3>
  <ul>
    <li><a href="arquivos/nome-da-disciplina/lista.pdf">Abrir lista (PDF)</a></li>
    <li><a href="arquivos/nome-da-disciplina/material.pdf" download>Baixar material (PDF)</a></li>
  </ul>
</article>
```

Crie a pasta `arquivos/` e suas subpastas conforme necessário. Para projetos, adicione itens semelhantes à seção de projetos e, se necessário, coloque os arquivos na pasta `projetos/`. Ajuste os nomes e caminhos dos exemplos para os arquivos reais. Links externos também podem ser usados, inclusive para vídeos e arquivos grandes; confira se as permissões permitem o acesso dos colegas.

Os materiais das disciplinas existentes estão em `arquivos/`, separados por categoria e mantendo os caminhos originais dentro de cada categoria. Arquivos temporários Python (`__pycache__` e `.pyc`) não foram copiados. Como arquivos relacionados podem estar em categorias diferentes, códigos e notebooks podem precisar de ajustes nos caminhos para funcionar a partir dessas cópias.

## Publicar

Envie os arquivos para um repositório no GitHub e configure o GitHub Pages para publicar a partir da branch e pasta desejadas. Os caminhos relativos funcionam tanto localmente quanto no GitHub Pages. O conteúdo publicado será público.

O vídeo de Análise Numérica tem aproximadamente 880 MiB e ultrapassa o limite de 100 MiB por arquivo do GitHub. Antes de enviar o repositório, hospede-o em outro serviço e substitua seu link no HTML por um link público; não inclua o vídeo no envio ao GitHub.
