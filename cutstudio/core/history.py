
from copy import deepcopy


class UndoHistory:
    """
    Document snapshot history for Undo and Redo.

    Each history entry is an independent copy of the document.
    """

    def __init__(self, document, max_steps=100):

        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")

        self.max_steps = max_steps

        self._states = [
            deepcopy(document)
        ]

        self._index = 0

    @property
    def can_undo(self):
        return self._index > 0

    @property
    def can_redo(self):
        return self._index < len(self._states) - 1

    @property
    def undo_count(self):
        return self._index

    @property
    def redo_count(self):
        return len(self._states) - self._index - 1

    def record(self, document):
        """
        Record a new document state.

        Discard redo history when a new edit follows an undo.
        Avoid recording identical states.
        """

        new_state = deepcopy(document)

        if new_state == self._states[self._index]:
            return False

        # Discard states that are no longer reachable.
        self._states = self._states[:self._index + 1]

        self._states.append(new_state)

        # Limit memory usage.
        if len(self._states) > self.max_steps + 1:
            self._states.pop(0)

        self._index = len(self._states) - 1

        return True

    def undo(self):
        """
        Return the previous document snapshot.
        """

        if not self.can_undo:
            return None

        self._index -= 1

        return deepcopy(self._states[self._index])

    def redo(self):
        """
        Return the next document snapshot.
        """

        if not self.can_redo:
            return None

        self._index += 1

        return deepcopy(self._states[self._index])

    def clear(self, document):
        """
        Reset history to a single initial document state.
        """

        self._states = [
            deepcopy(document)
        ]

        self._index = 0

