"use strict";

function setupDeleteConfirmation() {
  document.querySelectorAll("form[data-confirm-delete]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      const title = form.dataset.taskTitle || "esta tarefa";
      const confirmed = window.confirm(`Deseja realmente excluir \"${title}\"? Essa ação não pode ser desfeita.`);
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });
}

function setupHolidayLookup() {
  const input = document.querySelector("#due_date");
  const status = document.querySelector("#holiday-status");
  if (!input || !status) return;

  let controller = null;

  async function checkHoliday() {
    const selectedDate = input.value;
    status.className = "status-api";
    status.textContent = "";

    if (!selectedDate) return;

    if (controller) controller.abort();
    controller = new AbortController();

    status.textContent = "Consultando feriados nacionais...";
    status.classList.add("consultando");

    try {
      const response = await fetch(`/api/feriado?data=${encodeURIComponent(selectedDate)}`, {
        headers: { "Accept": "application/json" },
        signal: controller.signal,
      });
      const data = await response.json();

      status.className = "status-api";
      if (!response.ok || data.available === false) {
        status.textContent = data.message || data.error || "Não foi possível consultar os feriados agora.";
        status.classList.add("aviso");
        return;
      }

      if (data.is_holiday) {
        status.textContent = `Atenção: a data selecionada é feriado nacional (${data.name}).`;
        status.classList.add("feriado");
      } else {
        status.textContent = "A data selecionada não corresponde a um feriado nacional cadastrado na BrasilAPI.";
        status.classList.add("ok");
      }
    } catch (error) {
      if (error.name === "AbortError") return;
      status.className = "status-api aviso";
      status.textContent = "Não foi possível consultar os feriados agora. Você ainda pode salvar a tarefa.";
    }
  }

  input.addEventListener("change", checkHoliday);
  if (input.value) checkHoliday();
}

document.addEventListener("DOMContentLoaded", () => {
  setupDeleteConfirmation();
  setupHolidayLookup();
});
