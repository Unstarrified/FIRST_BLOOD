import json
from datetime import datetime, timezone
from typing import Any, List

import disnake
from disnake.ext import commands

class Job:
    class Skill:
        def __init__(self, job: "Job", data: dict) -> None:
            self._data = data
            self.source = job
            self.name = data["name"]
            self.description = data["description"]
            self.type = data["type"]
            self.image = data.get("image")
            self.position = data["position"]
            if data["damage"] != 0:
                self.damage = data["damage"]
            else:
                self.damage = None
            self.range = data["range"]
            if self.type == "active":
                self.cooldown = data["cooldown"]
            else:
                self.cooldown = None
            self.special = data["special"]


    def __init__(self, episode: Any, data: dict) -> None:
        self._data = data
        self.source = episode
        self.name = data["name"]
        self.person = data["person"]
        self.description = data["description"]
        self.emoji = data["emote"]
        self.emote = data["emote"]
        self.icon = data["image"]
        self.image = data.get("big_image")
        color = data["color"].replace("#", "")
        color = color.replace("0x", "")
        color = int(color, 16)
        self.color = disnake.Colour(color)
        self.skills = []
        for skill in data["skills"]:
            self.skills.append(self.Skill(self, skill))


class SkillSelection(disnake.ui.View):
    class SkillSelect(disnake.ui.StringSelect):
        def __init__(self, skills: List[Job.Skill]) -> None:
            self.skills = skills
            options = []
            for skill in skills:
                option = disnake.SelectOption(label=skill.name, description=f"{skill.description[:95]}...", value=str(self.skills.index(skill)), emoji="🌟")
                options.append(option)
            super().__init__(placeholder="정보를 확인할 스킬을 선택해주세요.", options=options, max_values=1, min_values=1, disabled=False)
        
        async def callback(self, inter: disnake.MessageInteraction) -> None:
            embed = skill_embed(self.view.inter.bot, self.skills[int(self.values[0])])
            await inter.response.edit_message(embed=embed)


    def __init__(self, job: Job) -> None:
        super().__init__(timeout=None)
        self.inter = None
        self.add_item(self.SkillSelect(job.skills))
    
    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        return self.inter.author == inter.author
    
    @disnake.ui.button(label="직업 정보로 돌아가기", style=disnake.ButtonStyle.blurple, emoji="⏮️", row=1)
    async def _back(self, button: disnake.ui.Button, inter: disnake.MessageInteraction) -> None:
        embed = job_embed(self.job)
        await inter.response.edit_message(embed=embed, view=None)
    
    @disnake.ui.button(label="열람 끝내기", style=disnake.ButtonStyle.red, emoji="⏹️", row=1)
    async def _end(self, button: disnake.ui.Button, inter: disnake.MessageInteraction) -> None:
        embed = disnake.Embed(description="곧 연구 보고서 뷰어가 종료됩니다.", color=0xFF0000)
        embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=self.inter.bot.user.display_avatar.url)
        await inter.response.edit_message(embed=embed)
        msg = await self.inter.original_response()
        await msg.delete(delay=1)
        self.stop()


def fetch_job(episode: Any, code: str) -> Job:
    data = json.load(open("src/jobs.json", "r", encoding="utf-8"))
    job = data[episode._season][episode._name][episode._number][code]
    job = Job(episode, job)
    return job

def job_view(bot: commands.Bot, job: Job) -> List[Any]:
    embed = job_embed(bot, job)
    view = SkillSelection(job)
    return embed, view

def job_embed(bot: commands.Bot, job: Job) -> disnake.Embed:
    embed = disnake.Embed(title=job.name, description=job.description, color=job.color, timestamp=datetime.now(timezone.utc))
    embed.set_author(name=f"불새위키 - {job.source.name}", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
    embed.set_footer(text=job.source.quote, icon_url=bot.user.display_avatar.url)
    embed.set_thumbnail(url=job.icon)
    if job.image is not None:
        embed.set_image(url=job.image)
    embed.add_field(name="역할군 주인", value=job.person)
    embed.add_field(name="스킬", value=f"{len(job.skills)}개")
    return embed

def skill_embed(bot: commands.Bot, skill: Job.Skill) -> disnake.Embed:
    embed = disnake.Embed(title=skill.name, description=skill.description, color=skill.source.color, timestamp=datetime.now(timezone.utc))
    embed.set_author(name=f"연구 보고 - {skill.source.name}", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
    embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=bot.user.display_avatar.url)
    embed.set_thumbnail(url=skill.source.icon)
    if skill.image is not None:
        embed.set_image(url=skill.image)
    types = {"active": "액티브", "passive": "패시브"}
    embed.add_field(name="스킬 유형", value=types[skill.type], inline=False)
    positions = ['왼쪽', '오른쪽']
    if skill.position is not None:
        embed.add_field(name="스킬 위치", value=f"{positions[skill.position]} 버튼")
    else:
        embed.add_field(name="스킬 위치", value="해당 없음")
    if skill.damage is not None:
        embed.add_field(name="스킬 대미지", value=skill.damage)
    else:
        embed.add_field(name="스킬 대미지", value="해당 없음")
    embed.add_field(name="스킬 범위", value=skill.range)
    embed.add_field(name="스킬 쿨타임", value=skill.cooldown)
    if len(skill.special) != 0:
        for spec in skill.special:
            specs += f"{spec}\n"
        embed.add_field(name="특수사항", value=specs, inline=False)
    return embed
    