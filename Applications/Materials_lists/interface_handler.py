# app.py  (standalone)
# Rule: nothing executes on import except definitions

from __future__ import annotations

import json
import traceback
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ==============================================================================
# APP META
# ==============================================================================
APP_NAME = "Material Handler"
APP_VERSION = "vNext"
APP_PURPOSE = "Upload or paste material info, process it using your logic, then save results to the Vault."

# ==============================================================================
# LOGIC IMPORT (same folder)
# ==============================================================================
def _import_logic():
    """
    Keep imports inside a function to avoid any side effects at import-time.
    Rename `material_logic` below to match your logic file name (without .py).
    """
    import logic as L  # <-- CHANGE THIS if your logic file is named differently
    st .write("Imported Logic From", L.__file__)

    # Expect these to exist in your logic file:
    # get_material_data, load_library, save_to_library, calculate_total, delete_item
    required = ["get_material_data", "load_library", "save_to_library", "calculate_total", "delete_item"]
    missing = [n for n in required if not hasattr(L, n)]
    if missing:
        raise AttributeError(f"Logic file is missing: {', '.join(missing)}")

    return L


# ==============================================================================
# STATE
# ==============================================================================
def _ensure_state() -> None:
    st.session_state.setdefault("page", "Home")

    # Workbench state
    st.session_state.setdefault("wb_text", "")
    st.session_state.setdefault("wb_file", None)  # streamlit UploadedFile or camera object
    st.session_state.setdefault("wb_result", None)
    st.session_state.setdefault("wb_error", None)

    # Draft fields (editable after processing)
    st.session_state.setdefault("wb_item_name", "")
    st.session_state.setdefault("wb_item_price", 0.0)
    st.session_state.setdefault("wb_qty", 1)
    st.session_state.setdefault("wb_item_number", "")
    # Vault state
    st.session_state.setdefault("vault_selected_key", None)

    # Help state
    st.session_state.setdefault("last_ticket", None)

    # Settings
    st.session_state.setdefault("dev_mode", False)


def _stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==============================================================================
# SIDEBAR NAV (always present)
# ==============================================================================
def _sidebar() -> None:
    with st.sidebar:
        st.title(APP_NAME)
        st.caption(APP_VERSION)
        st.divider()

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
        if st.button("🛠️ Workbench", use_container_width=True):
            st.session_state.page = "Workbench"
        if st.button("🗄️ Vault", use_container_width=True):
            st.session_state.page = "Vault"
        if st.button("❓ Help / Support", use_container_width=True):
            st.session_state.page = "Help"

        st.divider()
        st.session_state.dev_mode = st.toggle("Developer mode", value=st.session_state.dev_mode)


# ==============================================================================
# PAGES
# ==============================================================================
def _page_home() -> None:
    st.header("🏠 Home")
    st.write(f"**Purpose:** {APP_PURPOSE}")
    st.write(f"**Version:** {APP_VERSION}")

    st.divider()

    c1, c2 = st.columns([0.65, 0.35], gap="large")
    with c1:
        if st.button("▶️ Start", type="primary", use_container_width=True):
            st.session_state.page = "Workbench"

    with c2:
        st.info("🚧 Coming soon: ")
        if st.button("Need help / support?", use_container_width=True):
            st.session_state.page = "Help"


def _workbench_payload() -> Dict[str, Any]:
    f = st.session_state.wb_file
    text = (st.session_state.wb_text or "").strip()

    file_bytes = None
    filename = None
    if f is not None:
        filename = getattr(f, "name", None)
        try:
            file_bytes = f.getvalue()
        except Exception:
            # some camera inputs behave differently; UI still holds the object
            file_bytes = None

    return {
        "text": text if text else None,
        "file_obj": f,
        "file_bytes": file_bytes,
        "filename": filename,
    }


def _process_workbench(L) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Uses your existing OCR/tag logic via get_material_data(file_obj) if a file exists.
    If no file, falls back to text only (you can upgrade this later).
    """
    payload = _workbench_payload()
    f = payload["file_obj"]
    text = payload["text"]

    if f is None and not text:
        return None, "Nothing to process. Upload/scan an image or paste text first."

    try:
        # Preferred: OCR from file using your existing get_material_data
        if f is not None:
            data = L.get_material_data(f)
            # Expected pattern from earlier: ["Description: X", "Price: Y"]
            name = ""
            price = 0.0
            item_number = ""
            if isinstance(data, list) and len(data) >= 1 and ": " in data[0]:
                name = data[0].split(": ", 1)[1].strip()

            if isinstance(data, list) and len(data) >= 2 and ": " in data[1]:
                raw = data[1].split(": ", 1)[1].strip()
                try:
                    price = float(raw)
                except Exception:
                    price = 0.0
            if isinstance(data, list) and len(data) >= 3 and "# " in data[2]:
                item_number = data[2].split("# ", 1)[1].strip()
            st.session_state.wb_item_name = name
            st.session_state.wb_item_price = price
            st.session_state.wb_item_number = item_number
            
            return {"source": "ocr_image", "description": name, "price": price, "item_number": item_number, "raw": data}, None

        # Fallback: text-only (no OCR)
        # Keep it simple: store text as name/description
        st.session_state.wb_item_name = text[:140] if text else ""
        st.session_state.wb_item_price = 0.0
        return {"source": "pasted_text", "description": st.session_state.wb_item_name, "price": 0.0}, None

    except Exception as e:
        return None, f"Process failed: {e}"


def _page_workbench(L) -> None:
    st.header("🛠️ Workbench")
    st.caption("Input → Process → (edit draft) → Save to Vault")

    st.divider()

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.subheader("Input Box")

        cam = st.camera_input("Scan Material Tag (optional)", key="wb_cam_input")
        up = st.file_uploader("Or upload a photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False, key="wb_uploader_input")
        if cam is not None:
            st.session_state.wb_file = cam
        elif up is not None:
            st.session_state.wb_file = up

        st.session_state.wb_text = st.text_area(
            "Or paste source material",
            value=st.session_state.wb_text,
            height=180,
            placeholder="Paste receipt lines, label text, notes…",
        )

        b1, b2, b3 = st.columns(3)
        with b1:
            do_process = st.button("⚙️ Process", type="primary", use_container_width=True)
        with b2:
            do_scrap = st.button("🧹 Scrap", use_container_width=True)
        with b3:
            do_save = st.button("💾 Save", use_container_width=True, disabled=(st.session_state.wb_result is None))

        if do_scrap:
            st.session_state.wb_text = ""
            st.session_state.wb_file = None
            st.session_state.wb_result = None
            st.session_state.wb_error = None
            st.session_state.wb_item_name = ""
            st.session_state.wb_item_price = 0.0
            st.session_state.wb_qty = 1
            st.toast("Workbench cleared.", icon="🧹")

        if do_process:
            res, err = _process_workbench(L)
            st.session_state.wb_result = res
            st.session_state.wb_error = err

        st.divider()
        st.subheader("Draft (editable before Save)")

        st.session_state.wb_item_name = st.text_input("Item / Material Name", value=st.session_state.wb_item_name)
        st.session_state.wb_item_number = st.text_input("Item Number", value=st.session_state.wb_item_number)
        cA, cB = st.columns(2)
        
        with cA:
            st.session_state.wb_item_price = st.number_input(
                "Price",
                min_value=0.0,
                value=float(st.session_state.wb_item_price),
                format="%.2f",
            )
        with cB:
            st.session_state.wb_qty = st.number_input(
                "Quantity",
                min_value=1,
                step=1,
                value=int(st.session_state.wb_qty),
            )

        if do_save:
            name = (st.session_state.wb_item_name or "").strip()
            if not name:
                st.warning("Enter a material name first.")
            else:
                try:
                    library = L.load_library()
                    total = L.calculate_total(st.session_state.wb_item_price, st.session_state.wb_qty)

                    library[name] = {
                        "price": float(st.session_state.wb_item_price),
                        "qty": int(st.session_state.wb_qty),
                        "total": float(total),
                        "saved_at": _stamp(),
                        "workbench_result": st.session_state.wb_result,
                    }
                    L.save_to_library(library)

                    # Clear Workbench after save (as requested)
                    st.session_state.wb_text = ""
                    st.session_state.wb_file = None
                    st.session_state.wb_result = None
                    st.session_state.wb_error = None
                    st.session_state.wb_item_name = ""
                    st.session_state.wb_item_price = 0.0
                    st.session_state.wb_qty = 1

                    st.success(f"Saved to Vault: {name}")
                    st.rerun()

                except Exception:
                    st.error("Save failed.")
                    if st.session_state.dev_mode:
                        st.code(traceback.format_exc())

    with right:
        st.subheader("Output")
        if st.session_state.wb_error:
            st.error(st.session_state.wb_error)

        if st.session_state.wb_result is None:
            st.info("No output yet. Add input and press Process.")
        else:
            st.json(st.session_state.wb_result)

            if st.session_state.dev_mode:
                st.divider()
                st.subheader("Debug payload (dev)")
                p=_workbench_payload()
                st.write("file_obj:", p["file_obj"])
                st.write("filename:", p["filename"])
                st.write("file_bytes_len:", None if p.get("file_bytes") is None else len(p["file_bytes"]))
                st.write("text_len",0 if not p.get("text") else len(p["text"]))
                st.code(json.dumps(_workbench_payload(), indent=2, default=str), language="json")


def _page_vault(L) -> None:
    st.header("🗄️ Vault")
    st.caption("Saved results as selectable cards. Select an item to expand its details.")

    st.divider()

    try:
        library = L.load_library()
    except Exception:
        st.error("Could not load Vault.")
        if st.session_state.dev_mode:
            st.code(traceback.format_exc())
        return

    if not library:
        st.info("Vault is empty. Save something from the Workbench.")
        return

    q = st.text_input("Search", placeholder="filter by name…").strip().lower()
    keys = list(library.keys())
    if q:
        keys = [k for k in keys if q in k.lower()]

    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.subheader("Item List")
        for k in keys:
            v = library.get(k, {}) or {}
            with st.container(border=True):
                st.write(f"**{k}**")
                st.caption(f"qty: {v.get('qty', 0)} • price: ${v.get('price', 0)} • total: ${v.get('total', 0)}")

                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    if st.button("View details", key=f"view_{k}", use_container_width=True):
                        st.session_state.vault_selected_key = k
                with c2:
                    if st.button("Delete", key=f"del_{k}", use_container_width=True):
                        try:
                            ok = L.delete_item(k)
                            if ok:
                                st.toast("Deleted.", icon="🗑️")
                                if st.session_state.vault_selected_key == k:
                                    st.session_state.vault_selected_key = None
                                st.rerun()
                            else:
                                st.error("Delete failed (not found).")
                        except Exception:
                            st.error("Delete failed.")
                            if st.session_state.dev_mode:
                                st.code(traceback.format_exc())

    with right:
        st.subheader("Detail View")
        sel = st.session_state.vault_selected_key
        if not sel:
            st.info("Select an item to expand its full content/details.")
            return

        data = library.get(sel)
        if data is None:
            st.warning("Selected item no longer exists.")
            st.session_state.vault_selected_key = None
            return

        st.write(f"**{sel}**")
        st.json(data)


def _page_help() -> None:
    st.header("❓ Help / Support")

    st.divider()

    st.subheader("General questions & answers")
    with st.expander("How do I use this app?"):
        st.write("Home → Start → Workbench → Process → Save → Vault.")
    with st.expander("What does Scrap do?"):
        st.write("Scrap clears the Workbench draft without saving.")
    with st.expander("What does Save do?"):
        st.write("Save commits the current draft to the Vault and clears Workbench.")
    with st.expander("Why does nothing execute on import?"):
        st.write("Imports define; run executes. It prevents surprise behavior and keeps things stable.")

    st.divider()

    st.subheader("Report bug / request new feature / request login")
    kind = st.selectbox("Type", ["Bug report", "Feature request", "Access / login request"], index=0)
    summary = st.text_input("Summary", placeholder="One sentence summary")
    details = st.text_area("Details", height=160, placeholder="Steps, expected vs actual, screenshots…")
    contact = st.text_input("Contact (optional)", placeholder="email or phone")

    if st.button("Submit", type="primary"):
        ticket = {
            "id": str(uuid.uuid4())[:8],
            "stamp": _stamp(),
            "type": kind,
            "summary": summary,
            "details": details,
            "contact": contact,
        }
        st.session_state.last_ticket = ticket
        st.success("Submitted (local stub).")
        st.json(ticket)


# ==============================================================================
# RUN BOUNDARY
# ==============================================================================
def run() -> None:
    _ensure_state()
    st.set_page_config(page_title=APP_NAME, page_icon="🧱", layout="wide")

    _sidebar()

    # Import logic only when app is actually running
    try:
        L = _import_logic()
    except Exception as e:
        st.error(f"Logic import error: {e}")
        st.caption("Fix the logic filename in _import_logic(), or ensure required functions exist.")
        st.code(traceback.format_exc())
        st.stop()

    page = st.session_state.page
    if page == "Home":
        _page_home()
    elif page == "Workbench":
        _page_workbench(L)
    elif page == "Vault":
        _page_vault(L)
    elif page == "Help":
        _page_help()
    else:
        st.session_state.page = "Home"
        _page_home()


if __name__ == "__main__":
    run()