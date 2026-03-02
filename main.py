from apscheduler.schedulers.blocking import BlockingScheduler

from services.process_dlqs import process


def main() -> None:
    print("Starting the scheduler...")

    scheduler = BlockingScheduler()
    scheduler.add_job(process, "interval", seconds=10)
    scheduler.start()


if __name__ == "__main__":
    main()
