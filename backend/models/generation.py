from typing import Any, Literal
from pydantic import BaseModel, Field

class GenerationRequest(BaseModel):
    project_id: str | None = None
    prompt: str = Field(min_length=8)
    refinement_notes: str | None = None

class RequirementAnalysis(BaseModel):
    business_type: str
    audience: list[str]
    branding_style: list[str]
    required_pages: list[str]
    color_tone: list[str]
    layout_style: list[str]
    ux_priorities: list[str]
    product_intent: str

class UXSection(BaseModel):
    id: str
    name: str
    purpose: str
    components: list[str]

class UXPage(BaseModel):
    path: str
    title: str
    goal: str
    sections: list[UXSection]

class UXPlan(BaseModel):
    sitemap: list[str]
    navigation: list[str]
    user_flow: list[str]
    pages: list[UXPage]

class DesignSystem(BaseModel):
    colors: dict[str, str]
    typography: dict[str, Any]
    spacing: dict[str, str]
    radius: dict[str, str]
    button_variants: dict[str, dict[str, str]]
    component_rules: list[str]

class ComponentSpec(BaseModel):
    name: str
    type: Literal["layout", "section", "primitive", "data-display", "feedback"]
    purpose: str
    props: dict[str, str] = Field(default_factory=dict)

class FrontendArchitecture(BaseModel):
    stack: list[str]
    routing_strategy: str
    state_management: str
    api_integration: str
    styling_approach: str
    component_structure: list[str]

class GenerationResult(BaseModel):
    requirements: RequirementAnalysis
    ux_plan: UXPlan
    design_system: DesignSystem
    architecture: FrontendArchitecture
    generated_code: dict[str, str]
    validation: dict[str, Any]