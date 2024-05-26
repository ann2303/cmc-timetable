"""Module with timetable handlers."""

import logging
from typing import Annotated

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from fastapi.templating import Jinja2Templates

from auth.dependencies import get_current_active_user
from auth.models import User
from gettext_translate import _
from settings import settings
from table_processing import table_parser
from table_processing.timetable import Timetable

router = APIRouter(prefix="/timetable", tags=["timetable"])
templates = Jinja2Templates(directory="templates")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_timetable(request: Request, user: Annotated[User, Depends(get_current_active_user)]):
    """
    Get the timetable for the current user.

    Args:
        user (User): The current authenticated user.
    """
    try:
        if user.is_admin:
            return templates.TemplateResponse(
                request=request,
                name="timetable.html",
                context={"timetable": Timetable.get_timetable_for_admin(), "gettext": _},
            )
        elif user.group is None:
            return templates.TemplateResponse(
                request=request,
                name="timetable.html",
                context={"timetable": Timetable.get_timetable_for_teacher(user.username), "gettext": _},
            )
    except Exception as e:
        logging.error(e)

    try:
        return templates.TemplateResponse(
            request=request,
            name="timetable.html",
            context={"timetable": Timetable.get_timetable_for_student(user.group), "gettext": _},
        )
    except Exception as exc:
        logging.error(exc)


async def save_read_timetable(read_data: bytes, file_path: str):
    """Save the timetable file to the support directory."""

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(read_data)


@router.post("/load", status_code=status.HTTP_200_OK)
async def load_timetable(
    request: Request, user: Annotated[User, Depends(get_current_active_user)], uploaded_file: UploadFile
):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_("Only admin users can load timetable"))
    read_data = await uploaded_file.read()

    if uploaded_file.filename.endswith("pdf"):
        # Load timetable from PDF file
        file_path = settings.SUPPORT_DIR / "timetable.pdf"
        await save_read_timetable(read_data, file_path)
        parser = table_parser.PDFTableParser(str(file_path))
    elif uploaded_file.filename.endswith("xlsx"):
        # Load timetable from Excel file
        file_path = settings.SUPPORT_DIR / "timetable.xlsx"
        await save_read_timetable(read_data, file_path)
        parser = table_parser.ExcelTableParser(str(file_path))
    elif uploaded_file.filename.endswith("pkl"):
        # Load timetable from Pickle file
        file_path = settings.SUPPORT_DIR / "timetable.pkl"
        await save_read_timetable(read_data, file_path)
        parser = table_parser.PickleParser(str(file_path))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_("Unsupported file format"))
    return templates.TemplateResponse(
        request=request,
        name="timetable.html",
        context={"timetable": Timetable.load_timetable(parser.get_table()), "gettext": _},
    )


@router.get("/load", status_code=status.HTTP_200_OK)
def show_timetable(request: Request, user: Annotated[User, Depends(get_current_active_user)]):
    """
    Show the loaded timetable for admin.
    """

    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=_("Only admin users can load timetable"))
    return templates.TemplateResponse(request=request, context={"gettext": _}, name="load_timetable.html")
