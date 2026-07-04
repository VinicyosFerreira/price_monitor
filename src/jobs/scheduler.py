"""Agenda a coleta e a transformação dos preços uma vez por dia."""

import logging
import os
import time
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from src.extract.main import Extractor
from src.transform.main import Transform


ROOT_PATH = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT_PATH / "logs"

MAX_ATTEMPTS = 3  # 1 execução inicial + 2 tentativas adicionais
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", "300"))
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))


def configure_logging() -> None:
    """Configura os logs no terminal e em logs/scheduler.log."""
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH / "scheduler.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def run_pipeline() -> None:
    """Gera a fotografia dinâmica e executa sua transformação."""
    logging.info("Gerando nova fotografia de preços a partir da fixture.")
    products_path = Extractor().execute()
    logging.info("Iniciando transformação dos produtos gerados.")
    Transform(source_path=products_path).execute()
    logging.info("Pipeline diária concluída com sucesso.")


def run_with_retry() -> None:
    """Repete a pipeline até duas vezes se alguma etapa falhar."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            logging.info("Execução %s de %s iniciada.", attempt, MAX_ATTEMPTS)
            run_pipeline()
            return
        except Exception:
            logging.exception("Falha na execução %s de %s.", attempt, MAX_ATTEMPTS)

            if attempt == MAX_ATTEMPTS:
                logging.error("Pipeline encerrada após %s falhas.", MAX_ATTEMPTS)
                raise

            logging.info(
                "Nova tentativa será realizada em %s segundos.",
                RETRY_DELAY_SECONDS,
            )
            time.sleep(RETRY_DELAY_SECONDS)


def create_scheduler() -> BlockingScheduler:
    """Cria um único job para executar todos os dias no horário configurado."""
    scheduler = BlockingScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(
        run_with_retry,
        trigger=CronTrigger(
            hour=SCHEDULE_HOUR,
            minute=SCHEDULE_MINUTE,
            timezone="America/Sao_Paulo",
        ),
        id="daily_price_monitoring",
        name="Coleta e transformação diária de preços",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    return scheduler


def main() -> None:
    """Configura os logs e mantém o agendador em execução."""
    configure_logging()
    scheduler = create_scheduler()
    logging.info(
        "Agendador iniciado. Execução diária programada para %02d:%02d.",
        SCHEDULE_HOUR,
        SCHEDULE_MINUTE,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Agendador encerrado.")


if __name__ == "__main__":
    main()
