
from cutstudio.core.document import Document
from cutstudio.core.history import UndoHistory
from cutstudio.core.objects import ObjectType, VectorObject


def test_initial_history_has_no_undo_or_redo():

    history = UndoHistory(Document())

    assert not history.can_undo
    assert not history.can_redo


def test_record_and_undo():

    document = Document()
    history = UndoHistory(document)

    obj = VectorObject(
        object_type=ObjectType.RECTANGLE
    )

    document.active_layer.add_object(obj)

    assert history.record(document)

    assert history.can_undo

    restored = history.undo()

    assert len(restored.active_layer.objects) == 0


def test_redo():

    document = Document()
    history = UndoHistory(document)

    obj = VectorObject(
        object_type=ObjectType.RECTANGLE
    )

    document.active_layer.add_object(obj)

    history.record(document)

    history.undo()

    restored = history.redo()

    assert len(restored.active_layer.objects) == 1


def test_new_edit_discards_redo_history():

    document = Document()
    history = UndoHistory(document)

    first = VectorObject(
        object_type=ObjectType.RECTANGLE
    )

    document.active_layer.add_object(first)
    history.record(document)

    history.undo()

    second = VectorObject(
        object_type=ObjectType.ELLIPSE
    )

    document.active_layer.add_object(second)
    history.record(document)

    assert not history.can_redo


def test_history_limit():

    document = Document()
    history = UndoHistory(document, max_steps=2)

    for index in range(3):

        obj = VectorObject(
            object_type=ObjectType.RECTANGLE,
            x=index + 1
        )

        document.active_layer.add_object(obj)
        history.record(document)

    assert history.undo_count == 2


def test_clear_history():

    document = Document()
    history = UndoHistory(document)

    document.active_layer.add_object(
        VectorObject(
            object_type=ObjectType.RECTANGLE
        )
    )

    history.record(document)
    history.clear(document)

    assert not history.can_undo
    assert not history.can_redo

