def checkFlowState(story) -> int:
    complete = ["Complete", "Accepted"]
    mostlyComplete = ["Pending Environment", "Ready for Test", "In Test"]
    if story["FlowState"]["_refObjectName"] == complete:
        return 1
    if story["FlowState"]["_refObjectName"] == mostlyComplete:
        return 2
    return 3
