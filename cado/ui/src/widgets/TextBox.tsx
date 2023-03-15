interface ButtonProps {
  value: string;
  placeholder: string;
  onBlur: (value: string) => void;
  onChange: (value: string) => void;
}

export default function Button(props: ButtonProps) {
  return (
    <input
      className="inline-block w-24 rounded-md bg-rock py-2 px-4 outline-none duration-150 placeholder:text-gray-600 focus:bg-light-rock active:ease-linear"
      type="text"
      value={props.value}
      placeholder={props.placeholder}
      onBlur={(event) => props.onBlur(event.target.value)}
      onChange={(event) => props.onChange(event.target.value)}
    ></input>
  );
}
