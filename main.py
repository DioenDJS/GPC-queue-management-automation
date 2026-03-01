from apscheduler.schedulers.blocking import BlockingScheduler

def test_schedule():
    print("test..")

def main() -> None:
    print("Starting the scheduler...")

    scheduler = BlockingScheduler()
    scheduler.add_job(test_schedule, 'interval', seconds=10)
    scheduler.start()

if __name__ == "__main__":
    main()