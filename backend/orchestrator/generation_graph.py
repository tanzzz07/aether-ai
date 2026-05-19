from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel

from backend.agents import (
    DesignSystemAgent,
    FrontendArchitectAgent,
    RequirementAnalyzerAgent,
    UIGenerationAgent,
    UXPlannerAgent,
    ValidationAgent,
)
from backend.models import GenerationResult
from backend.services.ai_provider import AIProvider

class ProgressEvent(BaseModel):
    step: str
    status: str
    message: str
    data: dict[str, Any] | None = None

class GenerationOrchestrator:
    def __init__(self, ai: AIProvider) -> None:
        self.requirements = RequirementAnalyzerAgent(ai)
        self.ux = UXPlannerAgent(ai)
        self.design = DesignSystemAgent(ai)
        self.architect = FrontendArchitectAgent(ai)
        self.ui = UIGenerationAgent(ai)
        self.validator = ValidationAgent()

    async def run(self, prompt: str) -> GenerationResult:
        requirements = await self.requirements.run(prompt)
        ux_plan = await self.ux.run(requirements)
        design_system = await self.design.run(requirements, ux_plan)
        architecture = await self.architect.run(ux_plan, design_system)
        generated_code = await self.ui.run(ux_plan, design_system, architecture)
        validation = await self.validator.run(architecture, generated_code)
        return GenerationResult(
            requirements=requirements,
            ux_plan=ux_plan,
            design_system=design_system,
            architecture=architecture,
            generated_code=generated_code,
            validation=validation,
        )

    async def stream(self, prompt: str) -> AsyncIterator[ProgressEvent]:
        yield ProgressEvent(
            step="requirements",
            status="running",
            message="Analyzing business goals, audience, and UX priorities.",
        )
        requirements = await self.requirements.run(prompt)
        yield ProgressEvent(
            step="requirements",
            status="complete",
            message="Requirements captured.",
            data=requirements.model_dump(),
        )

        yield ProgressEvent(step="ux", status="running", message="Planning sitemap and section flow.")
        ux_plan = await self.ux.run(requirements)
        yield ProgressEvent(step="ux", status="complete", message="UX architecture planned.", data=ux_plan.model_dump())

        yield ProgressEvent(
            step="design_system", status="running", message="Generating design tokens and component rules."
        )
        design_system = await self.design.run(requirements, ux_plan)
        yield ProgressEvent(
            step="design_system",
            status="complete",
            message="Design system generated.",
            data=design_system.model_dump(),
        )

        yield ProgressEvent(
            step="frontend_architecture", status="running", message="Designing reusable frontend structure."
        )
        architecture = await self.architect.run(ux_plan, design_system)
        yield ProgressEvent(
            step="frontend_architecture",
            status="complete",
            message="Frontend architecture ready.",
            data=architecture.model_dump(),
        )

        yield ProgressEvent(step="ui_generation", status="running", message="Generating typed React component files.")
        generated_code = await self.ui.run(ux_plan, design_system, architecture)
        yield ProgressEvent(
            step="ui_generation",
            status="complete",
            message="Reusable UI files generated.",
            data=generated_code.model_dump(),
        )

        yield ProgressEvent(
            step="validation", status="running", message="Validating architecture, TypeScript shape, and consistency."
        )
        validation = await self.validator.run(architecture, generated_code)
        yield ProgressEvent(
            step="validation",
            status="complete",
            message="Validation complete.",
            data=validation.model_dump(),
        )

        result = GenerationResult(
            requirements=requirements,
            ux_plan=ux_plan,
            design_system=design_system,
            architecture=architecture,
            generated_code=generated_code,
            validation=validation,
        )
        yield ProgressEvent(
            step="result", status="complete", message="Generation pipeline finished.", data=result.model_dump()
        )