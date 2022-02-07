from pathlib import Path
from typing import Union, List

from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page
from mkdocs.utils import meta


def filter_drafts(nav: Navigation, config, files):
    # preload meta
    for page in nav.pages:
        doc, page.meta = meta.get_data(Path(page.file.abs_src_path).read_text())

    # remove drafts
    def remove_drafts(items: List[Union[Page, Section]]):
        for item in items[:]:
            if item.is_page:
                if item.meta.get("draft"):
                    items.remove(item)
            else:
                # recursive remove drafts
                remove_drafts(item.children)

    remove_drafts(nav.items)
    remove_drafts(nav.pages)
