import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from database import create_tables, get_connection

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Daromad"), KeyboardButton(text="Harajat")],
        [KeyboardButton(text="Bank"), KeyboardButton(text="Kassa")],
        [KeyboardButton(text="Statistika"), KeyboardButton(text="Hisobot")],
        [KeyboardButton(text="Qarzlar"), KeyboardButton(text="Jamgarma")],
        [KeyboardButton(text="🗑️ O'chir"), KeyboardButton(text="Sozlamalar")]
    ],
    resize_keyboard=True
)

user_state = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🚀 Asosiy menyu", reply_markup=main_menu)

@dp.message(F.text == "Daromad")
async def daromad(message: types.Message):
    user_state[message.from_user.id] = "kalla_soni"
    await message.answer("📥 Bugun nechta kalla ajratdingiz?", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Harajat")
async def harajat(message: types.Message):
    user_state[message.from_user.id] = "harajat_izoh"
    await message.answer("💰 Harajat uchun izoh yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Kassa")
async def kassa_menu(message: types.Message):
    kassa_menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Kassaga pul tushdi"), KeyboardButton(text="Kassadan pul chiqdi")],
            [KeyboardButton(text="Kassadagi pul miqdori")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    await message.answer("💵 Kassa bo'limi", reply_markup=kassa_menu_kb)

@dp.message(F.text == "Kassaga pul tushdi")
async def kassa_tushdi(message: types.Message):
    user_state[message.from_user.id] = "kassa_tushdi_izoh"
    await message.answer("💵 Izoh yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Kassadan pul chiqdi")
async def kassa_chiqdi(message: types.Message):
    user_state[message.from_user.id] = "kassa_chiqdi_izoh"
    await message.answer("💸 Izoh yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Kassadagi pul miqdori")
async def kassa_balans(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(summa) FROM kassa")
    total = cursor.fetchone()[0] or 0
    conn.close()
    await message.answer(f"💵 Kassadagi pul: {total:,} so'm", reply_markup=main_menu)

@dp.message(F.text == "Qarzlar")
async def qarzlar_menu(message: types.Message):
    qarz_menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Qarz berdim"), KeyboardButton(text="Qarz qaytardi")],
            [KeyboardButton(text="Barcha qarzlar ro'yxati")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    await message.answer("📌 Qarzlar bo'limi", reply_markup=qarz_menu_kb)

@dp.message(F.text == "Qarz berdim")
async def qarz_berdim(message: types.Message):
    user_state[message.from_user.id] = "qarz_ism"
    await message.answer("📌 Ism yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Qarz qaytardi")
async def qarz_qaytardi(message: types.Message):
    user_state[message.from_user.id] = "qarz_qaytar_ism"
    await message.answer("📌 Ism yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Barcha qarzlar ro'yxati")
async def qarzlar_royxati(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ism, SUM(qarz_miqdori) FROM qarzlar GROUP BY ism")
    qarzlar = cursor.fetchall()
    total_qarz = 0
    for i, m in qarzlar: total_qarz += m
    conn.close()
    if not qarzlar:
        await message.answer("📭 Qarz yo'q.", reply_markup=main_menu)
    else:
        text = "📌 Barcha qarzlar:\n"
        for ism, miqdor in qarzlar:
            text += f"• {ism}: {miqdor:,} so'm\n"
        text += f"\n💰 Jami: {total_qarz:,} so'm"
        await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "Bank")
async def bank_menu(message: types.Message):
    bank_menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Bankga pul tushdi"), KeyboardButton(text="Bankdan pul chiqdi")],
            [KeyboardButton(text="Bankdagi pul miqdori")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    await message.answer("🏦 Bank bo'limi", reply_markup=bank_menu_kb)

@dp.message(F.text == "Bankga pul tushdi")
async def bank_tushdi(message: types.Message):
    user_state[message.from_user.id] = "bank_tushdi_izoh"
    await message.answer("🏦 Izoh yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Bankdan pul chiqdi")
async def bank_chiqdi(message: types.Message):
    user_state[message.from_user.id] = "bank_chiqdi_izoh"
    await message.answer("💳 Izoh yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Bankdagi pul miqdori")
async def bank_balans(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(summa) FROM bank")
    total = cursor.fetchone()[0] or 0
    conn.close()
    await message.answer(f"🏦 Bankdagi pul: {total:,} so'm", reply_markup=main_menu)

@dp.message(F.text == "Statistika")
async def statistika(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(jami) FROM daromad")
    total_daromad = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(summa) FROM harajat")
    total_harajat = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(summa) FROM kassa")
    total_kassa = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(summa) FROM bank")
    total_bank = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(summa) FROM jamgarma")
    total_jamgarma = cursor.fetchone()[0] or 0
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(jami) FROM daromad WHERE DATE(sana) = ?", (today,))
    today_daromad = cursor.fetchone()[0] or 0
    conn.close()
    await message.answer(
        f"📊 **UMUMIY STATISTIKA**\n\n"
        f"💰 **Jami daromad:** {total_daromad:,} so'm\n"
        f"💸 **Jami harajat:** {total_harajat:,} so'm\n"
        f"📈 **Sof foyda:** {total_daromad - total_harajat:,} so'm\n\n"
        f"💵 **Kassadagi pul:** {total_kassa:,} so'm\n"
        f"🏦 **Bankdagi pul:** {total_bank:,} so'm\n"
        f"💰 **Jamg'arma:** {total_jamgarma:,} so'm\n\n"
        f"📅 **Bugungi daromad:** {today_daromad:,} so'm",
        parse_mode="Markdown",
        reply_markup=main_menu
    )

@dp.message(F.text == "Hisobot")
async def hisobot(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kalla_soni, jami, sana FROM daromad ORDER BY id DESC LIMIT 3")
    d = cursor.fetchall()
    cursor.execute("SELECT izoh, summa, sana FROM harajat ORDER BY id DESC LIMIT 3")
    h = cursor.fetchall()
    conn.close()
    text = "📋 Oxirgi 3 daromad:\n"
    for k, j, s in d:
        text += f"• {k} ta kalla → {j:,} so'm ({s})\n"
    text += "\n📋 Oxirgi 3 harajat:\n"
    for i, s, t in h:
        text += f"• {i} → {s:,} so'm ({t})\n"
    await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "Jamgarma")
async def jamgarma(message: types.Message):
    jamgarma_menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Jamg'armaga pul qo'shish"), KeyboardButton(text="Jamg'arma balansi")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
    await message.answer("💰 **Jamg'arma bo'limi**\n\nJamg'armangizga pul qo'shing yoki balansni ko'ring.", parse_mode="Markdown", reply_markup=jamgarma_menu_kb)

@dp.message(F.text == "Jamg'armaga pul qo'shish")
async def jamgarma_qoshish(message: types.Message):
    user_state[message.from_user.id] = "jamgarma_izoh"
    await message.answer("💰 Jamg'armaga pul qo'shish uchun izoh yozing (masalan: 'Yangi mashina uchun'):", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Jamg'arma balansi")
async def jamgarma_balans(message: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(summa) FROM jamgarma")
    total = cursor.fetchone()[0] or 0
    conn.close()
    await message.answer(f"💰 **Jamg'arma balansi:** {total:,} so'm", parse_mode="Markdown", reply_markup=main_menu)

@dp.message(F.text == "🗑️ O'chir")
async def delete_last(message: types.Message):
    user_state[message.from_user.id] = "delete_wait"
    await message.answer("❗ O'chirish uchun:\n\n'Daromadni ochir' deb yozing (Daromad uchun)\n'Harajatni ochir' deb yozing (Harajat uchun)", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text == "Daromadni ochir")
async def delete_daromad(message: types.Message):
    if user_state.get(message.from_user.id) == "delete_wait":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM daromad WHERE id = (SELECT MAX(id) FROM daromad)")
        conn.commit()
        conn.close()
        user_state[message.from_user.id] = None
        await message.answer("✅ Daromaddagi oxirgi yozuv o'chirildi!", reply_markup=main_menu)

@dp.message(F.text == "Harajatni ochir")
async def delete_harajat(message: types.Message):
    if user_state.get(message.from_user.id) == "delete_wait":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM harajat WHERE id = (SELECT MAX(id) FROM harajat)")
        conn.commit()
        conn.close()
        user_state[message.from_user.id] = None
        await message.answer("✅ Harajatdagi oxirgi yozuv o'chirildi!", reply_markup=main_menu)

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)

    if state == "kalla_soni":
        try:
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            kalla_soni = int(matn)
            jami = kalla_soni * 18000
            sana = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO daromad (kalla_soni, narx, jami, sana) VALUES (?, 18000, ?, ?)", (kalla_soni, jami, sana))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Saqlandi! Jami: {jami:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "harajat_izoh":
        user_state[user_id] = f"harajat_summa:{message.text}"
        await message.answer("💸 Summa yozing:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("harajat_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO harajat (izoh, summa, sana) VALUES (?, ?, ?)", (izoh, summa, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Harajat: {izoh} - {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "kassa_tushdi_izoh":
        user_state[user_id] = f"kassa_tushdi_summa:{message.text}"
        await message.answer("💵 Summa yozing:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("kassa_tushdi_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kassa (summa, sana, izoh) VALUES (?, ?, ?)", (summa, datetime.now().strftime("%Y-%m-%d %H:%M"), izoh))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Kassa tushdi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "kassa_chiqdi_izoh":
        user_state[user_id] = f"kassa_chiqdi_summa:{message.text}"
        await message.answer("💸 Summa yozing:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("kassa_chiqdi_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kassa (summa, sana, izoh) VALUES (?, ?, ?)", (-summa, datetime.now().strftime("%Y-%m-%d %H:%M"), izoh))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Kassa chiqdi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "qarz_ism":
        user_state[user_id] = f"qarz_summa:{message.text}"
        await message.answer("📌 Qancha pul berdingiz?:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("qarz_summa:"):
        try:
            ism = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO qarzlar (ism, qarz_miqdori, sana) VALUES (?, ?, ?)", (ism, summa, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Qarz berildi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "qarz_qaytar_ism":
        user_state[user_id] = f"qarz_qaytar_summa:{message.text}"
        await message.answer("📌 Qancha pul qaytardi?:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("qarz_qaytar_summa:"):
        try:
            ism = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO qarzlar (ism, qarz_miqdori, sana) VALUES (?, ?, ?)", (ism, -summa, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Qarz qaytarildi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "bank_tushdi_izoh":
        user_state[user_id] = f"bank_tushdi_summa:{message.text}"
        await message.answer("🏦 Summa yozing:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("bank_tushdi_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bank (summa, sana, izoh) VALUES (?, ?, ?)", (summa, datetime.now().strftime("%Y-%m-%d %H:%M"), izoh))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Bank tushdi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "bank_chiqdi_izoh":
        user_state[user_id] = f"bank_chiqdi_summa:{message.text}"
        await message.answer("💳 Summa yozing:", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("bank_chiqdi_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bank (summa, sana, izoh) VALUES (?, ?, ?)", (-summa, datetime.now().strftime("%Y-%m-%d %H:%M"), izoh))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Bank chiqdi: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif state == "jamgarma_izoh":
        user_state[user_id] = f"jamgarma_summa:{message.text}"
        await message.answer("💰 Qancha pul qo'shmoqchisiz? (Faqat son yozing):", reply_markup=ReplyKeyboardRemove())

    elif state and state.startswith("jamgarma_summa:"):
        try:
            izoh = state.split(":")[1]
            matn = message.text.strip()
            if not matn.isdigit():
                await message.answer("❌ Iltimos, faqat son kiriting!")
                return
            summa = int(matn)
            sana = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jamgarma (summa, sana) VALUES (?, ?)", (summa, sana))
            conn.commit()
            conn.close()
            user_state[user_id] = None
            await message.answer(f"✅ Jamg'armaga pul qo'shildi!\n\nIzoh: {izoh}\nSumma: {summa:,} so'm", reply_markup=main_menu)
        except Exception as e:
            await message.answer(f"❌ Xatolik: {str(e)}")

    elif message.text == "⬅️ Orqaga":
        await message.answer("Asosiy menyu.", reply_markup=main_menu)
    else:
        await message.answer("Menyudan birini tanlang 👇", reply_markup=main_menu)

async def main():
    create_tables()
    print("🚀 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())