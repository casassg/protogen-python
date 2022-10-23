#!/usr/bin/env python

import protogen

enumPackage = protogen.PyImportPath("enum")


def generate(gen: protogen.Plugin):
    for f in gen.files_to_generate:
        if f.generate:
            g = gen.new_generated_file(
                f.proto.name.replace(".proto", ".py"), 
                f.py_import_path,
            )
            g.P("# Autogenerated code. DO NOT EDIT.")
            g.P(f'"""This is an module docstring."""')
            g.P()
            g.print_import()
            g.P()

            for enum in f.enums:
                g.P(f"class {enum.py_ident.py_name}(", enumPackage.ident("Enum"), "):")
                for value in enum.values:
                    g.P(f"  {value.proto.name}={value.number}")
                g.P()

            for message in f.messages:
                g.P(f"class {message.py_ident.py_name}:")
                g.P(f"  def __init__(self, host: str):")
                g.P(f"    self.host = host")
                g.P()

            for service in f.services:
                g.P(f"class {service.py_ident.py_name}Client:")
                g.P(f"  def __init__(self, host: str):")
                g.P(f"    self.host = host")
                g.P()
                for method in service.methods:
                    # fmt: off
                    g.P(f"  def {method.py_name}(req: ", method.input.py_ident, ") -> ", method.output.py_ident, ":")
                    g.P(f"    pass")
                    g.P()
                    # fmt: on


opts = protogen.Options()
opts.run(generate)
