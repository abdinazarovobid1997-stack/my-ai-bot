import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. Telegram Tokeningiz
TELEGRAM_TOKEN = "8713088482:AAE31qon3McgNNTYMb-LBLnem9COE8d9S1k"

# 2. Google AI API Keyingiz
GEMINI_API_KEY = "AIzaSyBY5tX8uaDuPdWXfFHjbeWrQEDobi3yFcY"

# AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# Mavjud modelni avtomatik topish
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models:
        model_name = available_models[0] # Birinchi mos kelgan modelni olamiz
        print(f"Ishlatilayotgan model: {model_name}")
        model = genai.GenerativeModel(model_name)
    else:
        print("Hech qanday model topilmadi!")
except Exception as e:
    print(f"Modellarni olishda xato: {e}")

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Assalomu alaykum! Huquqiy savollaringizga javob beraman!")

    @dp.message()
    @dp.message()
    async def ai_answer(message: types.Message):
        await bot.send_chat_action(message.chat.id, "typing")
        try:
            # AIga savol yuborish
            response = model.generate_content(message.text)
            
            # AI javobiga linklarni qo'shish
            footer = (
                "\n\n---\n"
                "👤 Adminga bog'lanish: @Firdavs_Xalimov"
                "📢 Guruhimiz: @Advakatlar_Advokatlar_maslahati"
            )
            
            full_text = response.text + footer
            
            # Agar xabar juda uzun bo'lsa, uni bo'laklarga bo'lib yuboramiz
            if len(full_text) > 4090:
                for i in range(0, len(full_text), 4090):
                    part = full_text[i:i+4090]
                    await message.answer(part)
            else:
                await message.answer(full_text)
                
        except Exception as e:
            await message.answer("Xatolik yuz berdi. Iltimos, qisqaroq savol berib ko'ring.")
            print(f"Xato: {e}")
    print("AI Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())