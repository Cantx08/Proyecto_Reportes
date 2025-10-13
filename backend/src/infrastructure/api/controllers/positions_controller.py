from fastapi import HTTPException

from ....application.dto import (
    PositionDTO, PositionCreateDTO, PositionUpdateDTO,
    PositionsResponseDTO, PositionResponseDTO
)
from ....application.services.position_service import PositionService
from ....domain.entities.position import Position


class PositionsController:
    """Controlador para manejar endpoints relacionados con cargos/posiciones."""

    def __init__(self, position_service: PositionService):
        self.position_service = position_service

    async def get_position_by_id(self, pos_id: str) -> PositionResponseDTO:
        """Obtiene un cargo por su ID."""
        try:
            position = await self.position_service.get_position_by_id(pos_id)
            if not position:
                return PositionResponseDTO(
                    success=False,
                    data=None,
                    message=f"Position with ID {pos_id} not found"
                )

            position_dto = PositionDTO(
                pos_id=position.pos_id,
                pos_name=position.pos_name
            )

            return PositionResponseDTO(
                success=True,
                data=position_dto,
                message="Position retrieved successfully"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_positions(self) -> PositionsResponseDTO:
        """Obtiene todos los cargos."""
        try:
            positions = await self.position_service.get_all_positions()

            positions_dto = [
                PositionDTO(
                    pos_id=position.pos_id,
                    pos_name=position.pos_name
                )
                for position in positions
            ]

            return PositionsResponseDTO(
                success=True,
                data=positions_dto,
                message=f"Retrieved {len(positions)} positions successfully",
                total=len(positions)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_position(self, position_create: PositionCreateDTO) -> PositionResponseDTO:
        """Crea un nuevo cargo."""
        try:
            position = Position(
                pos_id=position_create.pos_id,
                pos_name=position_create.pos_name
            )

            created_position = await self.position_service.create_position(position)

            position_dto = PositionDTO(
                pos_id=created_position.pos_id,
                pos_name=created_position.pos_name
            )

            return PositionResponseDTO(
                success=True,
                data=position_dto,
                message="Position created successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_position(self, pos_id: str, position_update: PositionUpdateDTO) -> PositionResponseDTO:
        """Actualiza un cargo existente."""
        try:
            # Obtener el cargo actual
            existing_position = await self.position_service.get_position_by_id(pos_id)
            if not existing_position:
                raise HTTPException(status_code=404, detail=f"Position with ID {pos_id} not found")

            # Actualizar el cargo
            updated_position = Position(
                pos_id=existing_position.pos_id,
                pos_name=position_update.pos_name
            )

            result_position = await self.position_service.update_position(updated_position)

            position_dto = PositionDTO(
                pos_id=result_position.pos_id,
                pos_name=result_position.pos_name
            )

            return PositionResponseDTO(
                success=True,
                data=position_dto,
                message="Position updated successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_position(self, pos_id: str) -> PositionResponseDTO:
        """Elimina un cargo por su ID."""
        try:
            deleted = await self.position_service.delete_position(pos_id)
            if not deleted:
                raise HTTPException(status_code=404, detail=f"Position with ID {pos_id} not found")

            return PositionResponseDTO(
                success=True,
                data=None,
                message="Position deleted successfully"
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
