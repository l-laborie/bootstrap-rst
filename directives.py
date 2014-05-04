# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Bootstrap RST
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from docutils import nodes
from docutils.parsers.rst import Directive, directives, states, roles
from docutils.parsers.rst.roles import set_classes
from docutils.nodes import fully_normalize_name, whitespace_normalize_name



class button(nodes.Inline, nodes.Element): pass
class progress(nodes.Inline, nodes.Element): pass
class alert(nodes.General, nodes.Element): pass
class callout(nodes.General, nodes.Element): pass
class mute(nodes.General, nodes.Element): pass




class Alert(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'type': directives.unchanged,
                   'dismissable': directives.flag,
                   'class': directives.class_option }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = alert(text, **self.options)
        node['classes'] = ['alert']
        node['classes'] += self.options.get('class', [])
        if 'type' in self.options:
            node['classes'] += ['alert-%s' % node['type']]
        node.dismissable = False
        if 'dismissable' in self.options:
            node['classes'] += ['alert-dismissable']
            node.dismissable = True

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class Callout(Directive):
    required_arguments, optional_arguments = 0,1
    has_content = True

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = callout(self.block_text, **self.options)
        node['classes'] = ['bs-callout']
        if len(self.arguments):
            type = 'bs-callout-' + self.arguments[0]
        else:
            type = 'bs-callout-info'
        node['classes'] += [type]

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class Lead(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = nodes.container(text, **self.options)
        node['classes'] = ['lead']
        node['classes'] += self.options.get('class', [])

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class List(Directive):
    required_arguments, optional_arguments = 0,1
    has_content = True
    final_argument_whitespace = True

    # option_spec = {'class':  directives.class_option}
    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        # node = nodes.container(text, **self.options)
        node = mute(text, **self.options)
        node['classes'] += self.options.get('class', [])
        if self.arguments:
            node['list-class'] = self.arguments
        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]





class Paragraph(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = nodes.paragraph(text, **self.options)
        node['classes'] += self.options.get('class', [])

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class PageRow(Directive):
    """
    Directive to declare a container that is column-aware.
    """

    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'class':  directives.class_option }
    def run(self):
        self.assert_has_content()
        node = nodes.container(self.content)
        node['classes'] = ['row']
        if self.arguments:
            node['classes'] += [self.arguments[0]]
        node['classes'] += self.options.get('class', [])

        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class PageColumn(Directive):
    """
    Directive to declare column with width and offset.
    """

    required_arguments, optional_arguments = 0,0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'width':  directives.positive_int,
                   'offset': directives.positive_int,
                   'push':   directives.positive_int,
                   'pull':   directives.positive_int,
                   'class':  directives.class_option }
    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.container(text)
        width = self.options.get('width', 1)
        node['classes'] += ["col-md-%d" % width]

        offset = self.options.get('offset', 0)
        if offset > 0:
            node['classes'] += ["col-md-offset-%d" % offset]

        push = self.options.get('push', 0)
        if push > 0:
            node['classes'] += ["col-md-push-%d" % push]

        pull = self.options.get('pull', 0)
        if pull > 0:
            node['classes'] += ["col-md-pull-%d" % pull]

        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class Button(Directive):

    """
    Directive to declare a button with a lot of options.
    """

    required_arguments, optional_arguments = 0,0
    final_argument_whitespace = True
    has_content = True

    def check_type(argument):
        return directives.choice(argument,
               ('default', 'primary', 'success', 'info',
                'warning', 'danger', 'outline', 'link'))

    def check_size(argument):
        return directives.choice(argument,
               ('default', 'large', 'small','tiny'))

    def check_placement(argument):
        return directives.choice(argument,
               ('left', 'right', 'top','bottom'))

    option_spec = {'type'    : check_type,
                   'size'    : check_size,
                   'class'   : directives.class_option,
                   'active'  : directives.flag,
                   'block'   : directives.flag,
                   'toggle'  : directives.flag,
                   'target'  : directives.unchanged_required,
                   'disabled': directives.flag,
    }
    def run(self):
        self.assert_has_content()
        node = button()

        node['type'] = self.options.get('type', 'default')
        node['size'] = self.options.get('size', 'default')
        node['block'] = True if 'block' in self.options.keys() else False
        node['toggle'] = True if 'toggle' in self.options.keys() else False
        node['active'] = True if 'active' in self.options.keys() else False
        node['disabled'] = True if 'disabled' in self.options.keys() else False
        node['target'] = self.options.get('target', None)

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        self.add_name(node)
        return [node]



class Progress(Directive):

    """
    Directive to declare a progress bar.
    """

    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = False
    def check_type(argument):
        return directives.choice(argument,
               ('default', 'success', 'info', 'warning', 'danger', ))

    option_spec = {'type'    : check_type,
                   'class'   : directives.class_option,
                   'label'   : directives.unchanged,
                   'min'     : directives.unchanged_required,
                   'max'     : directives.unchanged_required,
                   'striped' : directives.flag,
                   'animated': directives.flag}
    def run(self):
        node = progress()
        node['type']      = self.options.get('type', 'default')
        node['value_min'] = self.options.get('min_value', 0)
        node['value_max'] = self.options.get('max_value', 100)
        node['value']     = self.options.get('max_value', 50)
        node['striped']   = True if 'striped' in self.options.keys() else False
        node['animated']  = True if 'animated' in self.options.keys() else False
        node['label']     = self.options.get('label', '')
        if self.arguments:
            node['value'] = int(self.arguments[0].rstrip(' %'))
            if 'label' not in self.options:
                node['label'] = self.arguments[0]
        return [node]


class Header(Directive):

    """Contents of document header."""

    required_arguments, optional_arguments = 0,1
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        self.assert_has_content()
        header = self.state_machine.document.get_decoration().get_header()
        header['classes'] += self.options.get('class', [])
        if self.arguments:
            header['classes'] += [self.arguments[0]]
        self.state.nested_parse(self.content, self.content_offset, header)
        return []


class Footer(Directive):

    """Contents of document footer."""

    required_arguments, optional_arguments = 0,1
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        self.assert_has_content()
        footer = self.state_machine.document.get_decoration().get_footer()
        footer['classes'] += self.options.get('class', [])
        if self.arguments:
            footer['classes'] += [self.arguments[0]]
        self.state.nested_parse(self.content, self.content_offset, footer)
        return []



directives.register_directive('progress', Progress)
directives.register_directive('list', List)
directives.register_directive('alert', Alert)
directives.register_directive('callout', Callout)
directives.register_directive('lead', Lead)
directives.register_directive('row', PageRow)
directives.register_directive('column', PageColumn)
directives.register_directive('button', Button)
directives.register_directive('footer', Footer)
directives.register_directive('header', Header)
