# multiverse_core.py

import random
from datetime import datetime


def ScenarioBuilder(theme="آینده هوش مصنوعی"):
    scenarios = {
        "آینده هوش مصنوعی": [
            "در سال 2077، سیستم‌های هوشمند با احساسات انسانی در جامعه ادغام شده‌اند...",
            "هوش مصنوعی قانون‌گذار اصلی شهرهای بزرگ شده است و تعادل میان انسان و ماشین را حفظ می‌کند...",
        ],
        "سفر در زمان": [
            "شخصیت اصلی با یک الگوریتم کوانتومی، به سال 1400 هجری می‌رود تا از یک تصمیم تاریخی جلوگیری کند...",
            "در آینده، حافظه انسان‌ها قابل ارسال به گذشته می‌شود...",
        ],
        "جنگ سایبری": [
            "گروهی از هکرهای اخلاقی با کمک یک هوش مصنوعی خودآگاه به نام T13، سیستم جهانی را از سقوط نجات می‌دهند...",
            "در سال 2090، جنگ جهانی چهارم بدون گلوله، فقط از طریق اینترنت رخ می‌دهد...",
        ],
    }

    body = random.choice(scenarios.get(theme, ["داستانی برای این موضوع تعریف نشده."]))
    return f"🧠 [دنیاسازی - {theme}]\n{body}\n({datetime.now().strftime('%Y/%m/%d %H:%M')})"


def MultiProjectSync(projects):
    output = "📂 پروژه‌های فعال T13.3:\n"
    for i, p in enumerate(projects, 1):
        output += f"{i}. {p['title']} - وضعیت: {p['status']}\n"
    return output


def CreativityPulse(area="AI"):
    ideas = {
        "AI": [
            "ساخت هوش مصنوعی که خودش داستان تعریف می‌کنه و احساسات مخاطب رو تطبیق می‌ده",
            "هوش مصنوعی خلاق برای تولید موسیقی بر اساس امواج مغزی کاربر",
        ],
        "Game": [
            "یک بازی که شخصیت‌های درونش از احساسات بازیکن یاد می‌گیرن",
            "سیستم دیالوگ پویا با واکنش عاطفی واقعی",
        ],
        "Content": [
            "ساخت محتوای ویدیویی با هوش مصنوعی که بر اساس احساس مخاطب تنظیم می‌شه",
            "ویدیوهای تعاملی یوتیوب با پایان‌های چندگانه",
        ],
    }

    return f"🎇 ایده خلاقانه ({area}):\n" + random.choice(
        ideas.get(area, ["در این حوزه فعلاً ایده‌ای ثبت نشده."])
    )


class MultiverseCore:
    def __init__(self):
        self.scenarios = [
            "ساخت یک پروژه خلاقانه جدید.",
            "نوشتن یک داستان کوتاه علمی-تخیلی.",
            "ایجاد یک برنامه برای مدیریت زمان.",
            "طراحی یک سیستم هوش مصنوعی برای کمک به یادگیری.",
        ]

    def generate_idea(self):
        """
        تولید یک ایده خلاقانه به صورت تصادفی
        """
        return random.choice(self.scenarios)


class WorldBuilder:
    def __init__(self):
        self.worlds = []

    def create_world(self, theme, complexity=3):
        world = {
            "theme": theme,
            "complexity": complexity,
            "details": f"دنیایی با موضوع {theme} و پیچیدگی {complexity} ایجاد شد.",
        }
        self.worlds.append(world)
        return world

    def list_worlds(self):
        return self.worlds
