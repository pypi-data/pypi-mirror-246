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


import asyncio
from multiprocessing.pool import ThreadPool
from functools import partial
from time import sleep
from timeit import timeit
from typing import Literal
from uuid import uuid4
import pytest

from sodom.classes import NormalElement, VoidElement, render, render_root
from sodom import *


def _build_attrs(**attrs):
    return ' '.join(f'{k}="{v}"'for k, v in attrs.items())


def _rand_attrs():
    return {
        str(uuid4()): str(uuid4())
    }


def test_draw_VoidElement_with_tag():
    elem = hr()
    assert '<hr>' == render(elem)


def test_draw_VoidElement_with_attrs():
    elem = hr(test1='test1', test2='test2', test3='test3')
    assert '<hr test1="test1" test2="test2" test3="test3">' == render(elem)


def test_draw_NormalElement_with_tag():
    elem = div()
    assert '<div></div>' == render(elem)


def test_draw_NormalElement_with_attrs():
    elem = div(test1='test1', test2='test2', test3='test3')
    assert '<div test1="test1" test2="test2" test3="test3"></div>' == render(elem)


def test_draw_NormalElement_with_children_via_args():
    attr0 = _rand_attrs()

    attr01 = _rand_attrs()
    attr02 = _rand_attrs()
    attr03 = _rand_attrs()

    attr031 = _rand_attrs()
    attr032 = _rand_attrs()
    attr033 = _rand_attrs()

    elem = div(
        '_',
        div(**attr01),
        div(**attr02),
        div(
            div(**attr031),
            div(**attr032),
            div(**attr033),
            **attr03,
        ),
        **attr0,
    )
    assert (
        f'<div {_build_attrs(**attr0)}>\n'
        '  _\n'
        f'  <div {_build_attrs(**attr01)}></div>\n'
        f'  <div {_build_attrs(**attr02)}></div>\n'
        f'  <div {_build_attrs(**attr03)}>\n'
        f'    <div {_build_attrs(**attr031)}></div>\n'
        f'    <div {_build_attrs(**attr032)}></div>\n'
        f'    <div {_build_attrs(**attr033)}></div>\n'
        '  </div>\n'
        '</div>'
    ) == render(elem)


def test_draw_NormalElement_with_children_via_context():
    attr0 = _rand_attrs()

    attr01 = _rand_attrs()
    attr02 = _rand_attrs()
    attr03 = _rand_attrs()

    attr031 = _rand_attrs()
    attr032 = _rand_attrs()
    attr033 = _rand_attrs()

    with div('_', **attr0) as elem:
        div(**attr01)
        div(**attr02)
        with div(**attr03):
            div(**attr031)
            div(**attr032)
            div(**attr033)

    assert (
        f'<div {_build_attrs(**attr0)}>\n'
        '  _\n'
        f'  <div {_build_attrs(**attr01)}></div>\n'
        f'  <div {_build_attrs(**attr02)}></div>\n'
        f'  <div {_build_attrs(**attr03)}>\n'
        f'    <div {_build_attrs(**attr031)}></div>\n'
        f'    <div {_build_attrs(**attr032)}></div>\n'
        f'    <div {_build_attrs(**attr033)}></div>\n'
        '  </div>\n'
        '</div>'
    ) == render(elem)


def test_VoidElement_build():
    attrs = {
        f'test{i}': f'test{i}'
        for i in range(3)
    }

    partial_test_hr: partial[VoidElement[Literal['hr']]] = VoidElement.partial('hr')

    test_hr = partial_test_hr(**attrs)

    assert 'hr' == test_hr.tag
    for k in attrs:
        assert test_hr.attrs[k] == attrs[k]


def test_NormalElement_with_children():
    child = NormalElement('div',
        NormalElement('div',
            NormalElement('div'),
        ),
        NormalElement('div'),
        NormalElement('div',
            VoidElement('hr'),
            '',
        ),
    )
    assert (
        '<div>\n'
        '  <div>\n'
        '    <div></div>\n'
        '  </div>\n'
        '  <div></div>\n'
        '  <div>\n'
        '    <hr>\n'
        '    \n'
        '  </div>\n'
        '</div>'
    ) == render(child)


def test_div_with_context():
    with div() as d:
        hr()

    assert (
        '<div>\n'
        '  <hr>\n'
        '</div>'
    ) == render(d)


def test_build_special_attrs():
    attrs = {
        f'data_test{i}': f'test{i}'
        for i in range(3)
    }

    d = div(**attrs)

    assert (
        '<div data-test0="test0" data-test1="test1" data-test2="test2"></div>'
    ) == render(d)


def test_void_element_str():
    h = hr()
    assert (
        '<hr @{}>'.format(id(h))
    ) == str(h)


def test_normal_element_str():
    d = div()
    assert (
        '<div @{}>:0</div>'.format(id(d))
    ) == str(d)

    d = div(div(), attr='attr')
    assert (
        '<div attr="attr" @{}>:1</div>'.format(id(d))
    ) == str(d)


def test_adding_children():
    d = div()
    h = hr()
    d.add(h)
    assert h in d._children
    assert h.parent == d


def test_parent_changing():
    h = hr()

    with div() as d1:
        h()
    assert h.parent == d1
    assert h in d1._children

    with div() as d2:
        h()
    assert h.parent == d2
    assert h in d2._children


def test_removing_children():
    h = hr()
    d = div(h)
    d.remove(h)
    assert h not in d._children
    assert h.parent is None

def test_document():
    d = div()
    assert (
        '<!DOCTYPE html>\n'
        + render(d)
    ) == render_root(d)

def test_text_utils():
    text_data = str(uuid4())
    with div() as d:
        text(text_data)
    assert text_data in d._children


@pytest.mark.asyncio
async def test_building_html_in_two_tasks():
    async def task1():
        with div() as d:
            text('task1')
            await asyncio.sleep(2)
            text('task1')
        return d

    async def task2():
        with div() as d:
            text('task2')
            await asyncio.sleep(5)
            text('task2')
        return d

    div1, div2 = await asyncio.gather(
        task1(),
        task2(),
    )

    assert div1._children[0] == 'task1'
    assert div1._children[1] == 'task1'
    assert div2._children[0] == 'task2'
    assert div2._children[1] == 'task2'


def test_building_html_in_two_threads():
    def task1():
        with div() as d:
            text('task1')
            sleep(2)
            text('task1')
        return d

    def task2():
        with div() as d:
            text('task2')
            sleep(5)
            text('task2')
        return d

    pool = ThreadPool(2)

    t1 = pool.apply_async(task1)
    t2 = pool.apply_async(task2)

    div1 = t1.get()
    div2 = t2.get()

    assert div1._children[0] == 'task1'
    assert div1._children[1] == 'task1'
    assert div2._children[0] == 'task2'
    assert div2._children[1] == 'task2'


def _dominate_case():
    with dominate_tags.body() as root:
        with dominate_tags.div(cls='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'):
            with dominate_tags.h5(cls='my-0 mr-md-auto font-weight-normal'):
                dominate_text('Company name')
            with dominate_tags.nav(cls='my-2 my-md-0 mr-md-3'):
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Features')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Enterprise')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Support')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Pricing')
    return root.render('')


def _sodom_case():
    with body() as root:
        with div(class_='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'):
            with h5(class_='my-0 mr-md-auto font-weight-normal'):
                text('Company name')
            with nav(class_='my-2 my-md-0 mr-md-3'):
                with a(class_='p-2 text-dark', href='#'):
                    text('Features')
                with a(class_='p-2 text-dark', href='#'):
                    text('Enterprise')
                with a(class_='p-2 text-dark', href='#'):
                    text('Support')
                with a(class_='p-2 text-dark', href='#'):
                    text('Pricing')
    return render(root, space='')


def _fast_html_case():
    root = fast_html.body(
        fast_html.div(
            class_='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow',
            i=(
                fast_html.h5(
                    'Company name'
                ),
                fast_html.nav(
                    class_='my-2 my-md-0 mr-md-3',
                    i=(
                        fast_html.a('Features', class_='p-2 text-dark', href='#'),
                        fast_html.a('Enterprise', class_='p-2 text-dark', href='#'),
                        fast_html.a('Support', class_='p-2 text-dark', href='#'),
                        fast_html.a('Pricing', class_='p-2 text-dark', href='#'),
                    )
                ),
            ),
        )
    )
    return fast_html.render(root)


try:
    from dominate import tags as dominate_tags
    from dominate.util import text as dominate_text
except ImportError:
    pass
else:
    def test_performance_dominate():
        # d = dominate_case()
        # s = sodom_case()

        dominate_case_time = timeit(_dominate_case, number=1_000)
        sodom_case_time = timeit(_sodom_case, number=1_000)

        result = round((dominate_case_time / sodom_case_time) * 100)
        assert result >= 100


try:
    import fast_html
except ImportError:
    pass
else:
    def test_performance_fast_html():
        # f = fast_html_case()
        # s = sodom_case()

        fast_html_case_time = timeit(_fast_html_case, number=1_000)
        sodom_case_time = timeit(_sodom_case, number=1_000)

        result = round((fast_html_case_time / sodom_case_time) * 100)
        assert result >= 100

try:
    from aiohttp import web
    from sodom.ext import aiohttp as aiohttp_
except ImportError as e:
    print(e)
else:
    def test_aiohttp():
        attr0 = _rand_attrs()

        attr01 = _rand_attrs()
        attr02 = _rand_attrs()
        attr03 = _rand_attrs()

        attr031 = _rand_attrs()
        attr032 = _rand_attrs()
        attr033 = _rand_attrs()

        with div('_', **attr0) as root:
            div(**attr01)
            div(**attr02)
            with div(**attr03):
                div(**attr031)
                div(**attr032)
                div(**attr033)
        response = aiohttp_.sodom_response(root)

        assert isinstance(response, web.Response)
        assert (
            '<!DOCTYPE html>\n'
            f'<div {_build_attrs(**attr0)}>\n'
            '  _\n'
            f'  <div {_build_attrs(**attr01)}></div>\n'
            f'  <div {_build_attrs(**attr02)}></div>\n'
            f'  <div {_build_attrs(**attr03)}>\n'
            f'    <div {_build_attrs(**attr031)}></div>\n'
            f'    <div {_build_attrs(**attr032)}></div>\n'
            f'    <div {_build_attrs(**attr033)}></div>\n'
            '  </div>\n'
            '</div>'
        ) == response.text

try:
    from flask import Response
    from sodom.ext import flask as flask_
except ImportError as e:
    print(e)
else:
    def test_flask():

        attr0 = _rand_attrs()

        attr01 = _rand_attrs()
        attr02 = _rand_attrs()
        attr03 = _rand_attrs()

        attr031 = _rand_attrs()
        attr032 = _rand_attrs()
        attr033 = _rand_attrs()

        with div('_', **attr0) as root:
            div(**attr01)
            div(**attr02)
            with div(**attr03):
                div(**attr031)
                div(**attr032)
                div(**attr033)
        response = flask_.sodom_response(root)

        assert isinstance(response, Response)
        assert (
            '<!DOCTYPE html>\n'
            f'<div {_build_attrs(**attr0)}>\n'
            '  _\n'
            f'  <div {_build_attrs(**attr01)}></div>\n'
            f'  <div {_build_attrs(**attr02)}></div>\n'
            f'  <div {_build_attrs(**attr03)}>\n'
            f'    <div {_build_attrs(**attr031)}></div>\n'
            f'    <div {_build_attrs(**attr032)}></div>\n'
            f'    <div {_build_attrs(**attr033)}></div>\n'
            '  </div>\n'
            '</div>'
        ) == ''.join((r.decode() for r in response.response if isinstance(r, (bytes, bytearray))))

try:
    import quart
    from sodom.ext import quart as quart_
except ImportError as e:
    print(e)
else:
    @pytest.mark.asyncio
    async def test_quart():

        attr0 = _rand_attrs()

        attr01 = _rand_attrs()
        attr02 = _rand_attrs()
        attr03 = _rand_attrs()

        attr031 = _rand_attrs()
        attr032 = _rand_attrs()
        attr033 = _rand_attrs()

        with div('_', **attr0) as root:
            div(**attr01)
            div(**attr02)
            with div(**attr03):
                div(**attr031)
                div(**attr032)
                div(**attr033)
        response = quart_.sodom_response(root)

        assert isinstance(response, quart.Response)
        assert (
            '<!DOCTYPE html>\n'
            f'<div {_build_attrs(**attr0)}>\n'
            '  _\n'
            f'  <div {_build_attrs(**attr01)}></div>\n'
            f'  <div {_build_attrs(**attr02)}></div>\n'
            f'  <div {_build_attrs(**attr03)}>\n'
            f'    <div {_build_attrs(**attr031)}></div>\n'
            f'    <div {_build_attrs(**attr032)}></div>\n'
            f'    <div {_build_attrs(**attr033)}></div>\n'
            '  </div>\n'
            '</div>'
        ) == await response.get_data(as_text=True)


try:
    from sanic.response.types import HTTPResponse
    from sodom.ext import sanic as sanic_
except ImportError as e:
    print(e)
else:
    def test_sanic():
        attr0 = _rand_attrs()

        attr01 = _rand_attrs()
        attr02 = _rand_attrs()
        attr03 = _rand_attrs()

        attr031 = _rand_attrs()
        attr032 = _rand_attrs()
        attr033 = _rand_attrs()

        with div('_', **attr0) as root:
            div(**attr01)
            div(**attr02)
            with div(**attr03):
                div(**attr031)
                div(**attr032)
                div(**attr033)
        response = sanic_.sodom_response(root)

        assert isinstance(response, HTTPResponse)
        assert (
            '<!DOCTYPE html>\n'
            f'<div {_build_attrs(**attr0)}>\n'
            '  _\n'
            f'  <div {_build_attrs(**attr01)}></div>\n'
            f'  <div {_build_attrs(**attr02)}></div>\n'
            f'  <div {_build_attrs(**attr03)}>\n'
            f'    <div {_build_attrs(**attr031)}></div>\n'
            f'    <div {_build_attrs(**attr032)}></div>\n'
            f'    <div {_build_attrs(**attr033)}></div>\n'
            '  </div>\n'
            '</div>'
        ).encode() == response.body
