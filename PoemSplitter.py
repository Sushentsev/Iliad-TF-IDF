from typing import List

class PoemSplitter:
    """
    Класс, который разбивает текст на стихотворные строки.
    """
    def __init__(self):
        self._introduction = True
        self._documents = []
        self._document = []
        self._poem_lines = 0
        self._cont_empty_lines = 0

    def _is_poem_beginning(self, line: str) -> bool:
        # Пропуск вступления.
        if line.strip() == "Гомер. Илиада. Песнь первая. Язва, гнев.":
            self._introduction = False

        # Стихи в тексте начинаются с пробела и должны быть достаточной длины.
        return len(line.strip()) > 5 and line[0].isspace() and not self._introduction

    def _is_poem_continuation(self, line: str) -> bool:
        line_strip = line.strip()

        # Единственная некорретная строка песни, которая не начинается с пробела.
        if line_strip.startswith('врагам и других'):
            return True

        # Песни в поэме заканчиваются на "Гомер. Илиада. Песнь ...".
        if line_strip.startswith('Гомер. Илиада. Песнь'):
            return False

        # Окончания стиха по отсуствию в начале строки пробела или цифры,
        # которые используются для нумерации строк песни.
        # В поэме иногда цифру 3 заменяют на букву "З".
        if len(line_strip) > 0 and (not (line[0].isspace() or line[0].isdigit() or line[0] == 'З')):
            return False

        # В стихах одной песни может присутствовать одна подряд идущая пустая строка
        if len(line_strip) == 0 and self._cont_empty_lines == 0:
            return True

        if self._cont_empty_lines >= 2:
            return False

        return not len(line_strip) == 0

    def _process_poem_beginning(self, line: str):
        self._document.append(line.strip())
        self._poem_lines += 1

    def _process_poem_continuation(self, line: str):
        line = line.strip()
        if len(line) == 0:
            self._cont_empty_lines += 1
            return

        self._cont_empty_lines = 0
        self._document.append(line)
        self._poem_lines += 1

    def _process_poem_stopping(self):
        if len(self._document) > 1:
            self._documents.append(self._document)
        self._document = []
        self._poem_lines = 0
        self._cont_empty_lines = 0

    def split_text(self, text: str) -> List[List[str]]:
        text = text.splitlines()

        for line in text:
            if self._poem_lines == 0:
                if self._is_poem_beginning(line):
                    self._process_poem_beginning(line)
            else:
                if self._is_poem_continuation(line):
                    self._process_poem_continuation(line)
                else:
                    self._process_poem_stopping()

        self._process_poem_stopping()
        return self._documents
