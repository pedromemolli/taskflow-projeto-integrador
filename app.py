"""TaskFlow - Projeto Integrador em Computação II.

Aplicação web para gerenciamento de tarefas com Flask, SQLite, JavaScript,
integração com BrasilAPI, acessibilidade, testes e preparação para nuvem.
"""

from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

VALID_PRIORITIES = ("Baixa", "Média", "Alta")
VALID_STATUSES = ("Pendente", "Em andamento", "Concluída")


def create_app(test_config=None):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)

    default_database = os.environ.get(
        "DATABASE_PATH", os.path.join(app.instance_path, "taskflow.sqlite")
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
        DATABASE=default_database,
    )

    if test_config is not None:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                priority TEXT NOT NULL CHECK(priority IN ('Baixa', 'Média', 'Alta')),
                status TEXT NOT NULL DEFAULT 'Pendente'
                    CHECK(status IN ('Pendente', 'Em andamento', 'Concluída')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        db.commit()

    def get_task(task_id: int):
        task = get_db().execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if task is None:
            abort(404)
        return task

    def validate_task_form(form):
        title = form.get("title", "").strip()
        description = form.get("description", "").strip()
        due_date = form.get("due_date", "").strip()
        priority = form.get("priority", "").strip()
        status = form.get("status", "").strip()
        errors = []

        if len(title) < 3:
            errors.append("O título precisa ter ao menos 3 caracteres.")
        if len(title) > 100:
            errors.append("O título pode ter no máximo 100 caracteres.")

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Informe uma data limite válida.")

        if priority not in VALID_PRIORITIES:
            errors.append("Selecione uma prioridade válida.")
        if status not in VALID_STATUSES:
            errors.append("Selecione uma situação válida.")

        values = (title, description, due_date, priority, status)
        return errors, values

    @app.route("/")
    def index():
        status_filter = request.args.get("status", "").strip()
        priority_filter = request.args.get("priority", "").strip()

        query = "SELECT * FROM tasks WHERE 1 = 1"
        params = []
        if status_filter in VALID_STATUSES:
            query += " AND status = ?"
            params.append(status_filter)
        else:
            status_filter = ""

        if priority_filter in VALID_PRIORITIES:
            query += " AND priority = ?"
            params.append(priority_filter)
        else:
            priority_filter = ""

        query += (
            " ORDER BY CASE priority "
            "WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 ELSE 3 END, due_date, id"
        )
        tasks = get_db().execute(query, params).fetchall()

        totals = get_db().execute(
            """
            SELECT
              COUNT(*) AS total,
              COALESCE(SUM(status = 'Pendente'), 0) AS pending,
              COALESCE(SUM(status = 'Em andamento'), 0) AS in_progress,
              COALESCE(SUM(status = 'Concluída'), 0) AS completed,
              COALESCE(SUM(status != 'Concluída' AND due_date < ?), 0) AS overdue
            FROM tasks
            """,
            (date.today().isoformat(),),
        ).fetchone()

        return render_template(
            "index.html",
            tasks=tasks,
            totals=totals,
            status_filter=status_filter,
            priority_filter=priority_filter,
            priorities=VALID_PRIORITIES,
            statuses=VALID_STATUSES,
            today=date.today().isoformat(),
        )

    @app.route("/tarefas/nova", methods=("GET", "POST"))
    def create_task():
        form_data = None
        if request.method == "POST":
            errors, values = validate_task_form(request.form)
            form_data = request.form
            if errors:
                for error in errors:
                    flash(error, "error")
            else:
                get_db().execute(
                    """
                    INSERT INTO tasks (title, description, due_date, priority, status)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    values,
                )
                get_db().commit()
                flash("Tarefa cadastrada com sucesso.", "success")
                return redirect(url_for("index"))

        return render_template(
            "task_form.html",
            task=None,
            form_data=form_data,
            today=date.today().isoformat(),
            priorities=VALID_PRIORITIES,
            statuses=VALID_STATUSES,
        )

    @app.route("/tarefas/<int:task_id>/editar", methods=("GET", "POST"))
    def edit_task(task_id):
        task = get_task(task_id)
        form_data = None
        if request.method == "POST":
            errors, values = validate_task_form(request.form)
            form_data = request.form
            if errors:
                for error in errors:
                    flash(error, "error")
            else:
                get_db().execute(
                    """
                    UPDATE tasks
                    SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
                    WHERE id = ?
                    """,
                    (*values, task_id),
                )
                get_db().commit()
                flash("Tarefa atualizada com sucesso.", "success")
                return redirect(url_for("index"))

        return render_template(
            "task_form.html",
            task=task,
            form_data=form_data,
            today=date.today().isoformat(),
            priorities=VALID_PRIORITIES,
            statuses=VALID_STATUSES,
        )

    @app.post("/tarefas/<int:task_id>/concluir")
    def complete_task(task_id):
        get_task(task_id)
        get_db().execute(
            "UPDATE tasks SET status = 'Concluída' WHERE id = ?", (task_id,)
        )
        get_db().commit()
        flash("Tarefa marcada como concluída.", "success")
        return redirect(url_for("index"))

    @app.post("/tarefas/<int:task_id>/excluir")
    def delete_task(task_id):
        get_task(task_id)
        get_db().execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        get_db().commit()
        flash("Tarefa excluída.", "success")
        return redirect(url_for("index"))

    @app.get("/api/feriado")
    def check_holiday():
        """Consulta a BrasilAPI e devolve somente os dados usados pela interface."""
        requested_date = request.args.get("data", "").strip()
        try:
            parsed = datetime.strptime(requested_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify(error="Data inválida. Use o formato AAAA-MM-DD."), 400

        api_url = f"https://brasilapi.com.br/api/feriados/v1/{parsed.year}"
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "TaskFlow-PI2/1.0"},
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                holidays = json.load(response)
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
            return (
                jsonify(
                    available=False,
                    message="Não foi possível consultar os feriados agora.",
                ),
                503,
            )

        holiday = next(
            (item for item in holidays if item.get("date") == requested_date), None
        )
        if holiday:
            return jsonify(
                available=True,
                is_holiday=True,
                name=holiday.get("name", "Feriado nacional"),
            )
        return jsonify(available=True, is_holiday=False)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
