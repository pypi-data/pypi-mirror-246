__license__ = '''
sodom
Copyright (C) 2023  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


from contextlib import AbstractContextManager
from contextvars import ContextVar, Token
from functools import lru_cache, partial
from itertools import chain
import os
from typing import MutableSequence, Self

from sodom.consts import NORMAL_TAGS, VOID_TAGS, SPECIAL_ATTRS


CURRENT_ELEMENT = ContextVar['NormalElement | None']("CURRENT_ELEMENT", default=None)


class VoidElement[HTML_TAGS: VOID_TAGS]:
    __slots__ = (
        'tag',
        'attrs',
        'parent',
        '_children',
        '_context_token',
    )

    tag: HTML_TAGS
    attrs: dict[str, str]
    parent: 'NormalElement | None'

    @classmethod
    def partial[ELEMENT](cls: type[ELEMENT], tag: HTML_TAGS, *children: 'NormalElement | VoidElement | str', **attrs: str) -> partial[ELEMENT]:
        return partial[ELEMENT](cls, tag, *children, **attrs)

    def __init__(self, _tag: HTML_TAGS, *_, **attrs: str) -> None:
        self.tag = _tag
        self.attrs = attrs
        self.parent = None
        self()

    def __call__(self) -> None:
        new_parent = CURRENT_ELEMENT.get()
        if new_parent is not None:
            new_parent.add(self)

    @lru_cache(int(os.getenv('SODOM_TAG_CACHE', 128)))
    def _build_tag_header_content(self) -> str:
        '''Render tag header content (between `<` and `>`)'''
        built_content: list[str] = []

        for k, v in self.attrs.items():
            k = k.strip('_')
            if k:
                if (spec_attr := k.split('_', 1)[0]) in SPECIAL_ATTRS:
                    k = k.replace(f'{spec_attr}_', f'{spec_attr}-')
                built_content.append(f'{k}="{v}"')

        return ' '.join(c for c in chain((self.tag,), built_content) if c)

    ##### HASHING #####
    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash((self.tag, tuple(self.attrs.items())))

    ##### RENDERING #####
    def __str__(self) -> str:
        return self.__repr__()

    def __html__(self, *, level: int = 0, space: str = '  ') -> str:
        tag_content = self._build_tag_header_content()
        result = '{}<{}>'.format(space * level, tag_content)
        return result

    def __repr__(self) -> str:
        tag_content = self._build_tag_header_content()
        result = '<{} @{}>'.format(tag_content, id(self))
        return result


class NormalElement[T: NORMAL_TAGS](
    AbstractContextManager,
    VoidElement[T], # type: ignore
):
    _children: MutableSequence['NormalElement | VoidElement | str']
    _context_token: Token['NormalElement | None']

    def __init__(self, _tag: T, *_children: 'NormalElement | VoidElement | str', **attrs: str) -> None:
        super().__init__(
            _tag,  # type: ignore
            **attrs,
        )
        self._children = []
        self.add(*_children)

    ##### CONTEXT MANAGEMENT #####
    def __enter__(self) -> Self:
        self._context_token = CURRENT_ELEMENT.set(self)
        return self

    def __exit__(self, exc_type, exc_value, trace) -> None:
        CURRENT_ELEMENT.reset(self._context_token)

    ##### CHILDREN MANIPULATION #####
    def add(self, *children: 'NormalElement | VoidElement | str') -> None:
        for child in children:
            if isinstance(child, (NormalElement, VoidElement)):
                if child.parent is not None:
                    child.parent.remove(child)
                child.parent = self
        self._children.extend(children)

    def remove(self, *children: 'NormalElement | VoidElement | str') -> None:
        for child in children:
            if isinstance(child, (NormalElement, VoidElement)):
                child.parent = None
            self._children.remove(child)

    ##### RENDERING #####
    def __html__(self, *, level: int = 0, space: str = '  ') -> str:
        tag = self.tag
        tag_content = self._build_tag_header_content()

        tag_begin = '{}<{}>'.format(space * level, tag_content)
        body_content = '\n'.join(map(lambda c: render(c, level=level+1, space=space), self._children))
        tag_end = f'</{tag}>'

        if body_content:
            tag_end = space * level + tag_end

        result = ('\n' if body_content else '').join((
            tag_begin,
            body_content,
            tag_end,
        ))

        return result

    def __repr__(self) -> str:
        tag = self.tag
        tag_content = self._build_tag_header_content()
        body_content = len(self._children)

        result = '<{} @{}>:{}</{}>'.format(
            tag_content,
            id(self),
            body_content,
            tag,
        )

        return result


def render(
    *elements: NormalElement | VoidElement | str,
    level: int = 0,
    space: str = '  ',
) -> str:
    result = []
    for element in elements:
        if isinstance(element, str):
            result.append(space * level + element)
        else:
            result.append(
                element.__html__(
                    level=level,
                    space=space,
                )
            )
    return '\n'.join(result)


def render_root(
    *elements: NormalElement | VoidElement | str,
    level: int = 0,
    space: str = '  ',
):
    return render('<!DOCTYPE html>', *elements, level=level, space=space)
