import { DotsSixVertical } from "@phosphor-icons/react";
import { DragControls } from "framer-motion";

interface ReorderIconProps {
  dragControls: DragControls;
}

export default function ReorderIcon(props: ReorderIconProps) {
  return (
    <DotsSixVertical size={24} onPointerDown={(event) => props.dragControls.start(event)} className="cursor-grab" />
  );
}
