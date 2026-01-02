import asyncio
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.agent import Agent

app = typer.Typer(help="A simple multi-turn claude code conversation.")
console = Console()

@app.command(name="guide")
def info():
    """Usage guide"""
    
    infoText = """
Claude Agent SDK를 사용한 구현이기에, Claude Code 설치가 필요합니다.
세션은 프로그램을 종료하지 않는 한 지속됩니다.

shifty_prompt.txt - 시스템 프롬프트를 수정해서 채팅 맥락을 변경할 수 있습니다.
shifty_schema.json - Claude Code의 최종 출력 형식을 강제합니다.

Agent는 WebSearch, WebFetch를 사용할 수 있고, Approve가 필요하도록 설정해 두었습니다.
    """
    infoPanel = Panel.fit(infoText, title="Info", border_style="green")

    commandText = """
[bold]cmd:event[/bold] - 랜덤 이벤트 생성
[bold]exit[/bold] or [bold]quit[/bold] - 채팅 종료
    """
    commandPanel = Panel.fit(commandText, title="Chat Commands", border_style="magenta")

    console.print(infoPanel)
    console.print(commandPanel)

@app.command(name="chat")
def simple_multi_turn(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode")
):
    """Start a chat with shifty"""

    asyncio.run(Agent().simple_multi_turn(debug=debug))