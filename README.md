# TaskFlow — Projeto Integrador em Computação II

Aplicação web acessível para cadastro, organização e acompanhamento de tarefas.

## Acesse online

🔗 **https://taskflow-pi2.onrender.com**

> Na hospedagem gratuita do Render, o site entra em repouso após um período sem acesso. O primeiro carregamento pode levar cerca de um minuto; depois disso, ele responde normalmente.

## Requisitos do PI II contemplados

| Requisito | Implementação no projeto |
|---|---|
| Framework web | Flask (Python) |
| Banco de dados | SQLite, tabela `tasks` |
| JavaScript | confirmação de exclusão e consulta dinâmica de feriados |
| API | BrasilAPI, consulta de feriados nacionais |
| Nuvem | `render.yaml`, `Procfile` e Gunicorn para publicação |
| Acessibilidade | HTML semântico, labels, foco visível, link de salto, regiões `aria-live`, navegação por teclado e tabela rolável |
| Controle de versão | `.gitignore` e estrutura preparada para Git/GitHub |
| Testes | suíte automatizada com `unittest` |
| Análise de dados | painel de totais por situação e tarefas atrasadas |

## Funcionalidades

- Cadastrar, editar, concluir e excluir tarefas.
- Registrar título, descrição, prazo, prioridade e situação.
- Filtrar tarefas por prioridade e situação.
- Ordenar por prioridade e prazo.
- Confirmar exclusão por JavaScript.
- Consultar dinamicamente se o prazo escolhido coincide com feriado nacional.
- Exibir resumo de tarefas totais, pendentes, em andamento, concluídas e atrasadas.
- Preservar os valores digitados quando uma validação do formulário falha.
- Exibir página amigável para recurso inexistente (404).

## Tecnologias

- Python 3.10+
- Flask
- SQLite
- HTML5 / CSS3
- JavaScript
- BrasilAPI
- Git / GitHub
- unittest
- Gunicorn (somente para implantação em servidor)
- Render (configuração de implantação)

## Executar no Windows PowerShell

Na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000`.

Se a política do PowerShell bloquear a ativação do ambiente virtual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Também é possível usar `iniciar.bat` com duplo clique.

## Rodar os testes

Com o ambiente virtual ativado:

```powershell
python -m unittest discover -s tests -v
```

Os testes usam banco temporário e não alteram suas tarefas reais.

## Publicação em nuvem

O projeto inclui `render.yaml` e `Procfile`. A aplicação lê a variável `SECRET_KEY` do ambiente e pode usar `DATABASE_PATH` para definir outro caminho do SQLite.

> Observação: em hospedagens com sistema de arquivos efêmero, um SQLite local pode ser recriado após reinicializações/deploys. Para persistência permanente em produção, configure armazenamento persistente ou migre posteriormente para um banco gerenciado, como PostgreSQL.

## Estrutura

```text
TaskFlow_PI2_Atualizado/
├── app.py
├── iniciar.bat
├── requirements.txt
├── requirements-cloud.txt
├── Procfile
├── render.yaml
├── README.md
├── CHANGELOG.md
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── task_form.html
│   └── 404.html
└── tests/
    └── test_app.py
```
