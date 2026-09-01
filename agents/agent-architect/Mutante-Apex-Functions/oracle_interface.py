import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apex_core import ApexCore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - ORACLE - %(levelname)s - %(message)s')
logger = logging.getLogger("ORACLE")

class OracleBot:
    def __init__(self, token: str, core: ApexCore):
        self.token = token
        self.core = core
        self.app = ApplicationBuilder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("think", self.cmd_think))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("👁️ Mutante Apex Functions - Interface Oráculo Ativa.")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        stats = self.core.telemetry.get_stats()
        msg = (f"📊 Status do Sistema:\n"
               f"CPU: {stats['cpu_usage']}%\n"
               f"RAM: {stats['ram_usage']}%\n"
               f"Uptime: {stats['uptime']:.0f}s")
        await update.message.reply_text(msg)

    async def cmd_think(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        prompt = " ".join(context.args) if context.args else "Quem é você?"
        response = await self.core.brain.think(prompt)
        await update.message.reply_text(f"🧠 Resposta: {response}")

    async def start(self):
        logger.info("Bot Oráculo Iniciando...")
        await self.app.initialize()
        await self.app.updater.start_polling()
        await self.app.start()

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    if token:
        core = ApexCore(gemini_key=os.getenv("GEMINI_API_KEY"))
        bot = OracleBot(token, core)
        loop = asyncio.get_event_loop()
        loop.create_task(core.start())
        loop.run_until_complete(bot.start())
        loop.run_forever()
    else:
        logger.error("TELEGRAM_TOKEN não encontrado.")
