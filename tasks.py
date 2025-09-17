import time


def process_job(message: str, notify: bool) -> dict:
    """
    Executa uma tarefa simulada de processamento.

    Args:
        message (str): Texto enviado pelo cliente que será retornado no resultado.
        notify (bool): Indica se o cliente deseja ser notificado quando a tarefa terminar.
    Returns:
        status (string): indicando que a tarefa terminou.
        message (string): o mesmo texto recebido como entrada.
        notify (bool): o mesmo valor recebido como entrada.
        elapsed_seconds (float): tempo gasto para executar a tarefa.
    """
    start = time.perf_counter()
    time.sleep(10)
    elapsed = round(time.perf_counter() - start, 2)

    return {
        "status": "done",
        "message": message,
        "notify": notify,
        "elapsed_seconds": elapsed
    }
