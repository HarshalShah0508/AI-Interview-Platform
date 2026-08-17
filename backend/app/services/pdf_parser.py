import pymupdf


def _get_background_color(page: pymupdf.Page) -> tuple[int, int, int]:
    """
    Estimates the page's background color by sampling its four
    corners — resume content essentially never starts exactly at
    the page edge, so this is a cheap, reliable stand-in for a
    full background-detection pass.
    """

    pixmap = page.get_pixmap()

    width, height = pixmap.width, pixmap.height

    margin = 5

    sample_points = [
        (margin, margin),
        (max(width - margin - 1, 0), margin),
        (margin, max(height - margin - 1, 0)),
        (max(width - margin - 1, 0), max(height - margin - 1, 0)),
    ]

    samples = [
        pixmap.pixel(x, y)[:3]
        for x, y in sample_points
        if 0 <= x < width and 0 <= y < height
    ]

    if not samples:
        return (255, 255, 255)

    return (
        sum(sample[0] for sample in samples) // len(samples),
        sum(sample[1] for sample in samples) // len(samples),
        sum(sample[2] for sample in samples) // len(samples),
    )


def _color_distance(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
) -> float:

    return sum(
        (a - b) ** 2
        for a, b in zip(first, second)
    ) ** 0.5


def _is_visible_span(
    span: dict,
    page_rect: pymupdf.Rect,
    background: tuple[int, int, int],
) -> bool:
    """
    Filters out text that a human reading the rendered PDF would
    never actually see, so it can't reach the resume/JD
    structuring prompts: near-zero-size text, text positioned
    entirely off the visible page, and text colored to match
    (or nearly match) the page background — the classic
    hidden-text prompt-injection technique.
    """

    if span.get("size", 0) < 1:
        return False

    bbox = pymupdf.Rect(span["bbox"])

    if not bbox.intersects(page_rect):
        return False

    color_int = span.get("color", 0)

    text_color = (
        (color_int >> 16) & 255,
        (color_int >> 8) & 255,
        color_int & 255,
    )

    if _color_distance(text_color, background) < 12:
        return False

    return True


def extract_text_from_pdf(file_path: str) -> str:

    extracted_text = ""

    with pymupdf.open(file_path) as document:

        for page in document:

            background = _get_background_color(page)

            page_dict = page.get_text("dict")

            page_lines = []

            for block in page_dict.get("blocks", []):

                for line in block.get("lines", []):

                    visible_text = "".join(
                        span["text"]
                        for span in line.get("spans", [])
                        if span.get("text")
                        and _is_visible_span(
                            span,
                            page.rect,
                            background,
                        )
                    )

                    if visible_text.strip():
                        page_lines.append(visible_text)

            if page_lines:
                extracted_text += "\n".join(page_lines) + "\n"

    return extracted_text
