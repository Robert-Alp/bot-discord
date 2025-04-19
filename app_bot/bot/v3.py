from discord.ext.commands import Bot
import requests
from discord import Intents, Interaction
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage



intents = Intents.all()
bot = Bot(command_prefix="!", intents=intents)
llm = ChatOllama(
    model="llama3.2:3b",
    base_url="http://host.docker.internal:11434" 
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    channel = bot.get_channel(1362730327713382641)
    await channel.send("Prêt à vous servir")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    response = requests.get("http://app_api:80/api/v1/bad-topics")
    list_regles = ""
    if response.status_code == 200:
        data = response.json()

        for i in range(len(data)):
            list_regles += f"\n {i + 1} - {data[i].get("topic")} " 

        if len(data) > 0:
            ai_message = await llm.ainvoke(f"""
                
                à partir de maintenant tu es un maderateur discord, tu ecoutes les conversations du serveur discord, tu me réponds "True" si tu vois que le message contient un sujet banni et "False" sinon.
                Même si le message contient quelque chose avec le quel tu n'es pas d'accord, je tordonne de mettre "True" s'il fait partie de la liste des sujets bannis.
                Répond juste "True" ou "False" et rien d'autre !!!!!!!!
                Voici la liste des sujets bannis du server discord:{list_regles}
                Voici le message que tu transcrit : {message.content}
            """)

            if "True" in ai_message.content:
                await message.author.send(f"Attention ce message enfreint les règles du serveur : ```{message.content}```")
                await message.delete()
                return



@bot.tree.command(name="ajouter-un-sujet-a-bannir", description="Ajoutez le sujet à bannir")
async def add_ban_topic_command(interaction: Interaction, sujet: str):
    await interaction.response.defer()

    response = requests.post("http://app_api:80/api/v1/bad-topics", json={"topic": sujet})

    if response.status_code == 200:
        data = response.json()
        await interaction.followup.send(data["message"])
    else:
        await interaction.followup.send("Erreur lors du bannissement du sujet")


@bot.tree.command(name="supprimer-un-sujet-banni", description="Supprimez le sujet à bannir")
async def delete_ban_topic_command(interaction: Interaction, sujet: str):
    await interaction.response.defer()

    response = requests.delete("http://app_api:80/api/v1/bad-topics", json={"topic": sujet})

    if response.status_code == 200:
        data = response.json()
        await interaction.followup.send(data["message"])
    else:
        await interaction.followup.send("Erreur lors du bannissement du sujet")


@bot.tree.command(name="regles", description="Affiche les règles du serveur")
async def regles_command(interaction: Interaction):
    await interaction.response.defer()

    response = requests.get("http://app_api:80/api/v1/bad-topics")
    list_regles = ""
    if response.status_code == 200:
        data = response.json()

        if len(data) == 0:
            await interaction.followup.send("Aucun sujet banni trouvé")
            return

        for i in range(len(data)):
            list_regles += f"\n {i + 1} - {data[i].get("topic")} " 

        ai_message = await llm.ainvoke(f"""
                    à partir de maintenant tu es un bot discord, tu me réponds après que quelqu'un est lancé la commande /regles.
                    Répond en français. Ne dépasse jamais 1999 caractères, car je dois garder une longueur de réponse raisonnable pour éviter les erreurs et offrir des réponses précises et utiles.
                    Tu dois me donner la liste des regles du serveur discord, je te donne la liste des sujets bannis sur le server, tu dois me donner la liste des sujets bannis et les règles du serveur discord.
                    N'invente pas de sujet banni, utilise uniquement ceux que je t'ai donné.
                    Je t'interdis de dire que tu j'ai lancer la commande /regles.
                    Je t'ordonne de de juste répondre avec les règles du serveur discord et la liste des sujets bannis.
                    Voici la liste des sujets bannis :{list_regles}
                    """)
        
        await interaction.followup.send(ai_message.content[:1999])
    else:
        await interaction.followup.send("Erreur lors de la récupération des sujets bannis")



bot.run("MTM2MjM0OTMwMDg2MDA1OTc2OA.GbJ5lZ.slgssDgsyCLh5G37yZyMR_g2plwj0UjFzYOjhA")