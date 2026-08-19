# TaskFlow — Projeto Integrador

Aplicação web acessível para cadastro e organização de tarefas. É uma referência simples para comparação e estudo: adapte nomes, textos e funcionalidades ao seu próprio projeto antes da entrega.

## O que o projeto demonstra

| Requisito do PI | Implementação |
|---|---|
| Framework web | Flask (Python) |
| Banco de dados | SQLite, com tabela `tasks` |
| JavaScript | confirmação de exclusão e consulta dinâmica de feriados |
| API | [BrasilAPI](https://brasilapi.com.br/) consulta feriados nacionais |
| Nuvem | `render.yaml` e `Procfile` para publicação no Render |
| Acessibilidade | HTML semântico, labels, foco visível, contraste, link para pular conteúdo e avisos com `aria-live` |
| Versionamento | arquivos prontos para uso com Git/GitHub |
| Testes | testes automatizados com `unittest` |
| Análise de dados | painel de totais por situação |

## Funcionalidades

- Cadastrar, editar, concluir e excluir tarefas.
- Registrar título, descrição, prazo, prioridade e situação.
- Filtrar por prioridade e situação.
- Consultar se o prazo selecionado coincide com feriado nacional.
- Ver um resumo com totais de tarefas.

## Como executar no seu computador

Pré-requisito: Python 3.10 ou superior instalado.

```powershell
cd taskflow
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000` no navegador. O banco SQLite é criado automaticamente na pasta `instance` após a primeira execução.

Se o PowerShell impedir a ativação do ambiente virtual, execute uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Como rodar os testes

Com o ambiente virtual ativado:

```powershell
python -m unittest discover -s tests -v
```

Os testes usam um banco temporário e não alteram suas tarefas reais.
