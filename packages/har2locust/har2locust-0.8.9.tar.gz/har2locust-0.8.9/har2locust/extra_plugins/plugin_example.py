# This file has some advanced examples of how to massage your recording
# Use it as inspiration for the techniques, not as a recommendation for exactly what to do
from har2locust.plugin import entriesprocessor, astprocessor
from ast import *
import re


@entriesprocessor
def skip_origin_header(entries):
    # this particular site doesnt care about origin header and skipping it makes the locustfile much neater
    for e in entries:
        request = e["request"]
        request["headers"] = [h for h in request["headers"] if h["name"] != "origin"]


@astprocessor
def get_customer_from_reader(tree: Module, values: dict):
    class T(NodeTransformer):
        def visit_ImportFrom(self, node: ImportFrom) -> ImportFrom:
            # our base class is RestUser, not FastHttpUser
            if node.names[0].name == "FastHttpUser":
                node.module = "svs_locust"
                node.names[0].name = "RestUser"
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node: ClassDef) -> ClassDef:
            node.bases[0].id = "RestUser"
            node.body.pop(0)  # remove host
            self.generic_visit(node)
            return node

        def visit_FunctionDef(self, node: FunctionDef) -> FunctionDef:
            # replace testlogin request with call to self.auth()
            for i in range(len(node.body)):
                try:
                    if node.body[i].items[0].context_expr.args[1].value == "/player/1/authenticate/testlogin":  # type: ignore
                        block = parse(
                            """
self.customer = next(self.customer_iterator)
self.auth()
"""
                        )
                        node.body[i] = block.body[0]
                        # yea, the next line modifies what we're iterating over so we'll miss the last element, which is ugly
                        node.body.insert(i + 1, block.body[1])
                    # if node.body[i].items[0].context_expr.args[1].value == "/wager/9/wagers":  # type: ignore
                    #     json_param = [
                    #         kw_arg.value
                    #         for kw_arg in node.body[i].items[0].context_expr.keywords  # type: ignore
                    #         if kw_arg.arg == "json"
                    #     ][0]
                    #     bets = [
                    #         json_param.values[k]
                    #         for k in range(len(json_param.keys))
                    #         if json_param.keys[k].value == "bets"
                    #     ][0]
                    #     node.body[i] = parse("self.wagerwrapper(game, append_draw_num=True)").body[0]
                except:
                    pass

            # Old school
            #             # wrap the entire task function body in a with-block.
            #             if node.name == "t":
            #                 with_block = parse(
            #                     f"""
            # with self.reader.user() as self.customer:
            #     pass
            #                     """
            #                 ).body[0]
            #                 assert isinstance(with_block, With), with_block
            #                 with_block.body = node.body
            #                 node.body = [with_block]
            self.generic_visit(node)
            return node

        def visit_Call(self, node: Call) -> Call:
            # call rest_ instead of rest for those urls that have &_<timestamp> at the end
            if isinstance(node.func, Attribute) and node.func.attr == "rest":
                c = node.args[1]
                if isinstance(c, Constant):
                    if re.search(r"[&?]_=\d+$", c.value):
                        node.func.attr = "rest_"
                        c.value = re.sub(r"[&?]_=\d+$", "", c.value)
            self.generic_visit(node)
            return node

    T().visit(tree)


# More examples

# @entriesprocessor
# def log_something_and_drop_everthing_but_the_first_request(entries):
#     logging.info(f"hello")
#     entries[:] = [entries[0]]  # update list in-place

# @entriesprocessor
# def parametrize_ssn(entries):
#     for e in entries:
#         if "postData" in e["request"]:
#             e["request"]["postData"]["text"] = re.sub(
#                 r'"personalId":"\d*"',
#                 "\"personalId\":self.customer['ssn']",
#                 e["request"]["postData"]["text"],
#             )
