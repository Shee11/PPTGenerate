"""Data.KPI layout strategy for metric dashboards."""
from typing import List, Dict

from src.common.bounds import Bounds
from src.common.size_class import SizeClass
from src.common.slot import Slot
from src.paged.layout.layout_protocol import LayoutContext, WidgetLayoutInput


class DataKPIRowStrategy:
    """Data.KPI_Row: Dashboard header with KPI metrics.
    
    Layout: M header spanning top + 4 S KPI cells in bottom row.
    Perfect for dashboard headers and quarterly reports.
    """

    @staticmethod
    def get_strategy_name() -> str:
        """Return strategy name."""
        return "Data.KPI_Row"

    @staticmethod
    def get_slots() -> List[Slot]:
        """Return header (M) + 4 KPI (S) slots."""
        return [
            Slot(role="header", size=SizeClass.M),
            Slot(role="kpi_1", size=SizeClass.S),
            Slot(role="kpi_2", size=SizeClass.S),
            Slot(role="kpi_3", size=SizeClass.S),
            Slot(role="kpi_4", size=SizeClass.S),
        ]
    
    @staticmethod
    def calculate_layout(
        widgets: List[WidgetLayoutInput],
        context: LayoutContext,
    ) -> Dict[str, Bounds]:
        """Calculate KPI row layout with header + metric cells.
        
        Layout structure:
        [         header (30%)         ]
        [kpi_1] [kpi_2] [kpi_3] [kpi_4]
        
        Args:
            widgets: List of widgets to layout
            context: Layout context
            
        Returns:
            Dictionary mapping role -> Bounds
        """
        bounds_map: Dict[str, Bounds] = {}
        
        # Header takes 30% of height, full width
        header_height = context.content_height * 0.3 - (context.gutter / 2)
        
        # KPIs take remaining 70% height, divided into 4 columns
        kpi_height = context.content_height * 0.7 - (context.gutter / 2)
        kpi_width = (context.content_width - (context.gutter * 3)) / 4
        
        for widget in widgets:
            if widget.role == "header":
                bounds_map["header"] = Bounds(
                    x=context.content_x,
                    y=context.content_y,
                    width=context.content_width,
                    height=header_height
                )
            elif widget.role.startswith("kpi_"):
                # Extract KPI number (1-4)
                kpi_num = int(widget.role.split("_")[1]) - 1
                kpi_x = context.content_x + (kpi_num * (kpi_width + context.gutter))
                kpi_y = context.content_y + header_height + context.gutter
                
                bounds_map[widget.role] = Bounds(
                    x=kpi_x,
                    y=kpi_y,
                    width=kpi_width,
                    height=kpi_height
                )
        
        return bounds_map
