import os
from dotenv import load_dotenv

# =====================
# 1. ENV & BOT CONFIG
# =====================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '/'

# =====================
# 2. ROLE & CATEGORY ID
# =====================
TICKET_CATEGORY_ID = 1370112549827121315  # ID kategori untuk ticket
STAFF_ROLE_ID = 1370110008120967329       # ID role staff
MEMBER_ROLE_ID = 1370110443313697030      # ID role member
REQUIRED_ROLE_ID = None                   # ID role yang diperlukan untuk open ticket (opsional)

# =====================
# 3. WARNA EMBED
# =====================
EMBED_COLOR = 0x3498db    # Biru utama
SUCCESS_COLOR = 0x2ecc71  # Hijau sukses
ERROR_COLOR = 0xe74c3c    # Merah error

# =====================
# 4. TICKET SYSTEM
# =====================
TICKET_CHANNEL_PREFIX = "ticket-"
TICKET_SETUP_MESSAGE = {
    "title": "🎫 Sistem Ticket",
    "description": "Klik tombol di bawah untuk membuat ticket",
    "color": EMBED_COLOR
}
TICKET_CREATED_MESSAGE = {
    "title": "Ticket Dibuat",
    "description": "Ticket Anda telah dibuat. Staff akan segera membantu Anda.\n\n/payment Untuk Melakukan Pembayaran\n/reps Untuk Memberikan Rating",
    "color": SUCCESS_COLOR
}
TICKET_CLOSED_MESSAGE = {
    "title": "Ticket Ditutup",
    "description": "Ticket ini akan ditutup dalam 2 menit...",
    "color": ERROR_COLOR
}
NO_ROLE_MESSAGE = {
    "title": "❌ Akses Ditolak",
    "description": "Anda tidak memiliki role yang diperlukan untuk membuat ticket.",
    "color": ERROR_COLOR
}
CREATE_TICKET_BUTTON = "Buat Ticket"
CLOSE_TICKET_BUTTON = "Tutup Ticket"

# =====================
# 5. WELCOME SYSTEM
# =====================
WELCOME_CHANNEL_ID = 1370111539985645579  # ID channel welcome
WELCOME_MESSAGE = "Hey {mention} welcome to Boy Shop !!!\nTAKE ROLE <#1370111684852584488>"
WELCOME_RULES_TITLE = "RULES Boy Shop"
WELCOME_RULES_DESC = (
    "```\n"
    "1. DILARANG RASIS DAN BERLEBIHAN\n"
    "2. PROMOSI PADA TEMPAT NYA\n"
    "3. DILARANG SHARE BERBAU PRONO BERUPA [LINK, FOTO, VIDIO, STICKER]\n"
    "4. SUDAH DEPOSIT TIDAK BISA BACK\n\n"
    "MELANGGAR DI ATAS BERARTI SUDAH MENERIMA  FREKUENSI"
    "```"
)
WELCOME_RULES_GIF = "https://media.discordapp.net/attachments/1139786394554867732/1370302434051624990/standard_1.gif?ex=681f0117&is=681daf97&hm=cb9bb95bef907acd2e9c40742d3271ca931c3fefd024699a39b507342ea27ecd&=" 

# =====================
# 6. REPS/FEEDBACK SYSTEM
# =====================
REPS_EMBED = {
    "title": "Feedback Terkirim",
    "color": 0xffc300  # Warna emas
}
REPS_FOOTER = "Feedback System"

FEEDBACK_CHANNEL_ID = 1370137606481907712 

# =====================
# 7. PAYMENT SYSTEM
# =====================
PAYMENT_CHANNEL_ID = 1370137606481907712  # ID channel untuk payment
PAYMENT_EMBED = {
    "title": "💳 Sistem Pembayaran",
    "description": "Berikut adalah metode pembayaran yang tersedia:",
    "color": 0x00ff00  # Warna hijau
}

PAYMENT_METHODS = {
    "DANA": {
        "number": "082298234855",
        "name": "wiwxx",
        "image": "https://example.com/dana.png"  # URL gambar QR DANA
    }
}

PAYMENT_FOOTER = "Pastikan untuk mengirim bukti pembayaran ke staff" 

# =====================
# 8. TESTI SYSTEM
# =====================
TESTI_EMBED = {
    "title": "BM Shop #1 Termurah",
    "footer": "BM Shop #1 Termurah"
}
TESTI_CHANNEL_ID = 1370264594878038077  # Ganti dengan ID channel untuk menampung testimoni
TESTI_BANNED_GIF = "https://media.discordapp.net/attachments/1139786394554867732/1370302434051624990/standard_1.gif?ex=681f0117&is=681daf97&hm=cb9bb95bef907acd2e9c40742d3271ca931c3fefd024699a39b507342ea27ecd&=" 