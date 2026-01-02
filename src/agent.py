from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock, ToolUseBlock, ToolResultBlock, PermissionResultAllow, PermissionResultDeny
from rich.panel import Panel
from rich.console import Console
from rich.json import JSON
from pathlib import Path
import json

class Agent:
    def __init__(self):
        self.console = Console()

    async def run(self):
        print("Agent is running")

    async def simple_multi_turn(self, debug: bool = False):
        """A simple claude code conversation."""

        asset_dir = Path(__file__).parent.parent / "assets"
        with open(asset_dir / "shifty_schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)
        with open(asset_dir / "shifty_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            output_format={
                "type": "json_schema",
                "schema": schema
            },
            can_use_tool=self.prompt_for_tool_approval,
            allowed_tools=["WebSearch", "WebFetch"],
            permission_mode="default"
        )
        async with ClaudeSDKClient(options=options) as client:
            while True:
                user_input = self.console.input("[bold green]User:[/bold green] ")
                if user_input.lower() in {"exit", "quit"}:
                    self.console.print("[bold red]Exiting...[/bold red]")
                    break

                await client.query(user_input)

                output = ""
                state = None
                async for msg in client.receive_response():
                    if isinstance(msg, ResultMessage):
                        json_string = json.dumps(msg.structured_output)
                        state = JSON(json_string, highlight=True)
                    elif isinstance(msg, AssistantMessage):
                        for chunk in msg.content:
                            if isinstance(chunk, TextBlock):
                                output += f"{chunk.text}\n"
                            elif isinstance(chunk, ToolUseBlock):
                                if (not debug):
                                    self.console.print(f"[Tool Use: {chunk.name}]", style="grey53")
                            elif isinstance(chunk, ToolResultBlock):
                                self.console.print(f"[Tool Result: {chunk.tool_use_id} - {chunk.content}]", style="grey53")

                    if (debug):
                        panel = Panel.fit(str(msg), title="Debug Message", border_style="red")
                        self.console.print(panel)

                outputPanel = Panel.fit(output, title="Shifty", border_style="cyan")
                self.console.print(outputPanel)
                if state:
                    statePanel = Panel.fit(state, title="State", border_style="magenta")
                    self.console.print(statePanel)

    async def prompt_for_tool_approval(self, tool_name: str, input_params: dict, context: dict):
        self.console.print(f"🔧 Tool Request: {tool_name}")
        self.console.print(f"   Parameters: {input_params}")

        answer = input("\nApprove tool use? (y/n): ")

        if answer.lower() in ['y', 'yes']:
            return PermissionResultAllow(updated_input=input_params)
        else:
            return PermissionResultDeny(message="User denied permission for this tool")
