from pydantic import BaseModel, Field


class Reflection(BaseModel):
    """反思：看清当下真实的处境与心思。"""
    situation: str = Field(description="用户当前面对的具体情境")
    obstacle: str = Field(description="真正的阻碍，是心里没看见的那件事")
    insight: str = Field(description="由此得到的一句关键洞察")


class Aspiration(BaseModel):
    """立志：确立一个具体、可检验的方向。"""
    goal: str = Field(description="想达成的具体目标")
    why: str = Field(description="为什么这件事值得做")
    standard: str = Field(description="怎样算做到了")


class Action(BaseModel):
    """行动：拆到五分钟能开始的一步。"""
    first_step: str = Field(description="五分钟内可以开始的第一步")
    duration_minutes: int = Field(description="建议投入的分钟数", ge=1, le=120)
    obstacle_plan: str = Field(description="遇到阻力时的应对")


class Review(BaseModel):
    """复盘：知行合一，从结果回到心。"""
    done: str = Field(description="实际完成了什么")
    gap: str = Field(description="与目标的差距")
    next_action: str = Field(description="下一步调整")


class Plan(BaseModel):
    """完整的一次行动陪伴结构：反思—立志—行动—复盘。"""
    reflection: Reflection
    aspiration: Aspiration
    action: Action
    review: Review | None = None
