# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, manage elements and adds entries to menu.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import pygame
import pygameMenu.controls as _controls

from pygameMenu.utils import check_key_pressed_valid
from pygameMenu.widgets.core.widget import Widget


class Selector(Widget):
    """
    Selector widget.

    :param label: Selector label text
    :type label: basestring
    :param elements: Elements of the selector
    :type elements: list
    :param selector_id: ID of the selector
    :type selector_id: basestring
    :param default: Index of default element to display
    :type default: int
    :param onchange: Callback when changing the selector
    :type onchange: callable, NoneType
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, NoneType
    :param kwargs: Optional keyword-arguments for callbacks
    """

    def __init__(self,
                 label,
                 elements,
                 selector_id='',
                 default=0,
                 onchange=None,
                 onreturn=None,
                 **kwargs
                 ):
        assert isinstance(label, str)
        assert isinstance(elements, list)
        assert isinstance(selector_id, str)
        assert isinstance(default, int)

        # Check element list
        for vl in elements:
            assert len(vl) > 1, \
                'Length of each element on item list must be greater than 1'
            assert isinstance(vl[0], str), \
                'First element of each item on list must be a string (the title of each item)'
        assert default < len(elements), 'default position should be lower than number of values'
        assert isinstance(selector_id, str), 'ID must be a string'
        assert isinstance(default, int), 'default must be an integer'

        super(Selector, self).__init__(widget_id=selector_id,
                                       onchange=onchange,
                                       onreturn=onreturn,
                                       kwargs=kwargs)

        self._elements = elements
        self._index = 0  # type: int
        self._label = label
        self._labelsize = 0.0  # type: float
        self._sformat = '{0}< {1} >'  # type: str

        # Apply default item
        default %= len(self._elements)
        for k in range(0, default):
            self.right()

    def _apply_font(self):
        self._labelsize = self._font.size(self._label)[0]

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def get_value(self):
        """
        Return the current value of the selector at the selected index.

        :return: Value and index as a tuple, (value,index)
        :rtype: tuple
        """
        return self._elements[self._index][0], self._index

    def left(self):
        """
        Move selector to left.

        :return: None
        """
        self._index = (self._index - 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def right(self):
        """
        Move selector to right.

        :return: None
        """
        self._index = (self._index + 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def _render(self):
        string = self._sformat.format(self._label, self.get_value()[0])
        if not self._render_hash_changed(string, self.selected):
            return
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._render_string(string, color)
        self._rect.width, self._rect.height = self._surface.get_size()
        self._check_render_size_changed()

    def set_value(self, item):
        """
        Set the current value of the widget, selecting the element that matches
        the text if item is a string, or the index of the position of item is an integer.

        For example, if selector is *[['a',0],['b',1],['a',2]]*:
            - *widget*.set_value('a') -> Widget selects 0 (first match)
            - *widget*.set_value(2) -> Widget selects 2.

        :param item: Item to select, can be a string or an integer.
        :type item: basestring, int
        :return: None
        """
        assert isinstance(item, (str, int)), 'item must be an string or an integer'
        if isinstance(item, str):
            for element in self._elements:
                if element[0] == item:
                    self._index = self._elements.index(element)
                    return
            raise ValueError("No value '{}' found in selector".format(item))
        elif isinstance(item, int):
            assert 0 <= item < len(self._elements), \
                'item index must be greater than zero and lower than the number of elements on the selector'
            self._index = item

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        for event in events:  # type: pygame.event.EventType

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Events
            keydown = event.type == pygame.KEYDOWN
            joy_hatmotion = self.joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self.joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self.joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            if keydown and event.key == _controls.KEY_LEFT or \
                    joy_hatmotion and event.value == _controls.JOY_LEFT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value < _controls.JOY_DEADZONE:
                self.sound.play_key_add()
                self.left()
                updated = True

            elif keydown and event.key == _controls.KEY_RIGHT or \
                    joy_hatmotion and event.value == _controls.JOY_RIGHT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value > -_controls.JOY_DEADZONE:
                self.sound.play_key_add()
                self.right()
                updated = True

            elif keydown and event.key == _controls.KEY_APPLY or \
                    joy_button_down and event.button == _controls.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply(*self._elements[self._index][1:])
                updated = True

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = self._rect.topleft
                    topright, _ = self._rect.topright
                    dist = mousex - (topleft + self._labelsize)  # Distance from label
                    if dist > 0:  # User clicked the options, not label

                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._labelsize)
                        if pos <= 0.5:
                            self.left()
                        else:
                            self.right()
                        updated = True

        return updated

    def update_elements(self, elements):
        """
        Update selector elements.

        :param elements: Elements of the selector
        :type elements: Object
        :return: None
        """
        for elem in elements:  # Check value list
            assert len(elem) >= 1, 'length of each element in value list must be greater than 1'
            assert isinstance(elem[0], str), 'first element of value list component must be a string'
        selected_element = self._elements[self._index]
        self._elements = elements
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= len(self._elements):
                self._index = len(self._elements) - 1
