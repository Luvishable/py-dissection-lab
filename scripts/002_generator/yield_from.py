"""
Diyelim ki logs klasöründe gün gün log dosyaları var:
app-2026-02-10.log
app-2026-02-11.log
app-2026-02-12.log gibi..
Amaç:
- Dosyaları tek tek belleğe almdan
- satır satır akıtarak
- ERROR geçen satırları yakalamak
Bu tarz akış + zincirleme işlerde yield from cuk diye oturur
"""


from pathlib import Path
from typing import Iterator, Iterable


# Firdt yield the log files in the given directory
def iter_log_files(log_dir: Path, pattern: str = "*.log") -> Iterator[Path]:
    """
    Yield log file paths in a deterministic order which is sorted by name
    """
    yield from sorted(log_dir.glob(pattern))


# We are gonna use the func below in order to yield the lines without giving a fuck if it's error or not
def iter_lines(path: Path, encoding: str ="utf-8") -> Iterator[str]:
    """Yield lines from a file lazily (line by line)"""
    with open("r", encoding=encoding, errors="replace") as f:
        # f itself is an iterable over lines; yield from streams it outward.
        yield from f


# şimdi iter_log_files fonksiyonu ile verilen bir klasördeki log file'larını lazy şekilde
# for döngüsü ile üreteceğiz. ardından da o file içindeki satırları da iter_log_lines ile
# yine aynı şekilde lazyily üreteceğiz
def iter_all_log_lines(log_dir: Path) -> Iterator[str]:
    """
    Treat many log files as a single continuous line stream
    """
    for file in iter_log_files(log_dir):
        yield from iter_lines(file)

def iter_error_lines(lines: Iterable[str]) -> Iterator[str]:
    """Filter only error lines"""
    for line in lines:
        if "ERROR" in line:
            yield line


if __name__ == "__main__":
    log_dir = Path("logs")

    # Pipeline: many files -> all lines -> error lines
    error_stream = iter_error_lines(iter_all_log_lines(log_dir))

    for line in error_stream:
        print(line, end="")

# Generator = iterable + iterator + lazy stream (tek kullanımlık akış)