"""Module with auth handlers."""

from datetime import timedelta
from typing import Annotated
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
    Response,
    status,
    UploadFile,
    File
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from auth.dependencies import (
    get_current_active_user,
)
from auth.models import User
from settings import settings
from table_processing.timetable import Timetable
from table_processing import table_parser

import logging

router = APIRouter(prefix="/timetable", tags=["timetable"])
templates = Jinja2Templates(directory="templates")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_timetable(request: Request, user: Annotated[User, Depends(get_current_active_user)]):
    """
    Get the timetable for the current user.

    Args:
        user (User): The current authenticated user.
    """
            
    if user.is_admin:
        return templates.TemplateResponse(
            request=request,
            name="load_timetable.html",
        )
    elif user.group is None:
        
        return templates.TemplateResponse(
            request=request,
            name="timetable.html",
            context={
                "timetable": Timetable.get_timetable_for_teacher(user.username),
            },
        )
        
    elif user.group is not None:
        logging.error(f"Getting timetable for student group: {user.group}")
        logging.error(f"{Timetable.timetable}")
        return templates.TemplateResponse(
            request=request,
            name="timetable.html",
            context={
                "timetable": Timetable.get_timetable_for_student(user.group),
            },
        )
        
@router.post("/load", status_code=status.HTTP_200_OK)
async def load_timetable(request: Request, user: Annotated[User, Depends(get_current_active_user)], uploaded_file: UploadFile):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can load timetable")
    read_data = await uploaded_file.read()
    
    if uploaded_file.filename.endswith("pdf"):
        # Load timetable from PDF file
        logging.error(f"Uploaded file PDF")
        file_path = Path(__file__).parent / "timetable.pdf"
        with open(file_path, "wb") as f:
            f.write(read_data)
        parser = table_parser.PDFTableParser(str(file_path))
        logging.error(f"Parsed file")
        logging.error(f"{parser.file}")
    elif uploaded_file.filename.endswith("excel"):
        # Load timetable from Excel file
        file_path = Path(__file__).parent / "timetable.xlsx"
        with open(file_path, "wb") as f:
            f.write(read_data)
        parser = table_parser.ExcelTableParser(str(file_path))
    elif uploaded_file.filename.endswith("pickle"):
        file_path = Path(__file__).parent / "timetable.pkl"
        with open(file_path, "wb") as f:
            f.write(read_data)
        # Load timetable from Pickle file
        parser = table_parser.PickleTableParser(str(file_path))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file format")
    return templates.TemplateResponse(
        request=request,
        name="timetable.html",
        context={
            "timetable": Timetable.load_timetable(parser.get_table()),
        },
    )
    
