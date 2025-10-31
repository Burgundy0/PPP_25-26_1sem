import asyncio
import string

async def caesar_cipher(text: str, shift: int) -> str:
    await asyncio.sleep(0)
    result = []
    for ch in text:
        if ch.isalpha():
            alphabet = string.ascii_lowercase if ch.islower() else string.ascii_uppercase
            result.append(alphabet[(alphabet.index(ch) + shift) % 26])
        else:
            result.append(ch)
    return ''.join(result)

async def reverse_text(text: str) -> str:
    await asyncio.sleep(0)
    return text[::-1]

async def process_commands(text: str, commands: list[str]) -> list[str]:
    steps = [text]
    for cmd in commands:
        cmd = cmd.strip().lower()
        if cmd.startswith('c'):
            try:
                shift = int(cmd[1:])
                text = await caesar_cipher(text, shift)
            except ValueError:
                continue
        elif cmd == 'r':
            text = await reverse_text(text)
        else:
            continue
        steps.append(text)
    return steps

def show_steps(steps: list[str]):
    for i, s in enumerate(steps):
        print(f"Шаг {i}: {s}")
    print(f"\nРезультат: {steps[-1]}")

async def main():
    text = input("Введите строку: ").strip()
    commands = input("Введите команды (например: c1 r c-1 r): ").strip().split()
    steps = await process_commands(text, commands)
    show_steps(steps)

if __name__ == "__main__":
    asyncio.run(main())
