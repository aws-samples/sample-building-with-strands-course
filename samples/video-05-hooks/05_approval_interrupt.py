import os
from strands import Agent, tool
from strands.hooks import BeforeToolCallEvent, HookProvider, HookRegistry


@tool
def list_files(directory: str) -> str:
    """List files in a directory.

    Args:
        directory: Path to the directory to list
    """
    try:
        entries = os.listdir(directory)
        if not entries:
            return f"{directory} is empty"
        return "\n".join(entries)
    except FileNotFoundError:
        return f"Directory not found: {directory}"


@tool
def read_file(path: str) -> str:
    """Read the contents of a file.

    Args:
        path: Path to the file to read
    """
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except IsADirectoryError:
        return f"{path} is a directory, not a file"


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file. Creates the file if it doesn't exist.

    Args:
        path: Path to the file to write
        content: Content to write to the file
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {path}"


@tool
def delete_file(path: str) -> str:
    """Delete a file from the filesystem.

    Args:
        path: Path to the file to delete
    """
    try:
        os.remove(path)
        return f"Deleted {path}"
    except FileNotFoundError:
        return f"File not found: {path}"


class DeleteApprovalHook(HookProvider):
    """Only intercepts delete operations — all other file tools run freely."""

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolCallEvent, self.check_delete)

    def check_delete(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] != "delete_file":
            return

        approval = event.interrupt(
            "delete-approval",
            reason={"path": event.tool_use["input"]["path"]}
        )

        if approval.lower() != "y":
            event.cancel_tool = "User denied file deletion"


agent = Agent(
    tools=[list_files, read_file, write_file, delete_file],
    hooks=[DeleteApprovalHook()],
)

print("File Manager Agent (type 'quit' to exit)")
print("-" * 45)

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break
    if not user_input:
        continue

    print()
    result = agent(user_input)

    while result.stop_reason == "interrupt":
        for interrupt in result.interrupts:
            approval = input(f"\n⚠️  Delete '{interrupt.reason['path']}'? (y/N): ")
            result = agent([
                {
                    "interruptResponse": {
                        "interruptId": interrupt.id,
                        "response": approval,
                    }
                }
            ])
