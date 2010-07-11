#!/usr/bin/env python
# coding=utf8

import sys
import os.path
import jinja2
import re

header_tpl_s = """\
#ifndef {{header_name}}
#define {{header_name}}

/* Header automatically generated by {{program_name}} */

#include <{{base_include}}>

#define {{uppercase_prefix}}_TYPE_{{uppercase_typename}} ({{lowercase_prefix}}_{{lowercase_typename}}_get_type())
#define {{uppercase_prefix}}_{{uppercase_typename}}(obj) (G_TYPE_CHECK_INSTANCE_CAST((obj), {{uppercase_prefix}}_TYPE_{{uppercase_typename}}, {{typename}}))
#define {{uppercase_prefix}}_IS_{{uppercase_typename}}(obj) (G_TYPE_CHECK_INSTANCE_TYPE((obj), {{uppercase_prefix}}_TYPE_{{uppercase_typename}}))
#define {{uppercase_prefix}}_{{uppercase_typename}}_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST((klass), {{uppercase_prefix}}_TYPE_{{uppercase_typename}}, {{typename}}Class))
#define {{uppercase_prefix}}_IS_{{uppercase_typename}}_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), {{uppercase_prefix}}_TYPE_{{uppercase_typename}}))
#define {{uppercase_prefix}}_{{uppercase_typename}}_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS((obj), {{uppercase_prefix}}_TYPE_{{uppercase_typename}}, {{typename}}Class))

typedef struct _{{prefix}}{{typename}} {{prefix}}{{typename}};
typedef struct _{{prefix}}{{typename}}Class {{prefix}}{{typename}}Class;

struct _{{prefix}}{{typename}} {
	{{base_prefix}}{{base_typename}} parent;

	/* <private> */
};

struct _{{prefix}}{{typename}}Class {
	{{base_prefix}}{{base_typename}}Class parent_class;

	/* <private> */
};

GType {{lowercase_prefix}}_{{lowercase_typename}}_get_type(void);
{{prefix}}{{typename}} *{{lowercase_prefix}}_{{lowercase_typename}}_new();

#endif /* {{header_name}} */
"""

implementation_tpls_s = """\
#include "{{header_filename}}"

/* Implementation automatically generated by {{program_name}} */

G_DEFINE_TYPE ({{prefix}}{{typename}}, {{lowercase_prefix}}_{{lowercase_typename}}, {{uppercase_base_prefix}}_TYPE_{{uppercase_base_typename}})

static void {{lowercase_prefix}}_{{lowercase_typename}}_class_init({{prefix}}{{typename}}Class *klass) {
	/* set up virtual method handler here, if needed */
}

static void {{lowercase_prefix}}_{{lowercase_typename}}_init({{prefix}}{{typename}} *self) {
	/* "constructor" */
}

{{prefix}}{{typename}} *{{lowercase_prefix}}_{{lowercase_typename}}_new() {
	return g_object_new({{uppercase_prefix}}_TYPE_{{uppercase_typename}}, NULL);
}
"""

if '__main__' == __name__:
	program_name = os.path.basename(sys.argv[0])
	if len(sys.argv) < 3:
		print "usage: %s Prefix TypeName [BasePrefix BaseTypeName] [BaseInclude]" % program_name
		print "example (defines a new widget derived from GtkWidget): %s MyApp SuperWidget Gtk Widget" % program_name
		sys.exit(1)

	base_typename = "Object"
	base_prefix = "G"
	if len(sys.argv) >= 5:
		base_typename = sys.argv[4]
		base_prefix = sys.argv[3]

	base_include = 'glib-object.h'
	if 'Gtk' == base_prefix: base_include = 'gtk/gtk.h'
	if len(sys.argv) >= 6:
		base_include = sys.argv[5]

	print "Inheriting from",base_prefix + base_typename,"out of",base_include

	header_tpl = jinja2.Template(header_tpl_s)
	implementation_tpl = jinja2.Template(implementation_tpls_s)

	typename = sys.argv[2]
	prefix = sys.argv[1]
	uppercase_typename = re.sub(r'(\w)([A-Z])',r'\1_\2',typename).upper()
	uppercase_prefix = prefix.upper()

	uppercase_base_typename = re.sub(r'(\w)([A-Z])',r'\1_\2',base_typename).upper()
	uppercase_base_prefix = base_prefix.upper()

	filename_stem = (prefix + typename).lower()
	header_filename = filename_stem + '.h'
	implementation_filename = filename_stem + '.c'

	if os.path.exists(header_filename):
		print "file exists:",header_filename
		sys.exit(2)
	if os.path.exists(implementation_filename):
		print "file exists:",implementation_filename
		sys.exit(3)

	data = {
		'header_name': uppercase_typename + '_H',
		'typename': typename,
		'prefix': prefix,
		'uppercase_typename': uppercase_typename,
		'uppercase_prefix': uppercase_prefix,
		'lowercase_typename': uppercase_typename.lower(),
		'lowercase_prefix': uppercase_prefix.lower(),

		'base_typename': base_typename,
		'base_prefix': base_prefix,
		'uppercase_base_typename': uppercase_base_typename,
		'uppercase_base_prefix': uppercase_base_prefix,
		'lowercase_base_typename': uppercase_base_typename.lower(),
		'lowercase_base_prefix': uppercase_base_prefix.lower(),

		'header_filename': header_filename,
		'base_include': base_include,
	}

	file(header_filename, 'w').write(header_tpl.render(**data))
	print "wrote",header_filename
	file(implementation_filename, 'w').write(implementation_tpl.render(**data))
	print "wrote",implementation_filename
