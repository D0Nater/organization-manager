"""Default exception handlers for the intape package."""

from logging import getLogger
from typing import Any
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .base import AbstractException


logger = getLogger(__name__)

EMPTY_EXCEPTION_UUID = "00000000-0000-0000-0000-000000000000"


class ErrorSchema(BaseModel):
    """Schema for standardized error responses returned by exception handlers."""

    detail: str | None = Field(
        description="Optional exception detail. Public and can be shown to the user.",
        examples=["Service 1 not found."],
    )
    error_code: str = Field(description="The exception name or code.", examples=["ServiceNotFoundException"])
    event_id: str | UUID = Field(
        description="Exception event UUID for tracking. Can be shared with support to request more details. "
        "If it equals zero, then the exception is not tracked.",
    )
    additional_info: dict[str, Any] = Field(
        description="Additional computer-readable information about the error.",
        examples=[{"service_id": 1}],
    )


async def abstract_exception_handler(request: Request, exc: AbstractException, log: bool = True) -> JSONResponse:
    """Handles custom AbstractException instances and returns a standardized error response.

    Args:
        request (Request): The incoming HTTP request.
        exc (AbstractException): The raised application-specific exception.
        log (bool, optional): Whether to log the exception. Defaults to True.

    Returns:
        JSONResponse: A JSON response containing error details following ErrorSchema.
    """
    if log:
        exc._log()

    if exc.current_request_id is None:
        exc.current_request_id = request.state.request_id

    if not exc.is_public:
        return await unknown_exception_handler(request, exc)

    error_schema = ErrorSchema(
        error_code=exc.__class__.__name__,
        detail=exc.current_detail,
        event_id=str(exc.current_request_id),
        additional_info=exc.current_additional_info,
    ).model_dump(mode="json")

    return JSONResponse(status_code=exc.current_status_code, content=error_schema, headers=exc.current_headers)


async def unknown_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles unexpected exceptions and returns a standardized error response.

    Args:
        request (Request): The incoming HTTP request.
        exc (Exception): The raised unknown exception.

    Returns:
        JSONResponse: A JSON response with generic error details following ErrorSchema.
    """
    id_: UUID = request.state.request_id
    logger.exception(f"({id_}) Unknown exception occurred. Details:")

    error_schema = ErrorSchema(
        error_code="UnknownException",
        detail="Unknown exception occurred.",
        event_id=str(id_),
        additional_info={},
    ).model_dump(mode="json")

    return JSONResponse(status_code=500, content=error_schema)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handles HTTPException instances and returns a standardized error response.

    Args:
        request (Request): The incoming HTTP request.
        exc (HTTPException): The raised FastAPI/Starlette HTTPException.

    Returns:
        JSONResponse: A JSON response containing HTTP exception details following ErrorSchema.
    """
    id_: UUID = request.state.request_id
    logger.exception(f"({id_}) Raw HTTPException occurred. Details:")

    error_schema = ErrorSchema(
        error_code="Exception",
        detail=exc.detail,
        event_id=str(id_),
        additional_info={},
    ).model_dump(mode="json")

    return JSONResponse(status_code=exc.status_code, content=error_schema)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles Pydantic request validation errors and returns a standardized error response.

    Args:
        request (Request): The incoming HTTP request.
        exc (RequestValidationError): The raised validation exception.

    Returns:
        JSONResponse: A JSON response containing validation error details following ErrorSchema.
    """
    errors = exc.errors()

    for error in errors:
        if "ctx" in error:
            del error["ctx"]
        if "url" in error:
            del error["url"]

    error_schema = ErrorSchema(
        error_code="UnprocessableEntityException",
        detail="Invalid request data.",
        event_id=EMPTY_EXCEPTION_UUID,
        additional_info={"errors": errors},
    ).model_dump(mode="json")

    return JSONResponse(status_code=422, content=error_schema)


async def not_found_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handles 404 not found errors and returns a standardized error response with helpful links.

    Args:
        request (Request): The incoming HTTP request.
        exc (HTTPException): The raised 404 HTTPException.

    Returns:
        JSONResponse: A JSON response describing the 404 error following ErrorSchema.
    """
    error_schema = ErrorSchema(
        error_code="EndpointNotFoundException",
        detail="404 endpoint not found.",
        event_id=EMPTY_EXCEPTION_UUID,
        additional_info={},
    ).model_dump(mode="json")

    error_schema["additional_info"]["urls"] = {
        "openapi": "/openapi.json",
        "docs": "/docs",
    }

    return JSONResponse(status_code=404, content=error_schema)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers default exception handlers with the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    app.add_exception_handler(AbstractException, abstract_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unknown_exception_handler)
    app.add_exception_handler(404, not_found_exception_handler)  # type: ignore[arg-type]
