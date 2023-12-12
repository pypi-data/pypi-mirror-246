from grimp import ImportGraph
from importlinter import Contract, ContractCheck, fields, output
from importlinter.application import contract_utils
from importlinter.application.contract_utils import AlertLevel


class ImportPolicy(Contract):
    type_name = None

    allow_modules = fields.SetField(subfield=fields.ImportExpressionField(), required=False)

    def check(self, graph: ImportGraph, verbose: bool) -> ContractCheck:
        is_kept = True
        invalid_importers = []

        contract_utils.remove_ignored_imports(
            graph=graph,
            ignore_imports=self.allow_modules,  # type: ignore
            unmatched_alerting=AlertLevel.ERROR,
        )

        for mod in graph.modules:
            was_imported = graph.find_downstream_modules(mod)
            if not was_imported:
                continue

            is_kept = False
            invalid_importers.extend([dict(downstream_module=imp, upstream_module=mod) for imp in was_imported])

        return ContractCheck(kept=is_kept, metadata=dict(invalid_importers=invalid_importers))

    def render_broken_contract(self, check: ContractCheck) -> None:
        metadata = check.metadata["invalid_importers"]
        for chains_data in metadata:
            downstream = chains_data["downstream_module"]
            upstream = chains_data["upstream_module"]
            output.print_error(f"{downstream} is not allowed to import {upstream}")
            output.new_line()
