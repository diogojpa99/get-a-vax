from dataclasses import dataclass

@dataclass
class MenuEntry:
  label: str
  i_classes: str | None
  href: str
  is_active: bool = False

@dataclass
class MenuEntryHeading:
  label: str

@dataclass
class MenuCollapsible:
  entries: list

