import discord
from discord.ext import commands, tasks
from discord import app_commands
import config
import asyncio
from flask import Flask
from threading import Thread
from keep_alive import keep_alive

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Dictionary to store ticket channels
ticket_channels = {}

# Helper untuk cek role
async def has_required_role(interaction: discord.Interaction):
    role = interaction.guild.get_role(config.STAFF_ROLE_ID)
    return role in interaction.user.roles

def is_staff(interaction: discord.Interaction) -> bool:
    staff_role = interaction.guild.get_role(config.STAFF_ROLE_ID)
    return staff_role in interaction.user.roles if staff_role else False

# Slash command setup_ticket
@bot.tree.command(name="setup_ticket", description="Setup sistem ticket (khusus staff)")
async def setup_ticket(interaction: discord.Interaction):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Kamu tidak punya izin untuk menggunakan command ini!", ephemeral=True)
        return
    embed = discord.Embed(
        title=config.TICKET_SETUP_MESSAGE["title"],
        description=config.TICKET_SETUP_MESSAGE["description"],
        color=config.TICKET_SETUP_MESSAGE["color"]
    )
    embed.set_image(url=config.WELCOME_RULES_GIF)
    button = discord.ui.Button(
        label=config.CREATE_TICKET_BUTTON,
        style=discord.ButtonStyle.primary,
        custom_id="create_ticket"
    )
    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)

# Slash command ambilrole
@bot.tree.command(name="ambilrole", description="Ambil role member (khusus staff)")
async def ambilrole(interaction: discord.Interaction):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Kamu tidak punya izin untuk menggunakan command ini!", ephemeral=True)
        return
    embed = discord.Embed(
        title="BM SHOP FIVEM SERVICES",
        description="Klik tombol di bawah untuk mendapatkan role <@&{0}>".format(config.MEMBER_ROLE_ID),
        color=discord.Color.blue()
    )
    embed.set_image(url=config.WELCOME_RULES_GIF)
    view = AmbilRoleView()
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    # Add persistent views
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
    bot.add_view(AmbilRoleView())
    
    # Load payment cog
    await bot.load_extension('payment')
    
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"Gagal sync slash command: {e}")
    print(f'{bot.user} telah siap!')
    update_status.start()

@tasks.loop(seconds=0)  # Loop tanpa delay, delay di-handle manual
async def update_status():
    channel = bot.get_channel(config.WELCOME_CHANNEL_ID)
    guild = channel.guild if channel else None
    if guild:
        member_count = guild.member_count
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"with {member_count} member"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BM SHOP #1 TERMURAH"))
        await asyncio.sleep(10)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    """Setup ticket system in the current channel"""
    embed = discord.Embed(
        title=config.TICKET_SETUP_MESSAGE["title"],
        description=config.TICKET_SETUP_MESSAGE["description"],
        color=config.TICKET_SETUP_MESSAGE["color"]
    )
    # Tambahkan GIF banned di bawah deskripsi
    embed.set_image(url="https://media.discordapp.net/attachments/1139786394554867732/1370302434051624990/standard_1.gif?ex=681f0117&is=681daf97&hm=cb9bb95bef907acd2e9c40742d3271ca931c3fefd024699a39b507342ea27ecd&=")
    
    # Create button
    button = discord.ui.Button(
        label=config.CREATE_TICKET_BUTTON,
        style=discord.ButtonStyle.primary,
        custom_id="create_ticket"
    )
    view = discord.ui.View()
    view.add_item(button)
    
    await ctx.send(embed=embed, view=view)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=config.CREATE_TICKET_BUTTON, style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user already has a ticket
        for channel_id in ticket_channels.values():
            channel = interaction.guild.get_channel(channel_id)
            if channel and channel.name == f"{config.TICKET_CHANNEL_PREFIX}{interaction.user.name.lower()}":
                await interaction.response.send_message("Anda sudah memiliki ticket yang aktif!", ephemeral=True)
                return

        # Create new ticket channel
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Add staff role permissions if configured
        if config.STAFF_ROLE_ID:
            staff_role = interaction.guild.get_role(config.STAFF_ROLE_ID)
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        # Get category if configured
        category = None
        if config.TICKET_CATEGORY_ID:
            category = interaction.guild.get_channel(config.TICKET_CATEGORY_ID)
        
        channel = await interaction.guild.create_text_channel(
            f"{config.TICKET_CHANNEL_PREFIX}{interaction.user.name}",
            overwrites=overwrites,
            category=category
        )
        
        ticket_channels[interaction.user.id] = channel.id
        
        embed = discord.Embed(
            title=config.TICKET_CREATED_MESSAGE["title"],
            description=config.TICKET_CREATED_MESSAGE["description"],
            color=config.TICKET_CREATED_MESSAGE["color"]
        )
        
        # Create close ticket button
        close_view = CloseTicketView()
        
        await channel.send(f"{interaction.user.mention}", embed=embed, view=close_view)
        await interaction.response.send_message(f"Ticket Anda telah dibuat di {channel.mention}", ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=config.CLOSE_TICKET_BUTTON, style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.channel.name.startswith(config.TICKET_CHANNEL_PREFIX):
            embed = discord.Embed(
                title=config.TICKET_CLOSED_MESSAGE["title"],
                description=config.TICKET_CLOSED_MESSAGE["description"],
                color=config.TICKET_CLOSED_MESSAGE["color"]
            )
            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(120)  # Tunggu 2 menit
            await interaction.channel.delete(reason="Ticket ditutup")
            
            # Remove from tracking
            user_id = next((k for k, v in ticket_channels.items() if v == interaction.channel.id), None)
            if user_id:
                del ticket_channels[user_id]

class AmbilRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ambil Role Member", style=discord.ButtonStyle.success, custom_id="ambil_role_member")
    async def ambil_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(config.MEMBER_ROLE_ID)
        if role:
            if role in interaction.user.roles:
                await interaction.response.send_message("Kamu sudah memiliki role Member!", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("Role Member berhasil ditambahkan!", ephemeral=True)
        else:
            await interaction.response.send_message("Role Member tidak ditemukan!", ephemeral=True)

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(config.WELCOME_CHANNEL_ID)
    if channel:
        # Pesan mention dan TAKE ROLE
        await channel.send(config.WELCOME_MESSAGE.format(mention=member.mention))
        # Embed rules
        embed = discord.Embed(
            title=config.WELCOME_RULES_TITLE,
            description=config.WELCOME_RULES_DESC,
            color=discord.Color.dark_gray()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1139786394554867732/1370302434051624990/standard_1.gif?ex=681f0117&is=681daf97&hm=cb9bb95bef907acd2e9c40742d3271ca931c3fefd024699a39b507342ea27ecd&=")
        await channel.send(embed=embed)

# Daftar produk yang diizinkan
PRODUCT_CHOICES = [
    app_commands.Choice(name=":rockstar_logo_for_tweets: Rockstar Account Fresh", value=":Rockstar_logo_for_tweets: Rockstar Account Fresh"),
    app_commands.Choice(name=":rockstar_logo_for_tweets: Rockstar Activation Codes", value=":Rockstar_logo_for_tweets: Rockstar Activation Codes")
]

# Fungsi autocomplete/choice produk
async def product_autocomplete(interaction: discord.Interaction, current: str):
    return [choice for choice in PRODUCT_CHOICES if current.lower() in choice.name.lower()]

@bot.tree.command(name="reps", description="Kirim feedback customer (public)")
@app_commands.describe(
    customer="Customer yang ingin direp (mention)",
    rating="Rating bintang (1-5)",
    review="Review singkat",
    product="Produk yang dibeli"
)
@app_commands.autocomplete(product=product_autocomplete)
async def reps(interaction: discord.Interaction, customer: discord.Member, rating: int, review: str, product: str):
    if rating < 1 or rating > 5:
        await interaction.response.send_message("Rating harus antara 1 sampai 5!", ephemeral=True)
        return
    stars = "⭐" * rating
    embed = discord.Embed(
        title=config.REPS_EMBED["title"],
        color=config.REPS_EMBED["color"]
    )
    embed.add_field(name="Customers", value=customer.mention, inline=True)
    embed.add_field(name="Rating", value=stars, inline=True)
    embed.add_field(name="Review", value=review, inline=False)
    embed.add_field(name="Product", value=product, inline=True)
    embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty)
    embed.set_footer(text=f"{interaction.user.display_name} • {interaction.created_at.strftime('%Y-%m-%d %H:%M')}")
    embed.set_image(url=config.WELCOME_RULES_GIF)

    # Kirim embed ke channel feedback khusus
    channel = interaction.guild.get_channel(config.FEEDBACK_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message("Feedback berhasil dikirim ke channel feedback!", ephemeral=True)
    else:
        await interaction.response.send_message("Channel feedback tidak ditemukan!", ephemeral=True)

# Fungsi autocomplete untuk payment_method
async def payment_method_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=method, value=method) for method in config.PAYMENT_METHODS.keys() if current.lower() in method.lower()]

# Slash command testi
@bot.tree.command(name="testi", description="Kirim testimoni transaksi (khusus staff)")
@app_commands.describe(
    seller="Penjual (mention)",
    buyer="Pembeli (mention)",
    product="Produk (pilih)",
    jumlah="Jumlah produk yang dibeli",
    price="Harga (cth: Rp. 150.000)",
    payment_method="Metode pembayaran",
    bukti="Bukti pembayaran (gambar)"
)
@app_commands.autocomplete(payment_method=payment_method_autocomplete, product=product_autocomplete)
async def testi(
    interaction: discord.Interaction,
    seller: discord.Member,
    buyer: discord.Member,
    product: str,
    jumlah: int,
    price: str,
    payment_method: str,
    bukti: discord.Attachment
):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Hanya staff yang bisa menggunakan command ini!", ephemeral=True)
        return
    embed = discord.Embed(
        description=(
            f"Thanks for purchasing in BM Shop #1 Termurah\n"
            f"Seller: {seller.mention}\n"
            f"Buyer: {buyer.mention}\n"
            f"Product: {product}\n"
            f"Jumlah: {jumlah}\n"
            f"Price: {price}\n"
            f"Payment Method: {payment_method}"
        ),
        title=config.TESTI_EMBED["title"],
        color=discord.Color.dark_blue()
    )
    embed.set_footer(text=config.TESTI_EMBED["footer"])
    # Thumbnail kanan atas: GIF banned
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1139786394554867732/1370345633218691206/static_1.png?ex=681f2952&is=681dd7d2&hm=5606fdb6f8812abbf2bf8bcbf446c44ac12b432732b87813f1233d51e19a2f75&")
    # Gambar utama: bukti pembayaran (jika ada)
    if bukti.content_type and bukti.content_type.startswith("image"):
        embed.set_image(url=bukti.url)
    channel = interaction.guild.get_channel(config.TESTI_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message("Testimoni berhasil dikirim!", ephemeral=True)
    else:
        await interaction.response.send_message("Channel testimoni tidak ditemukan!", ephemeral=True)

@bot.tree.command(name="giverole", description="Memberikan role ke member (khusus staff)")
@app_commands.describe(
    member="Member yang akan diberi role",
    role="Role yang akan diberikan"
)
async def giverole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Hanya staff yang bisa menggunakan command ini!", ephemeral=True)
        return
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ Berhasil menambahkan role {role.mention} ke {member.mention}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Gagal menambahkan role: {e}", ephemeral=True)

# Run the bot
bot.run(config.TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive() 