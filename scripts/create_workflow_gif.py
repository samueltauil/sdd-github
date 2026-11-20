from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1400, 930
CARD_WIDTH, CARD_HEIGHT = 390, 135
COLS = (80, 505, 930)
ROWS = (175, 370, 565)
POSITIONS = (
    (COLS[0], ROWS[0]),
    (COLS[1], ROWS[0]),
    (COLS[2], ROWS[0]),
    (COLS[2], ROWS[1]),
    (COLS[1], ROWS[1]),
    (COLS[0], ROWS[1]),
    (COLS[0], ROWS[2]),
    (COLS[1], ROWS[2]),
    (COLS[2], ROWS[2]),
)
STEPS = (
    ("Issue", "Describe the problem",
     "A person describes the problem and the outcome they need."),
    ("OpenSpec", "Define the proposed change",
     "Compare the current system contract with the proposed change."),
    ("Gherkin", "Write examples people can read",
     "Describe observable behavior as Given, When, and Then examples."),
    ("Human approval", "Agree before coding",
     "People review the requirements and examples before implementation."),
    ("Copilot", "Plan, then implement",
     "Copilot maps the approved behavior to code and tests."),
    ("Pull request", "Share the change",
     "The pull request connects the issue, specifications, code, and evidence."),
    ("Automated checks", "Run the evidence",
     "OpenSpec validation, acceptance scenarios, and technical tests run."),
    ("Human review", "Review and approve",
     "Reviewers check the behavior, implementation, and remaining risks."),
    ("Merge + archive", "Update the living specification",
     "Merge, update the contract, and archive the change; the linked issue can close."),
)
BACKGROUND = "#0b1422"
MUTED = "#91a4b7"
WHITE = "#f4f8fc"
ACCENT = "#61e3db"
DONE = "#64c4a0"
TRACK = "#455a6d"


def font(size, bold=False):
    candidates = (
        ("C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"),
        ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


FONTS = {
    "heading": font(43, True),
    "intro": font(23),
    "small": font(18, True),
    "number": font(22, True),
    "card_title": font(30, True),
    "card_text": font(21),
    "detail_title": font(25, True),
    "detail": font(22),
}


def connector(index):
    x1, y1 = POSITIONS[index]
    x2, y2 = POSITIONS[index + 1]
    if y1 == y2 and x2 > x1:
        return (x1 + CARD_WIDTH + 3, y1 + CARD_HEIGHT // 2), (x2 - 3, y2 + CARD_HEIGHT // 2)
    if y1 == y2:
        return (x1 - 3, y1 + CARD_HEIGHT // 2), (x2 + CARD_WIDTH + 3, y2 + CARD_HEIGHT // 2)
    return (x1 + CARD_WIDTH // 2, y1 + CARD_HEIGHT + 3), (x2 + CARD_WIDTH // 2, y2 - 3)


def arrow(draw, start, end, color):
    draw.line((start, end), fill=color, width=4)
    x, y = end
    if end[0] > start[0]:
        points = ((x, y), (x - 9, y - 6), (x - 9, y + 6))
    elif end[0] < start[0]:
        points = ((x, y), (x + 9, y - 6), (x + 9, y + 6))
    else:
        points = ((x, y), (x - 6, y - 9), (x + 6, y - 9))
    draw.polygon(points, fill=color)


def wrap(draw, text, selected_font, max_width):
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=selected_font) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def render(active, progress):
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((80, 54, 91, 65), radius=5, fill=ACCENT)
    draw.text((108, 40), "FROM IDEA TO A TRUSTED CHANGE", font=FONTS["heading"], fill=WHITE)
    draw.text(
        (82, 102),
        "A connected workflow, with people in control at every step.",
        font=FONTS["intro"],
        fill=MUTED,
    )

    for index in range(len(STEPS) - 1):
        start, end = connector(index)
        arrow(draw, start, end, DONE if index < active else TRACK)
        if index == active and progress:
            dot = (
                round(start[0] + (end[0] - start[0]) * progress),
                round(start[1] + (end[1] - start[1]) * progress),
            )
            draw.line((start, dot), fill=ACCENT, width=4)
            draw.ellipse((dot[0] - 6, dot[1] - 6, dot[0] + 6, dot[1] + 6), fill=ACCENT)

    for index, ((x, y), (title, subtitle, _)) in enumerate(zip(POSITIONS, STEPS)):
        if index == active:
            fill, border, badge = "#173b4b", ACCENT, "#26706f"
        elif index < active:
            fill, border, badge = "#152e36", "#477e72", "#28594f"
        else:
            fill, border, badge = "#172535", "#31475b", "#293f52"
        draw.rounded_rectangle(
            (x, y, x + CARD_WIDTH, y + CARD_HEIGHT),
            radius=17,
            fill=fill,
            outline=border,
            width=3 if index == active else 2,
        )
        draw.ellipse((x + 23, y + 23, x + 69, y + 69), fill=badge)
        number = str(index + 1)
        box = draw.textbbox((0, 0), number, font=FONTS["number"])
        draw.text(
            (x + 46 - (box[2] - box[0]) / 2, y + 30),
            number,
            font=FONTS["number"],
            fill=WHITE,
        )
        draw.text((x + 85, y + 20), title, font=FONTS["card_title"], fill=WHITE)
        draw.text((x + 24, y + 91), subtitle, font=FONTS["card_text"], fill="#c6d5e0")

    draw.rounded_rectangle((80, 758, 1320, 879), radius=17, fill="#192b3c", outline="#31485c", width=2)
    draw.text(
        (105, 776),
        f"{active + 1:02d} / {len(STEPS):02d}   {STEPS[active][0]}",
        font=FONTS["detail_title"],
        fill=ACCENT,
    )
    for line, text in enumerate(wrap(draw, STEPS[active][2], FONTS["detail"], 1160)):
        draw.text((105, 815 + line * 27), text, font=FONTS["detail"], fill=WHITE)

    for index in range(len(STEPS)):
        x = 80 + index * 138
        draw.rounded_rectangle(
            (x, 900, x + 118, 907),
            radius=3,
            fill=ACCENT if index == active else DONE if index < active else TRACK,
        )
    return image.convert("P", palette=Image.Palette.ADAPTIVE, colors=128)


def main():
    frames = []
    durations = []
    for active in range(len(STEPS)):
        for progress in ((0, 0.33, 0.66, 1) if active < len(STEPS) - 1 else (0,)):
            frames.append(render(active, progress))
            durations.append(2200 if active == len(STEPS) - 1 else 1700 if progress == 0 else 120)

    output = Path(__file__).resolve().parent.parent / "docs" / "assets" / "sdd-workflow.gif"
    output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Created {output} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
