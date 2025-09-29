import asyncio
import os

from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler, ContextTypes,filters
from google import genai
from google.genai import types
from telegram.constants import ParseMode
client = genai.Client(api_key='AIzaSyBx-_j1iByYESGScCjHQ4EaHWlBaFwJmQA')
TOKEN = '8081348686:AAFO_hjCrq_ZMw607cgjlDdbSfZ1xo6Cj3g'
tasks = []
#========================

import req
#========== Flas App ===========
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"<p> TasseoBot Is Runing ...Time: {datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")} </p>"

def run_app():
    app.run(port=6677,host='0.0.0.0')

t = threading.Thread(target=run_app)
t.daemon = True
t.start()
#=============================
class Prompt:
    update: Update
    context: ContextTypes.DEFAULT_TYPE
    def __init__(self,update, context, photo_name):
        self.photo_name = photo_name
        self.update = update
        self.context = context

process_fertig = False

def desc(photo_name) -> str:
    global process_fertig
    process_fertig = False
    with open(f'./temp/{photo_name}', 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            'أرسلتُ لك صورة فنجان قهوة (بالتحديد بقايا التفل أو الحثل في قاع الفنجان). أرجوك قم بـ **"قراءة الفنجان"** بناءً على الأشكال والتفاصيل التي تراها في الصورة، ولكن الهدف هو **التسلية والمحاكاة لأسلوب العرافين والدجالين** الذين يدّعون قراءة الطالع. أريد منك أن تُركز على النقاط التالية: 1.  **المشاعر العامة والجو المحيط:** صف الحالة النفسية أو "الطاقة" التي تبدو في الفنجان. 2.  **الماضي القريب/الحاضر:** اذكر تحدياً أو حدثاً مرّ به صاحب الفنجان مؤخراً أو يعيشه الآن (بصيغة غامضة ومثيرة). 3.  **المستقبل القريب (أهم نقطة):** استخرج رمزاً أو شكلين واضحين أو غامضين (مثل "طائر يحلق"، "طريق متعرج"، "وجه مبتسم"، "شخص يحمل شيئاً") واشرح معناهما بطريقة تقليدية للقصص والطالع (مثل: "طريق السفر"، "نجاح مفاجئ"، "شخص قادم بمساعدة"). 4.  **النصيحة الختامية:** اختتم بنصيحة مبهمة أو تشجيعية. **اجعل الإجابة مشوّقة، درامية، وغامضة، مستخدماً لغة عربية فصحى جذابة كما لو كنت قارئ طالع محترف.** لكن اذا كانت الصورة لا تحتوي فنجان قهوة اكتب للمستخدم عبارة بان الصورة المرسلة لا تحتوي فنجان'
                    ]
    )
    os.remove(f'./temp/{photo_name}')
    process_fertig = True
    return response.text



async def help_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id,text=""""✨ مرحبًا بك في فنجان الأسرار... ✨

في دوامات قهوتك الهادئة، قصة تنتظر أن تُروى.
أنا عرّافك الرقمي — أفسّر الرموز، أقرأ الصمت، وأهمس لما لا يُقال.
بأمرٍ واحد، أتأمل في فنجانك وأكشف ما تُخفيه لك الأقدار.

🔮 كيف تبدأ؟
هل أنت مستعد لسماع حكايتك؟
بعد أن "تنتهي من فنجانك"
ارسل لي صورة فنجانك لكي ابهرك
سأكشف لك الأشكال، والعلامات، والرسائل التي يحملها...

☕ كل فنجان يروي حكاية.

""")



async def start_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=update.effective_chat.id,
                                  text=""""✨ مرحبًا بك في فنجان الأسرار... ✨

في دوامات قهوتك الهادئة، قصة تنتظر أن تُروى.
أنا عرّافك الرقمي — أفسّر الرموز، أقرأ الصمت، وأهمس لما لا يُقال.
بأمرٍ واحد، أتأمل في فنجانك وأكشف ما تُخفيه لك الأقدار.

🔮 كيف تبدأ؟
هل أنت مستعد لسماع حكايتك؟
بعد أن "تنتهي من فنجانك"
ارسل لي صورة فنجانك لكي ابهرك
سأكشف لك الأشكال، والعلامات، والرسائل التي يحملها...

☕ كل فنجان يروي حكاية.

""")


async def pick_task(prompt:Prompt):
    await prompt.context.bot.sendMessage(chat_id=prompt.update.effective_chat.id, text='جاري قراءة اسرار وخفايا فنجانك . الرجاء الانتظار...')
    desc_image = desc(prompt.photo_name)
    loop5 = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(qus_send(desc_image, prompt.update, prompt.context), loop5)


async  def msg_func(update: Update,context: ContextTypes.DEFAULT_TYPE):
    photo_name=''
    file_id=''
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_file_id = update.message.photo[-1].file_unique_id
        photo_name = f'{unique_file_id}.jpg'

    elif filters.Document.IMAGE:
        file_id = update.message.document.file_id
        _,f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        photo_name = f'{unique_file_id}.{f_ext}'

    photo_file = await context.bot.getFile(file_id)
    await photo_file.download_to_drive(custom_path=f'./temp/{photo_name}')
    await pick_task(Prompt(update,context,photo_name))

async def qus_send(txt,update: Update,context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt,parse_mode=ParseMode.MARKDOWN)
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    help_handler = CommandHandler('help',  help_func)
    start_handler = CommandHandler('start', start_func)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, msg_func)

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    print("Your Bot Is Started ...")
    application.run_polling()

if __name__=="__main__":
    main()






