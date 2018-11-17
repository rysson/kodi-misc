# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function

from .base import TestCase
from unittest import skip as skiptest, skipIf as skiptestIf

from ..mselect import dom_select
from ..base import aWord, aWordStarts, aStarts, aEnds, aContains
from ..base import Node, DomMatch   # for test only


class N(Node):
    __slots__ = Node.__slots__ + ('content', )
    def __init__(self, content, attrs=None, tag=None, **kwargs):
        if tag is None:
            tag = content[:1].lower()
        super(N, self).__init__('<{}>'.format(tag))
        self._Node__name = tag
        self.content = content
        self._Node__attrs = attrs or kwargs or {}
    def __eq__(self, other):
        #for a in 'name', 'attrs', 'content':
        #    print('====?', getattr(self, a), getattr(other, a))
        return self.name == other.name and self.attrs == other.attrs and self.content == other.content

class NC(N):
    def __init__(self, content, cls=None, tag=None, **kwargs):
        super(NC, self).__init__(content, tag=tag, **kwargs)
        if cls is not None:
            self._Node__attrs['class'] = cls


class TestDomSelect(TestCase):

    def test_tag(self):
        self.assertEqual(dom_select('<a>A</a>', 'a'), [N('A')])
        self.assertEqual(dom_select('<a>A</a>', 'b'), [])
        self.assertEqual(dom_select('<a>A1</a><a>A2</a>', 'a'), [N('A1'), N('A2')])

    def test_id_empty(self):
        self.assertEqual(dom_select('<a id="0">A</a>', '#1'), [])
        self.assertEqual(dom_select('<a id="1">A</a>', '#1'), [N('A', id='1')])
        self.assertEqual(dom_select('<a id="1">A</a><b id="2">B</b>', '#1'), [N('A', id='1')])

    def test_id_tag(self):
        self.assertEqual(dom_select('<a id="0">A</a>', 'a#1'), [])
        self.assertEqual(dom_select('<a id="1">A</a>', 'a#1'), [N('A', id='1')])
        self.assertEqual(dom_select('<a>A</a>', 'b#1'), [])
        self.assertEqual(dom_select('<a id="1">A</a>', 'b#1'), [])
        self.assertEqual(dom_select('<a id="1">A1</a><a>A2</a>', 'a#1'), [N('A1', id='1')])
        self.assertEqual(dom_select('<a id="1">A1</a><a id="2">A2</a>', 'a#1'), [N('A1', id='1')])

    def test_class_1_empty(self):
        self.assertEqual(dom_select('<a class="0">A</a>', '.1'), [])
        self.assertEqual(dom_select('<a class="1">A</a>', '.1'), [NC('A', '1')])
        self.assertEqual(dom_select('<a class="1">A1</a><a class="2">A2</a>', '.1'), [NC('A1', '1')])
        self.assertEqual(dom_select('<a class="1">A1</a><a class="1">A2</a>', '.1'), [NC('A1', '1'), NC('A2', '1')])
        self.assertEqual(dom_select('<a class="1">A</a><b class="1">B</b>', '.1'), [NC('A', '1'), NC('B', '1')])

    def test_class_1_tag(self):
        self.assertEqual(dom_select('<a class="0">A</a>', 'a.1'), [])
        self.assertEqual(dom_select('<a class="1">A</a>', 'a.1'), [NC('A', '1')])
        self.assertEqual(dom_select('<a class="1">A1</a><a class="2">A2</a>', 'a.1'), [NC('A1', '1')])
        self.assertEqual(dom_select('<a class="1">A1</a><a class="1">A2</a>', 'a.1'), [NC('A1', '1'), NC('A2', '1')])
        self.assertEqual(dom_select('<a class="1">A</a><b class="1">B</b>', 'a.1'), [NC('A', '1')])

    def test_class_n_empty(self):
        self.assertEqual(dom_select('<a class="0 9">A</a>', '.1'), [])
        self.assertEqual(dom_select('<a class="1 2">A</a>', '.1'), [NC('A', '1 2')])
        self.assertEqual(dom_select('<a class="2 1">A</a>', '.1'), [NC('A', '2 1')])
        self.assertEqual(dom_select('<a class="0 1 2">A</a>', '.1'), [NC('A', '0 1 2')])
        self.assertEqual(dom_select('<a class="11 2 3">A</a>', '.1'), [])

    def test_class_n_tag(self):
        self.assertEqual(dom_select('<a class="0 9">A</a>', 'a.1'), [])
        self.assertEqual(dom_select('<a class="1 2">A</a>', 'a.1'), [NC('A', '1 2')])
        self.assertEqual(dom_select('<a class="1">A1</a><a class="11 2">A2</a>', 'a.1'), [NC('A1', '1')])
        self.assertEqual(dom_select('<a class="1 2">A1</a><a class="1 3">A2</a>', 'a.1'), [NC('A1', '1 2'), NC('A2', '1 3')])
        self.assertEqual(dom_select('<a class="1 2 3">A</a><b class="1">B</b>', 'a.1'), [NC('A', '1 2 3')])

    def test_id_class_empty(self):
        self.assertEqual(dom_select('<a id="0">A</a>', '#1.2'), [])
        self.assertEqual(dom_select('<a id="1">A</a>', '#1.2'), [])
        self.assertEqual(dom_select('<a class="0">A</a>', '#1.2'), [])
        self.assertEqual(dom_select('<a class="2">A</a>', '#1.2'), [])
        self.assertEqual(dom_select('<a id="1" class="2">A</a>', '#1.2'), [NC('A', '2', id='1')])
        self.assertEqual(dom_select('<a class="2" id="1">A</a>', '#1.2'), [NC('A', '2', id='1')])
        self.assertEqual(dom_select('<a id="1" class="2 3">A</a>', '#1.2'), [NC('A', '2 3', id='1')])

    def test_id_class_tag(self):
        self.assertEqual(dom_select('<a id="0">A</a>', 'a#1.2'), [])
        self.assertEqual(dom_select('<a id="1">A</a>', 'a#1.2'), [])
        self.assertEqual(dom_select('<a class="0">A</a>', 'a#1.2'), [])
        self.assertEqual(dom_select('<a class="2">A</a>', 'a#1.2'), [])
        self.assertEqual(dom_select('<a id="1" class="2">A</a>', 'a#1.2'), [NC('A', '2', id='1')])
        self.assertEqual(dom_select('<a class="2" id="1">A</a>', 'a#1.2'), [NC('A', '2', id='1')])
        self.assertEqual(dom_select('<a id="1" class="2 3">A</a>', 'a#1.2'), [NC('A', '2 3', id='1')])
        self.assertEqual(dom_select('<b id="1" class="2">B</b>', 'a#1.2'), [])
        self.assertEqual(dom_select('<b class="2" id="1">B</b>', 'a#1.2'), [])
        self.assertEqual(dom_select('<b id="1" class="2 3">B</b>', 'a#1.2'), [])

    def test_descend(self):
        self.assertEqual(dom_select('<a>A</a>', 'a b'), [])
        self.assertEqual(dom_select('<b>B</b>', 'a b'), [])
        self.assertEqual(dom_select('<a>A</a><b>B</b>', 'a b'), [])
        self.assertEqual(dom_select('<a>A<b>B</b></a>', 'a b'), [N('B')])
        self.assertEqual(dom_select('<b>B</b><a>A</a>', 'a b'), [])
        self.assertEqual(dom_select('<b>B<a>A</a></b>', 'a b'), [])
        self.assertEqual(dom_select('<a><b><c>C</c></b></a>', 'a b'), [N('<c>C</c>', tag='b')])
        self.assertEqual(dom_select('<a><b><c>C</c></b></a>', 'a b c'), [N('C')])

    def test_node_attrs(self):
        self.assertEqual(dom_select('<a>A</a>', 'a')[0].attrs, {})
        self.assertEqual(dom_select('<a x="1">A</a>', 'a')[0].attrs, {'x': '1'})
        self.assertEqual(dom_select('<a x="1" y="2">A</a>', 'a')[0].attrs, {'x': '1', 'y': '2'})
        self.assertEqual(dom_select('<a x-y="1">A</a>', 'a')[0].attrs, {'x-y': '1'})
        self.assertEqual(dom_select('<a x="1" x-y="2">A</a>', 'a')[0].attrs, {'x': '1', 'x-y': '2'})
        self.assertEqual(dom_select('<a x="1" y="2" x-y="3">A</a>', 'a')[0].attrs, {'x': '1', 'y': '2', 'x-y': '3'})

    def test_node_attr(self):
        self.assertRaises(AttributeError, getattr, dom_select('<a>A</a>', 'a')[0].attr, 'x')
        self.assertRaises(AttributeError, dom_select('<a>A</a>', 'a')[0].attr, 'x')
        self.assertEqual(dom_select('<a x="1">A</a>', 'a')[0].attr.x, '1')
        self.assertEqual(dom_select('<a x="1" y="2">A</a>', 'a')[0].attr.x, '1')
        self.assertEqual(dom_select('<a x="1" y="2">A</a>', 'a')[0].attr.y, '2')
        self.assertEqual(dom_select('<a x="1" y="2">A</a>', 'a')[0].attr('x'), '1')
        self.assertEqual(dom_select('<a x="1" y="2">A</a>', 'a')[0].attr('y'), '2')
        self.assertEqual(dom_select('<a x-y="1">A</a>', 'a')[0].attr('x-y'), '1')

    def test_node_data(self):
        self.assertRaises(AttributeError, getattr, dom_select('<a>A</a>', 'a')[0].data, 'x')
        self.assertRaises(AttributeError, dom_select('<a>A</a>', 'a')[0].data, 'x')
        self.assertRaises(AttributeError, getattr, dom_select('<a x="1">A</a>', 'a')[0].data, 'x')
        self.assertRaises(AttributeError, dom_select('<a x="1">A</a>', 'a')[0].data, 'x')
        self.assertEqual(dom_select('<a data-x="1">A</a>', 'a')[0].data.x, '1')
        self.assertEqual(dom_select('<a data-x="1" data-y="2">A</a>', 'a')[0].data.x, '1')
        self.assertEqual(dom_select('<a data-x="1" data-y="2">A</a>', 'a')[0].data.y, '2')
        self.assertEqual(dom_select('<a data-x="1" data-y="2">A</a>', 'a')[0].data('x'), '1')
        self.assertEqual(dom_select('<a data-x="1" data-y="2">A</a>', 'a')[0].data('y'), '2')
        self.assertEqual(dom_select('<a data-x-y="1">A</a>', 'a')[0].data('x-y'), '1')
        self.assertEqual(dom_select('<a data-x="1" x="2">A</a>', 'a')[0].data.x, '1')
        self.assertEqual(dom_select('<a data-x="1" x="2">A</a>', 'a')[0].data('x'), '1')
        self.assertEqual(dom_select('<a data-x-y="1" x-y="2">A</a>', 'a')[0].data('x-y'), '1')

    def test_case_sensitive_tag(self):
        with self.subTest('Case sensitive: search a in a'):
            self.assertEqual(dom_select('<a>A</a>', 'a'), [N('A')])
        with self.subTest('Case sensitive: search A in a'):
            self.assertEqual(dom_select('<a>A</a>', 'A'), [N('A')])
        with self.subTest('Case sensitive: search a in A'):
            self.assertEqual(dom_select('<A>A</A>', 'a'), [N('A', tag='A')])
        with self.subTest('Case sensitive: search A in A'):
            self.assertEqual(dom_select('<A>A</A>', 'A'), [N('A', tag='A')])

    def test_case_sensitive_attr(self):
        with self.subTest('Case sensitive: search x in x'):
            self.assertEqual(dom_select('<a x="1">A</a>', '[x]'), [N('A', x='1')])
        with self.subTest('Case sensitive: search X in x'):
            self.assertEqual(dom_select('<a x="1">A</a>', '[X]'), [N('A', x='1')])
        with self.subTest('Case sensitive: search x in X'):
            self.assertEqual(dom_select('<a X="1">A</a>', '[x]'), [N('A', x='1')])
        with self.subTest('Case sensitive: search X in X'):
            self.assertEqual(dom_select('<a X="1">A</a>', '[X]'), [N('A', x='1')])



class TestDomSelectSet(TestCase):

    def test_simple(self):
        self.assertEqual(dom_select('<a>A</a><b>B</b>', '{a,b}'), [(N('A'), N('B'))])

    def test_tag_alt(self):
        self.assertEqual(dom_select('<a>A1<b>B</b>A2<c>C</c>A3</a>', 'a {b,c}'), [(N('B'), N('C'))])

    def test_alt_tag(self):
        self.assertEqual(dom_select('<a>A1<c>C1</c>A2</a>X<b>B1<c>C2</c>B2</b>', '{a,b} c'), [[N('C1')], [N('C2')]])

    def test_alt_tag2(self):
        self.assertEqual(dom_select('<a>A1<c>C1</c>A2</a>X<b>B1<c>C2</c>B2<c>C3</c>B3</b>', '{a,b} c'),
                         [[N('C1')], [N('C2'), N('C3')]])

    def test_alt_tag_desc(self):
        self.assertEqual(dom_select('<a>A1<c>C1</c>A2</a>X<b>B1<c>C2</c>B2</b>', '{a c,b c}'), [(N('C1'), N('C2'))])

    def test_alt_tag2_desc(self):
        self.assertEqual(dom_select('<a>A1<c>C1</c>A2</a>X<b>B1<c>C2</c>B2<c>C3</c>B3</b>', '{a c,b c}'),
                         [(N('C1'), N('C2'))])

    def test_multi(self):
        self.assertEqual(dom_select('<a>A1</a><a>A2</a>', '{a,a}'), [(N('A1'), N('A2'))])

    def test_multi_old_first(self):
        self.assertEqual(dom_select('<a>A1</a><a>A2</a>', '{{a,a}}'), [(N('A1'), N('A1')), (N('A2'), N('A2'))])

    def test_nth(self):
        self.assertEqual(dom_select('<a>A1</a><a>A2</a>', '{a:1,a}'), [(N('A1'), N('A2'))])
        self.assertEqual(dom_select('<a>A1</a><a>A2</a>', '{a:2,a:1}'), [(N('A2'), N('A1'))])

    def test_nth2(self):
        self.assertEqual(dom_select('<a>A1</a><a>A2</a><b>B1</b><b>B2</b>', '{a:1,a,b}'), [(N('A1'), N('A2'), N('B1'))])
        self.assertEqual(dom_select('<a>A1</a><a>A2</a><b>B1</b><b>B2</b>', '{a:1,a,b:2}'), [(N('A1'), N('A2'), N('B2'))])



# Manual tests
if __name__ == '__main__':
    #print(dom_select('<a>A<c>C0</c></a><a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c><b>B9</b>', '{a,b}'))
    #print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c>', '{a,b}'))
    print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c></b><c>Cx</c>', '{a,b} c, a'))
    #print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c>', '{a,b} c, a'))
    #print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c>', '{a c,b c}, a'))
    #print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c>', '* c::node, a'))
    #print(dom_select('<a>A<c>C1</c></a><b>B<c>C2</c><c>C3</c></b><c>Cx</c>', '* c, a'))
    #print(dom_select('<a>A<c>C1</c><d>D1</d></a><b>B<c>C2</c><d>D1</d></b>', '{a,b} {c,d}, a'))

    #print(dom_select('<a><b>B1</b><c>C1</c></a><a><b>B2</b></a>', 'a {b,c}'))
    #print(dom_select('<a><b>B1<d>D1b</d></b><c>C1<d>D1c</d></c></a><a><b>B2<d>D2b</d></b></a>', 'a {b,c} d'))
