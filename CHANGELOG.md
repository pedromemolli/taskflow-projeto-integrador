# Alterações da versão atualizada do TaskFlow

## Funcionalidades adicionadas/completadas

- JavaScript real no front-end (`static/app.js`).
- Confirmação de exclusão antes de enviar o formulário.
- Consulta dinâmica de feriado ao selecionar a data de prazo.
- Integração front-end → endpoint Flask → BrasilAPI.
- Controles visíveis para filtros de situação e prioridade.
- Painel ampliado com total de tarefas atrasadas.
- Melhorias de responsividade e acessibilidade.
- Preservação dos campos do formulário após erro de validação.
- Página 404 amigável.
- Testes ampliados: criação, validações, edição, conclusão, exclusão, filtros, API e 404.
- Estrutura de testes movida para a pasta `tests/`, coerente com o comando do README.
- `Procfile`, `render.yaml` e Gunicorn incluídos para implantação em nuvem.
- README revisado para refletir somente funcionalidades realmente presentes no pacote.
