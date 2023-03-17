interface SlyTextBoxProps {
  value: string;
  placeholder: string;
  onBlur: (value: string) => void;
  onChange: (value: string) => void;
}

export default function SlyTextBox(props: SlyTextBoxProps) {
  return (
    <input
      className="inline-block bg-transparent outline-none"
      type="text"
      value={props.value}
      placeholder={props.placeholder}
      onBlur={(event) => props.onBlur(event.target.value)}
      onChange={(event) => props.onChange(event.target.value)}
    ></input>
  );
}
