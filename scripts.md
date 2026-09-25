# Applepy pyRevit scripts

This inventory covers every executable Python script found under `Applepy/Applepy.extension`, including pushbutton scripts and extension hooks.

| Script name | Description |
| --- | --- |
| Copy filters to other documents | Copies selected view filters from an open source document to destination views or view templates in the current model, preserving overrides. |
| View filters based on parameter | Incomplete utility intended to create parameter-based view filters from element type values. |
| Find CAD | Reports all CAD imports and links and shows their owner views when they are view-specific. |
| Find untagged | Finds untagged elements for a selected element category and tag category across selected views. |
| File rename | Bulk renames files in a selected folder by replacing matching text in file names. |
| Add Shared Parameters | Adds selected shared parameters to chosen categories as type or instance bindings. |
| Duplicate Elements | Lists electrical fixture elements reported by Revit duplicate placement warnings. |
| Space at room | Creates spaces in the host model at the locations of rooms from a selected linked model. |
| Copy linked elements (document) | Copies selected model elements from a linked document into the current host model. |
| Copy linked elements (view) | Copies selected view-based linked elements into the active host view. |
| Exporting IFC | Testing utility that inspects pyRevit output methods related to table rendering. |
| Loader | Loads selected Revit family files into the current project. |
| Read Excel | Reads data from a selected Excel workbook and prints the sheet contents. |
| TEST | Parses an exported HTML clash report and renders it as a clickable pyRevit output table. |
| Trial | Testing utility that writes a clickable HTML snippet to the pyRevit output and saves it as HTML. |
| for later | Experimental tagging tool that tags selected elements in chosen views using a selected tag category. |
| doc-opened hook | Hook that stores the current project's open time for later tracking. |
| doc-closing hook | Hook that calculates project session duration on close and exports timing data to CSV. |
