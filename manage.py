import argparse
import asyncio
from create_bot import bot, dp, db
from handlers.start import start_router
from handlers.login import login_router

async def run_bot():
    dp.include_router(start_router)
    dp.include_router(login_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Управление приложением")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    migrate_parser = subparsers.add_parser("migrate", help="Управление миграциями")
    migrate_subparsers = migrate_parser.add_subparsers(dest="subcommand", help="Действия с миграциями")

    up_parser = migrate_subparsers.add_parser("up", help="Применить миграции")
    up_parser.add_argument("--from", type=int, dest="from_version", help="Начальная версия миграции")
    up_parser.add_argument("--to", type=int, dest="to_version", help="Конечная версия миграции")

    down_parser = migrate_subparsers.add_parser("down", help="Откатить миграции")
    down_parser.add_argument("--from", type=int, dest="from_version", help="Начальная версия миграции")
    down_parser.add_argument("--to", type=int, dest="to_version", help="Конечная версия миграции")

    status_parser = subparsers.add_parser("runbot", help="Запустить бота")

    args = parser.parse_args()

    if args.command == "runbot":
        asyncio.run(run_bot())

    if args.command == "migrate":
        if args.subcommand == "up":
            db.migrate_up(migrate_from=args.from_version, migrate_to=args.to_version)
        elif args.subcommand == "down":
            db.migrate_down(migrate_from=args.from_version, migrate_to=args.to_version)
