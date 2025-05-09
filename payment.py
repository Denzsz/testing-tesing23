import discord
from discord import app_commands
from discord.ext import commands
import config

class Payment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="payment", description="Menampilkan informasi pembayaran")
    async def payment(self, interaction: discord.Interaction):
        # Cek apakah command digunakan di channel ticket
        if not interaction.channel.name.startswith(config.TICKET_CHANNEL_PREFIX):
            await interaction.response.send_message("❌ Command ini hanya bisa digunakan di channel ticket!", ephemeral=True)
            return

        # Membuat embed untuk payment
        embed = discord.Embed(
            title=config.PAYMENT_EMBED["title"],
            description=config.PAYMENT_EMBED["description"],
            color=config.PAYMENT_EMBED["color"]
        )

        # Menambahkan warning message
        warning_text = (
            "⚠️ **PERINGATAN PENTING** ⚠️\n\n"
            "Payment yang valid hanya dari:\n"
            "<@1139782740338823199> dan <@1260556494332624947>\n\n"
            "**PERHATIAN**: Kami tidak bertanggung jawab atas segala bentuk scam atau kerugian yang terjadi jika Anda melakukan pembayaran ke selain staff yang disebutkan di atas!"
        )
        embed.add_field(name="", value=warning_text, inline=False)

        # Menambahkan field untuk setiap metode pembayaran
        for method, details in config.PAYMENT_METHODS.items():
            embed.add_field(
                name=f"💳 {method}",
                value=f"Nomor: `{details['number']}`\nAtas Nama: `{details['name']}`",
                inline=False
            )
            # Jika ada gambar QR, tambahkan sebagai thumbnail
            if details.get('image'):
                embed.set_image(url=details['image'])

        embed.set_footer(text=config.PAYMENT_FOOTER)
        
        # Kirim embed
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Payment(bot)) 