interface ButtonProps {
  onClick: () => void;
  tooltip: string;
  iconClass: any;
}

export default function Button(props: ButtonProps) {
  return (
    <button
      className="mr-5 cursor-pointer rounded-md bg-rock py-2 px-4 duration-150 hover:bg-light-rock hover:ease-linear"
      onClick={props.onClick}
      title={props.tooltip}
    >
      <props.iconClass weight="bold" />
    </button>
  );
}
